from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages

# Create your views here.

def shopping_bag(request):
    extra_title = "- Shopping Bag"
    context = {
    'extra_title': extra_title,
    }
    return render(request, 'bag.html', context)

# View for handling adding items to the shopping bag

def add_to_bag(request, product_id):
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product = get_object_or_404(Product, id=product_id)
    bag = request.session.get('bag', {})
    id_str = str(product_id)
    if id_str in list(bag.keys()):
        bag[id_str] += quantity
    else:
        bag[id_str] = quantity

    request.session['bag'] = bag
    messages.success(request, f"You have succesfully added {product.title} to your bag!")
    return redirect(redirect_url)

# View for handling removing items from the shopping bag

def remove_from_bag(request, product_id):
    redirect_url = request.POST.get('redirect_url')
    product = get_object_or_404(Product, id=product_id)
    bag = request.session.get('bag', {})
    id_str = str(product_id)

    if id_str in list(bag.keys()):
        bag.pop(id_str)
    else:
        messages.success(request, f"An error occured when trying to remove {product.title} from your bag! Try again later!")
        return redirect(redirect_url)
    
    request.session['bag'] = bag
    messages.success(request, f"You have removed {product.title} from your bag!")
    return redirect(redirect_url)