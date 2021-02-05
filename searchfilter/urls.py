from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='api_products')
router.register(r'orders', views.OrderViewSet, basename='api_orders')

urlpatterns = [
    path('', include(router.urls)),
]