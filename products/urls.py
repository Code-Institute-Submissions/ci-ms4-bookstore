from products.views import ProductListView, EditProductView, delete_product, EditAuthorView, EditGenreView, EditSeriesView
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
    path('dashboard/api/list-all', ProductListView.as_view(), name='product-list'),    
    path('dashboard/api/edit_product/<slug:pk>', EditProductView.as_view(), name='edit_product'),
    path('dashboard/api/edit_genre/<slug:pk>', EditGenreView.as_view(), name='edit_genre'),
    path('dashboard/api/edit_series/<slug:pk>', EditSeriesView.as_view(), name='edit_series'),
    path('dashboard/api/edit_author/<slug:pk>', EditAuthorView.as_view(), name='edit_author'),
    path('dashboard/api/delete_product/<int:product_id>', views.delete_product, name='delete_product'),

]