from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

# Import in-memory PRODUCTS to enrich cart display
from products.views import PRODUCTS
from .forms import CheckoutForm
from django.utils import timezone


def cart_view(request):
    items, total = build_cart_items_from_session(request.session)
    return render(request, 'cart/cart.html', {'cart_items': items, 'total': total})


def build_cart_items_from_session(session):
    cart = session.get('cart', {})
    items = []
    total = 0.0
    for k, v in cart.items():
        try:
            pid = int(k)
            qty = int(v)
        except (TypeError, ValueError):
            continue
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if not product:
            continue
        line_total = product['price'] * qty
        total += line_total
        items.append({'product': product, 'quantity': qty, 'line_total': line_total})
    return items, total


def checkout_view(request):
    items, total = build_cart_items_from_session(request.session)
    # If cart is empty, show helpful message
    if not items:
        return render(request, 'cart/checkout.html', {'cart_items': items, 'total': total, 'empty_cart': True})
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Build order-like structure and save to session (lightweight simulation)
            order = {
                'id': int(timezone.now().timestamp()),
                'created_at': timezone.now().isoformat(),
                'customer': {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data.get('last_name', ''),
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data.get('phone', ''),
                },
                'shipping_address': {
                    'address': form.cleaned_data['address'],
                    'city': form.cleaned_data['city'],
                    'postal_code': form.cleaned_data['postal_code'],
                    'country': form.cleaned_data['country'],
                },
                'notes': form.cleaned_data.get('notes', ''),
                'items': items,
                'total': total,
            }
            request.session['last_order'] = order
            messages.success(request, 'Order placed successfully — thank you for your purchase!')
            # Clear the cart
            request.session['cart'] = {}
            # Redirect to order summary/success
            return redirect('orders:summary')
    else:
        # prefills
        initial = {}
        if request.user.is_authenticated:
            if hasattr(request.user, 'first_name') and request.user.first_name:
                initial['first_name'] = request.user.first_name
            if hasattr(request.user, 'last_name') and request.user.last_name:
                initial['last_name'] = request.user.last_name
            if hasattr(request.user, 'email') and request.user.email:
                initial['email'] = request.user.email
        form = CheckoutForm(initial=initial)
    return render(request, 'cart/checkout.html', {'form': form, 'cart_items': items, 'total': total})


@require_POST
def add_to_cart(request, product_id):
    # Simple session-based cart: {product_id: quantity}
    cart = request.session.get('cart', {})
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    request.session['cart'] = cart
    # Friendly flash message for UX (shows as toast in the frontend)
    try:
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
    except Exception:
        product = None
    if product:
        messages.success(request, f'Added "{product["name"]}" to cart.')
    else:
        messages.success(request, 'Added item to cart.')
    # Redirect back to the product detail page (or cart if referer missing)
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('cart:cart')


@require_POST
def remove_from_cart(request, product_id):
    """Remove an item from the session-based cart entirely.

    Expects POST and a product_id. Redirects back to the cart view.
    """
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        cart.pop(pid, None)
        request.session['cart'] = cart
        messages.info(request, 'Item removed from cart.')
    else:
        messages.warning(request, 'Item not found in cart.')
    # redirect back to cart page
    return redirect('cart:cart')
