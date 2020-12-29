from django.urls import path
from . import views

urlpatterns = [
    path('shopping-bag', views.shopping_bag, name='shopping_bag'),    
]