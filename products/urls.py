from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('details/<int:id>', views.single_product, name='details'),
    path('search', views.search, name='search'),
]
