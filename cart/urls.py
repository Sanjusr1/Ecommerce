from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove'),
    path('add/<int:product_id>/', views.add_to_cart, name='add'),
]
