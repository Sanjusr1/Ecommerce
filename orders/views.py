from django.shortcuts import render




def order_summary(request):
    order = request.session.get('last_order')
    return render(request, 'orders/order_summary.html', {'order': order})


def order_success(request):
    order = request.session.get('last_order')
    return render(request, 'orders/order_success.html', {'order': order})
