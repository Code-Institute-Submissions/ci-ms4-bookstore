from django.urls import path
from . import views

urlpatterns = [
    path('shopping-bag', views.shopping_bag, name='shopping_bag'),    
    path('add_to_bag/<int:product_id>', views.add_to_bag, name='add_to_bag'),
]