from orders.models import Order, OrderItems


def cart_details(request):
  context= {}
  if request.user.is_authenticated and not request.user.is_anonymous:
    if Order.objects.all().filter(user=request.user, complated=False):
      order = Order.objects.get(user=request.user, complated=False)
      orderdetails = OrderItems.objects.all().filter(order=order)
      total = 0
      for sub in orderdetails:
        total += sub.price * sub.quantity
      context = {
        'order': order,
        'orderdetails': orderdetails,
        'total': total,
      }
  return context