from products.views import delete_product
from home.views import edit_post
from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.products, name='products'),
    path('<int:product_id>/', views.product_info, name='product_info'),
    path('dashboard/', views.dashboard, name ='dashboard'),
    path('dashboard/api/edit_product/<int:product_id>', views.edit_product, name='edit_product'),
    path('dashboard/api/delete_product/<int:product_id>', views.delete_product, name='delete_product')
]