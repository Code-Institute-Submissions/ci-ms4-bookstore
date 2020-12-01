from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('archive/', views.archive, name='archive'),
    path('archive/api/add_post/', views.add_post, name='add_post')
]