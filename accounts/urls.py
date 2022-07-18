from django.urls import path
from . import views
urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('add_favorite/<int:id>', views.add_fav_products, name='add_favorite'),
    path('favorites', views.favorites, name='favorites'),
]
