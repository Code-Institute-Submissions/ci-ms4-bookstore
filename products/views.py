from products.models import Product
from .forms import ProductForm
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
# Create your views here.


def products(request):
    """
    Products view, containing an oversight of all products. Since this is also the 'landing page' for visitors
    """

    products = Product.objects.all()
    # Feature grabs the first 5 objects that match featured, so the main page is not inundated.
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
    # reviews = ProductReview.objects.filter(=product_info)

    """
    # Post handler for user reviews
     if request.method == 'POST':
        if request.user.is_anonymous():
            messages.warning(request, 'Only logged in users can add comments')
            return HttpResponseRedirect('products/<int:product_id>/')
        else:
            
    """



    context = {
        "product": product,
        "product_info": product_info,
        # "reviews": reviews,
        "user": user,
    }

    return render(request, 'product_info.html', context)

@login_required
def dashboard(request):
    user = request.user
    form = ProductForm(request.POST, request.FILES)
    if request.method == 'POST':
        if request.user.is_superuser:            
            #Instancing new product
            instance = form.save(commit=False)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product item added!')
                return HttpResponseRedirect('dashboard')
            else:
                messages.warning(request, 'One or more fields were not valid. Please try again.')
                return HttpResponseRedirect('dashboard')
        else:        
            messages.warning(request, 'Please log in before trying to add new products!')
    context = {
    'user': user,
    'form': form
    }
    return render(request, 'dashboard.html', context)
