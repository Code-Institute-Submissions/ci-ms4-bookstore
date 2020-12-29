from bag.views import shopping_bag
from django.shortcuts import request

def bag_items(request):

    item_contents = []
    product_counter = 0
    total = 0
    # Placeholder value for Delivery while I figure out how I want to handle that.
    delivery = 10
    grand_total = total + delivery

    context = {
        'item_contents': item_contents,
        'product_counter': product_counter,
        'total': total,
        'grand_total': grand_total
    }

    return context
