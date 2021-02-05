from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='api_products')
router.register(r'orders', views.OrderViewSet, basename='api_orders')


"""
    Commented out, as the corresponding view is commented out, please see searchfilter.views line 22 for explanation.

    path('vote_rigger', views.vote_rigger, name='vote_rigger')
    
"""
urlpatterns = [
    path('', include(router.urls)),
]


