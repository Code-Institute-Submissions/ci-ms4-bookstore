from products.models import Product, ProductReview
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.


def products(request):
    # Products view, containing an oversight of all products. Since this is also the 'landing page' for visitors, it also contains 
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