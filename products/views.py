from django.shortcuts import render


# In-memory product dataset used for the lightweight prototype.
# Each product includes an `image` key matching a file in `static/images/`.
PRODUCTS = [
    {
        'id': 1,
        'slug': 'sample-product-a',
        'name': 'Sample Product A',
        'price': 19.99,
        'description': 'A versatile gadget that solves everyday problems.',
        'image': 'images/product_a.svg',
        'category': 'Electronics',
    },
    {
        'id': 2,
        'slug': 'sample-product-b',
        'name': 'Sample Product B',
        'price': 29.99,
        'description': 'Premium quality with excellent durability.',
        'image': 'images/product_b.svg',
        'category': 'Electronics',
    },
    {
        'id': 3,
        'slug': 'sample-product-c',
        'name': 'Sample Product C',
        'price': 9.99,
        'description': 'Affordable and reliable — a customer favorite.',
        'image': 'images/product_c.svg',
        'category': 'Books',
    },
    {
        'id': 4,
        'slug': 'sample-product-d',
        'name': 'Sample Product D',
        'price': 14.50,
        'description': 'Lightweight and easy to carry around.',
        'image': 'images/product_d.svg',
        'category': 'Clothing',
    },
    {
        'id': 5,
        'slug': 'sample-product-e',
        'name': 'Sample Product E',
        'price': 49.00,
        'description': 'High-end model with extended warranty.',
        'image': 'images/product_e.svg',
        'category': 'Electronics',
    },
    {
        'id': 6,
        'slug': 'sample-product-f',
        'name': 'Sample Product F',
        'price': 5.99,
        'description': 'Compact accessory — great as a stocking stuffer.',
        'image': 'images/product_f.svg',
        'category': 'Clothing',
    },
]


def product_list(request):
    # If an optional query param 'category' is provided, filter here (fallback)
    category = request.GET.get('category')
    if category:
        filtered = [p for p in PRODUCTS if (p.get('category') or '').lower() == category.lower()]
        return render(request, 'products/product_list.html', {'products': filtered, 'selected_category': category})
    return render(request, 'products/product_list.html', {'products': PRODUCTS})


def product_list_by_category(request, category_slug):
    # category_slug will be a hyphenated/slug form; allow match by lowercased start
    # Map known categories to slug form
    slug_to_cat = {c.replace('-', '').replace(' ', '').lower(): c for c in ['Clothing', 'Books', 'Electronics']}
    # normalize incoming slug
    key = category_slug.replace('-', '').replace(' ', '').lower()
    category_name = slug_to_cat.get(key, category_slug)
    filtered = [p for p in PRODUCTS if (p.get('category') or '').lower() == (category_name or '').lower()]
    return render(request, 'products/product_list.html', {'products': filtered, 'selected_category': category_name})


def product_detail(request, pk):
    # Find product by id in the in-memory list. If not found, show a simple placeholder.
    product = next((p for p in PRODUCTS if p['id'] == int(pk)), None)
    if not product:
        product = {'id': pk, 'name': f'Sample Product {pk}', 'price': 19.99, 'description': 'A nice product.', 'image': 'images/product_c.svg'}
    return render(request, 'products/product_detail.html', {'product': product})


def category_list(request):
    categories = ['Clothing', 'Books', 'Electronics']
    return render(request, 'products/category_list.html', {'categories': categories})
