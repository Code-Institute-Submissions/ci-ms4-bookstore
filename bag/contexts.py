from decimal import Decimal
from django.shortcuts import get_object_or_404
from bag.views import shopping_bag
from products.models import Product

def bag_items(request):

    item_contents = []
    product_counter = 0
    total = 0
    # Placeholder value for Delivery while I figure out how I want to handle that.
    delivery = 10
    grand_total = total + delivery
    bag = request.session.get('bag', {})

    for product_id, quantity in bag.items():

        product = get_object_or_404(Product, pk=product_id)
        total += quantity * product.price
        product_counter += quantity
        item_contents.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product
        })


    context = {
        'item_contents': item_contents,
        'product_counter': product_counter,
        'total': total,
        'grand_total': grand_total
    }

    return context
