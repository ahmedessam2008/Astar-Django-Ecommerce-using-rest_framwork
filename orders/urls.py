from django.urls import path
from . import views
urlpatterns = [
  path('add_to_cart', views.add_to_cart, name='add_to_cart'),
  path('cart', views.cart, name='cart'),
  path('remove/<int:orderdetails_id>', views.remove_from_cart, name="remove_from_cart"),
  path('empty/<int:order_id>', views.empty_cart, name="empty_cart"),
  path('increase/<int:orderdetails_id>', views.increaseQty, name="increase_qty"),
  path('decrease/<int:orderdetails_id>', views.decreaseQty, name="decrease_qty"),
  path('payment', views.payment, name='payment'),
  path('show_orders', views.show_orders, name="show_orders")
]