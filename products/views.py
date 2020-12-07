from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.


def products(request):
    # Products view, containing an oversight of all products. Since this is also the 'landing page' for visitors, it also contains 
    products = Product.objects.all()
    
    context = {
        "products": products,

    }

    return render(request, 'products_all.html', context)