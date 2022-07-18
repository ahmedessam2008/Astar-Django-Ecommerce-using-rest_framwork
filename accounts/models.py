from products.models import Product
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
  gender = [
    ('male', 'male'),
    ('female', 'female'),
    ]
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  fav_products = models.ManyToManyField(Product)
  adress1 = models.CharField(max_length=50, null=True, blank=True)
  adress2 = models.CharField(max_length=50, null=True, blank=True)
  country = models.CharField(max_length=50, null=True, blank=True)
  zipcode = models.CharField(max_length=50, null=True, blank=True)
  gender = models.CharField(max_length=50, null=True, blank=True, choices=gender)
  age = models.IntegerField(null=True, blank=True)
  mobile = models.SlugField(max_length=50, null=True, blank=True)
  
  def __str__(self):
    return self.user.username