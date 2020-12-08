from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.


def products(request):
    # Products view, containing an oversight of all products. Since this is also the 'landing page' for visitors, it also contains 
    products = Product.objects.all()
    # Once data-entry is done, filter the feature var into [5]
    feature = Product.objects.filter(featured=True)
    context = {
        "products": products,
        "feature": feature,

    }

    return render(request, 'products_all.html', context)