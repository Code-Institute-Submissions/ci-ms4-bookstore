from django.urls import path
from . import views

urlpatterns = [
    path('all', views.products, name='products'),
    path('products/<int:product_id>/', views.product_info, name='product_info'),
    path('dashboard', views.dashboard, name ='dashboard')
]