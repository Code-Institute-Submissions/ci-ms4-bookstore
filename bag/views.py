from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages

# Create your views here.

def shopping_bag(request):

    return render(request, 'bag.html')

def add_to_bag(request, product_id):
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product = get_object_or_404(Product, id=product_id)
    bag = request.session.get('bag', {})

    if product_id in list(bag.keys()):
        bag[product_id] += quantity
    else:
        bag[product_id] = quantity

    request.session['bag'] = bag
    print(bag)
    messages.success(request, f"You have succesfully added {product.title} to your bag!")
    return redirect(redirect_url)