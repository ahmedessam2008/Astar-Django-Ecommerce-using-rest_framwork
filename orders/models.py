from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
# Create your models here.

class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  order_date = models.DateTimeField(auto_created=True, null=True, blank=True)
  order_details = models.ManyToManyField(Product, through='OrderItems')
  complated = models.BooleanField(default=False)
  total = 0
  items_count = 0
  
  def __str__(self):
    return f"user: {self.user.username}, Order ID {self.id}"
  
  
class OrderItems(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField(null=False)
  date_added = models.DateTimeField(auto_created=True, null=True, blank=True)
  
  def __str__(self):
    return f"User: {self.order.user.username}, Product: {self.product.title}, Order ID {self.order.id}"
  
  class Meta:
    ordering = ['-date_added']
    
    
class Payment(models.Model):
  pyment_method = [
    ('paypal','paypal'),
    ('cod','cod'),
    ('credit','credit'),
    ('bank','bank'),
  ]
  order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=True)
  shipping_adress = models.CharField(max_length=150, null=False, blank=True)
  shipping_mobile = models.CharField(max_length=150, null=False, blank=True)
  pyment_method = models.CharField(max_length=100, choices=pyment_method)
  card_number  = CardNumberField()
  expired = CardExpiryField(default="12/22")
  security_code = SecurityCodeField()
  