from urllib.robotparser import RequestRate
from django.shortcuts import render
from .models import Product, Size
from .forms import ProductForm


# Create your views here.

def products(request):
  pros = Product.objects.all()
  
  title = None
  category = None
  color=None
  startprice = None
  endprice = None
  if "productname" in request.GET:
    title = request.GET['productname']
    if title:
      pros = pros.filter(title__icontains=title)
  
  if "category" in request.GET:
    category = request.GET["category"]
    if category:
      pros = pros.filter(category__name__icontains=category)
  
  if "color" in request.GET:
    color = request.GET['color']
    if color:
      pros = pros.filter(colors__name__icontains=color)
      
  if 'startprice' in request.GET and 'endprice' in request.GET:
    startprice = request.GET["startprice"]
    endprice = request.GET["endprice"]
    if startprice and endprice:
      if startprice.isdigit() and endprice.isdigit():
        pros = pros.filter(price__gte=startprice, price__lte=endprice)
  
  context = {
    'products': pros,
  }
  return render(request, 'products/products.html', context)



def single_product(request, id):
  product_id = Product.objects.get(id=id)
    
  context = {
    'product_id': product_id,
  }
  return render(request, 'products/single_product.html', context)

def search(request):
  
  context = {
    
  }
  return render(request, 'products/search.html', context)


# def product(request, id):
#   product_id = Product.objects.get(id=id)
#   context = {
#     'product': Product.objects.all(),
#     'product_id': product_id,
#   }
#   return render(request, 'ecommerce/product.html', context)