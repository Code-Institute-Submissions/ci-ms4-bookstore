import random
from django.db.models import F
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from searchfilter.serializers import ProductSerializer, OrderSerializer
from products.models import Product
from checkout.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-date')
    permission_classes = [permissions.IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-upvote')
    permission_classes = [permissions.IsAuthenticated]

"""

Testing API - This view exists only for testing purposes and is used to manipulate the Product objects of the database, for testing the API.
It will be commented out from all deployed versions and is only included for assessment purposes. 



def vote_rigger(request):
    products = Product.objects.all()
    
    for product in products:
        Product.objects.filter(title=product.title).update(upvote=F('upvote') + random.randint(1, 101))
        Product.objects.filter(title=product.title).update(downvote=F('downvote') + random.randint(1, 101))
    
    return HttpResponseRedirect('/')

"""