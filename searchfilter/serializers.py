from rest_framework import serializers
from products.models import Product
from checkout.models import Order

"""

These classes will primarily exist as a REST-API for charts.JS in order to provide admins/staff with details on sales and activity.
Uses Django Rest-Framework model serializers.

"""

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'upvote', 'downvote', "price"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'user_id', 'date', 'grand_total']