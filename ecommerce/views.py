from django.shortcuts import render

from products.models import Product
from .models import *
# Create your views here.

def index(request):
  context = {
    'products': Product.objects.all(),
  }
  return render(request, 'ecommerce/index.html', context)


def cart(request):
  
  # if request.user.is_authenticated:
  #   customer = request.user.
  context= {
    
  }
  return render(request, 'ecommerce/cart.html', context)


def blog(request):
  
  context = {
    
  }
  return render(request, 'ecommerce/blog.html', context)


def checkout(request):
  
  context = {
    
  }
  return render(request, 'ecommerce/checkout.html', context)