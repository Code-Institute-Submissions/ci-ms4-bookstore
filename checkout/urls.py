from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('cache_checkout_data/',
         views.cache_checkout_data,
         name='cache_checkout_data'),
    path('success/<order_id>', views.checkout_success, name='checkout_success'),
    path('api/wh/', webhook, name='webhook'),
]
