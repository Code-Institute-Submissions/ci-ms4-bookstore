from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages

# Create your views here.

def shopping_bag(request):

    return render(request, 'bag.html')

# View for handling adding items to the shopping bag

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
    messages.success(request, f"You have succesfully added {product.title} to your bag!")
    return redirect(redirect_url)

# View for handling removing items from the shopping bag

def remove_from_bag(request, product_id):
    redirect_url = request.POST.get('redirect_url')
    product = get_object_or_404(Product, id=product_id)
    bag = request.session.get('bag', {})

    if str(product_id) in list(bag.keys()):
        bag.pop(str(product_id))
    else:
        messages.success(request, f"An error occured when trying to remove {product.title} from your bag! Try again later!")
        return redirect(redirect_url)
    
    request.session['bag'] = bag
    messages.success(request, f"You have removed {product.title} from your bag!")
    return redirect(redirect_url)