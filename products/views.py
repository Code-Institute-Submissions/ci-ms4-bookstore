from products.models import Product, ProductReview
from .forms import ProductForm, ReviewForm
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
# Create your views here.


def products(request):
    """
    Products view, containing an oversight of all products. 
    """

    products = Product.objects.all()
    # Feature grabs the first 5 objects that match as featured, so the main page is not inundated.
    feature = Product.objects.filter(featured=True)[:5]
    context = {
        "products": products,
        "feature": feature,
    }

    return render(request, 'products_all.html', context)

def product_info(request, product_id):
    # Detailed product object for individual entries.

    user = request.user
    product = get_object_or_404(Product, id=product_id)

    # Post handler for user reviews
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if request.user.is_anonymous:
            messages.warning(request, 'Only logged in users can add reviews!')
            return HttpResponseRedirect(request.path_info)
        else:                       
            if form.is_valid():
                instance = form.save(commit=False)
                # Appears to be only sending the user object on printing
                instance.reviewer = user
                instance.product = product
                instance.save()
                messages.success(request, 'Your review has been posted!')
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, 'Your review was not valid. Please, try again!')
                return HttpResponseRedirect(request.path_info)
            
    context = {
        # We pass a separate, unbound ReviewForm in the contexts on GET, to avoid issues with anonymous users who lack an instance
        "form": ReviewForm,
        "product": product,
        "product_info": product_info,
        # "reviews": reviews,
        "user": user,
    }

    return render(request, 'product_info.html', context)

@login_required
def dashboard(request):
    user = request.user
    if request.method == 'POST':
        if user.is_superuser:            
            form = ProductForm(request.POST, request.FILES)
            #Instancing new product
            instance = form.save(commit=False)
            if form.is_valid():
                instance.save()
                messages.success(request, 'Product item added!')
                return HttpResponseRedirect('dashboard')
            else:
                messages.warning(request, 'One or more fields were not valid. Please try again.')
                return HttpResponseRedirect('dashboard')
        else:        
            messages.warning(request, 'This URL is restricted to Staff members, please login with your staff account.')
            return HttpResponseRedirect('account_login')
    context = {
    'user': user,
    'form': ProductForm
    }
    return render(request, 'dashboard.html', context)

@login_required
def edit_product(request, product_id):
    # View for editing products
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if user.is_superuser:
            if form.is_valid():
                form.save()
                messages.success(request, f"You have succesfully edited {product.title}")
                return HttpResponseRedirect('dashboard')
            else:                
                messages.success(request, f"Failed to edit {product.title}, form was invalid.")
                return HttpResponseRedirect('dashboard')
        else:           
           messages.warning(request, 'This URL is restricted to Staff members, please login with your staff account.')
           return HttpResponseRedirect('account_login')

    context = {
        "product": product,
        'form': ProductForm(instance=product),
        "user": user,
    }

    return render(request, 'edit_product.html', context)

@login_required
def delete_product(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    
    if user.is_superuser:
        product.delete()
        messages.warning(request, f"You have succesfully deleted the product!")
        return HttpResponseRedirect('dashboard')
    else:           
        messages.warning(request, 'This URL is restricted to Staff members, please login with your staff account.')
        return HttpResponseRedirect('account_login')