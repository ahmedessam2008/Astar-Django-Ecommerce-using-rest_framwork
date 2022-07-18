from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order, OrderItems, Payment
from django.utils import timezone
# Create your views here.

def add_to_cart(request):
  if request.user.is_authenticated and not request.user.is_anonymous and 'pro_id' in request.GET and 'price' in request.GET and 'quantity' in request.GET:
    product_id = request.GET["pro_id"]
    qty = request.GET["quantity"]
    
    
    order = Order.objects.all().filter(user=request.user, complated=False)
    if not Product.objects.all().filter(id=product_id).exists():
      return redirect('products')
    product = Product.objects.get(id=product_id)
    if order: # هنا شرط لو رجع حاجه يبقي لسه فيه اوردر مخلصش لو مجابش اعمل اوردر جديد
      old_order = Order.objects.get(user=request.user, complated=False)
      # علشان لو فيه منتج مضاف قبل كده اجمعه علي القديم 
      if OrderItems.objects.all().filter(order=old_order, product=product).exists():
        orderdetails = OrderItems.objects.get(order=old_order, product=product)
        orderdetails.quantity += int(qty)
        orderdetails.save()
      else:
        orderdetails = OrderItems.objects.create(product=product, order=old_order,price=str(product.price), quantity=qty, date_added=timezone.now())
        messages.success(request, "Was added To cart For Old Order")
    else:
      new_order = Order()
      new_order.user = request.user
      new_order.order_date = timezone.now()
      new_order.complated = False
      new_order.save()
      orderdetails = OrderItems.objects.create(product=product, order=new_order, price=str(product.price), quantity=qty, date_added=timezone.now())
      messages.success(request, "create New Order")
    return redirect(f"/products/details/{request.GET['pro_id']}")
  else:
    if 'pro_id' in request.GET:
      messages.error(request, 'You must be Login')
      return redirect(f"/products/details/{request.GET['pro_id']}")
    else:
      return redirect('products')


def cart(request):
  context= None
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
  return render(request, 'orders/cart.html', context)


def remove_from_cart(request, orderdetails_id):
  if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderItems.objects.get(id=orderdetails_id)
    # حتي تمنع ان  اي مستخدم مسجل دخول يحزف او يغير حاجه من مستخدم تاني
    if orderdetails.order.user.id == request.user.id:
      orderdetails.delete()
  return redirect('cart')


def empty_cart(request, order_id):
  if request.user.is_authenticated and not request.user.is_anonymous and order_id:
    orders = Order.objects.all().filter(id=order_id)
    
    if orders.user.id == request.user.id:
      orders.delete()
  return redirect('cart')


def increaseQty(request, orderdetails_id):
  if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderItems.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id == request.user.id:
      orderdetails.quantity += 1
      orderdetails.save()
  return redirect('cart')

def decreaseQty(request, orderdetails_id):
  if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderItems.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id == request.user.id:
      if orderdetails.quantity > 1:
        orderdetails.quantity -= 1
        orderdetails.save()
  return redirect('cart')

def payment(request):
  context= {}
  adress1 = None
  mobile = None
  payment = None
  card_number = None
  expired = None
  security_code = None
  is_added = None
  if request.user.is_authenticated and not request.user.is_anonymous:
    
    if request.method == "POST" and "paymentbtn" in request.POST and 'adress1' in request.POST and 'mobile' in request.POST and 'payment' in request.POST:
      adress1 = request.POST['adress1']
      mobile = request.POST['mobile']
      payment = request.POST['payment']
      card_number = request.POST["card_number"]
      expired = request.POST["expired"]
      security_code = request.POST["security_code"]
      
      if Order.objects.all().filter(user=request.user,complated=False):
        order = Order.objects.get(user=request.user, complated=False)
      
      if adress1 and mobile and payment == "paypal":
        payment = Payment(order=order, shipping_adress=adress1, shipping_mobile=mobile, pyment_method=payment)
        payment.save()
        order.complated = True
        order.save()
        messages.success(request, "paypal Ship Complated ")
        
      elif adress1 and mobile and payment == "cod":
        payment = Payment(order=order, shipping_adress=adress1, shipping_mobile=mobile, pyment_method=payment)
        payment.save()
        order.complated = True
        order.save()
        messages.success(request, "Cash on Delivery Ship ")
        
      elif adress1 and mobile and payment == "credit" and 'card_number' in request.POST and 'expired' in request.POST and 'security_code' in request.POST:
        
        if card_number and expired and security_code:
          payment = Payment(order=order, shipping_adress=adress1, shipping_mobile=mobile, pyment_method=payment)
          payment.save()
          order.complated = True
          order.save()
          messages.success(request, "Credit Card Ship ")
        else:
          messages.success(request, "Credit Card Details Empty ")
          
      elif adress1 and mobile and payment == "bank":
        payment = Payment(order=order, shipping_adress=adress1, shipping_mobile=mobile, pyment_method=payment)
        payment.save()
        order.complated = True
        order.save()
        messages.success(request, "Direct Bank Transfer Ship ")

      else :
        messages.error(request, "empty Feilds")
  else:
    messages.error(request, "You Are Not Loggin from payment view")
  return render(request, 'orders/checkout.html', context)

def show_orders(request):
  context = {}
  all_orders = None
  if request.user.is_authenticated and not request.user.is_anonymous:
    all_orders = Order.objects.all().filter(user=request.user)
    for x in all_orders:
      order = Order.objects.get(id=x.id, user=request.user)
      orderdetails = OrderItems.objects.all().filter(order=order)
      total = 0
      for sub in orderdetails:
        total += sub.price * sub.quantity
      x.total = total
      x.items_count = orderdetails.count
    context={
      'all_orders': all_orders,
    }
  else:
    messages.error(request, "You Are Not Loggin ")
  return render(request, 'orders/show_orders.html', context)