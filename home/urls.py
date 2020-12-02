from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('archive/', views.archive, name='archive'),
    path('archive/api/add_post/', views.add_post, name='add_post'),
    path('archive/api/delete_post/<int:news_id>', views.delete_post, name='delete_post')
]