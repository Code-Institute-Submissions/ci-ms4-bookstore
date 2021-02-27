from products.views import *
from django.contrib.admin.views.decorators import staff_member_required
from home.views import edit_post
from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.products, name='products'),
    path('<int:product_id>/', views.product_info, name='product_info'),
    path('dashboard/', views.dashboard, name ='dashboard'),
    path('dashboard/api/add_author', views.add_author, name ='add_author'),
    path('dashboard/api/add_genre', views.add_genre, name ='add_genre'),
    path('dashboard/api/add_series', views.add_series, name ='add_series'),
    path('dashboard/api/list-all/products', staff_member_required(ProductListView.as_view(), login_url='/'), name='product-list'),    
    path('dashboard/api/list-all/orders', staff_member_required(OrderListView.as_view(), login_url='/'), name='order-list'),
    path('dashboard/api/edit_product/<slug:pk>', staff_member_required(EditProductView.as_view(), login_url='/'), name='edit_product'),
    path('dashboard/api/edit_order/<slug:pk>', staff_member_required(EditOrderView.as_view(), login_url='/'), name='edit_order'),
    path('dashboard/api/edit_genre/<slug:pk>', staff_member_required(EditGenreView.as_view(), login_url='/'), name='edit_genre'),
    path('dashboard/api/edit_series/<slug:pk>', staff_member_required(EditSeriesView.as_view(), login_url='/'), name='edit_series'),
    path('dashboard/api/edit_author/<slug:pk>', staff_member_required(EditAuthorView.as_view(), login_url='/'), name='edit_author'),
    path('dashboard/api/delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('dashboard/api/delete_author/<slug:pk>', staff_member_required(DeleteAuthorView.as_view(), login_url='/'), name='delete_author'),
    path('dashboard/api/delete_genre/<slug:pk>', staff_member_required(DeleteGenreView.as_view(), login_url='/'), name='delete_genre'),
    path('dashboard/api/delete_series/<slug:pk>', staff_member_required(DeleteSeriesView.as_view(), login_url='/'), name='delete_series'),

]