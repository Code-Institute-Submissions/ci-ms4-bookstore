from products.models import *
from .forms import ProductForm, ReviewForm
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse, render, get_object_or_404
# Create your views here.


def products(request):
    """
    Products view, containing an oversight of all products. 
    """
    products = Product.objects.all()
    query = None
    series = None
    author = None
    genre = None

    """
    Search handler

    """

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria! Please specify what to seasrch for."))
                return redirect(reverse('products'))

            queries = Q(title__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Feature grabs the first 5 objects that match as featured, so the main page is not inundated.
    feature = Product.objects.filter(featured=True)[:5]

    context = {
        "products": products,
        "feature": feature,
        "series_filter": series,
        "search_term": query,
    }

    return render(request, 'products_all.html', context)

def product_info(request, product_id):
    # Detailed product object for individual entries.

    user = request.user
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Post handler for user reviews, with instancing to keep unique reviews. Checks for a registered users review of this product, if not found instantiates one.
        try:
            prod_instance = ProductReview.objects.get(reviewer=user, product=product)
        except ProductReview.DoesNotExist:
            prod_instance = ProductReview(reviewer=user, product=product)
        form = ReviewForm(request.POST, instance=prod_instance)
        if request.user.is_anonymous:
            messages.warning(request, 'Only logged in users can add reviews!')
            return HttpResponseRedirect(request.path_info)
        else:                       
            if form.is_valid():                
                instance = form.save(commit=False)
                instance.reviewer = user
                instance.product = product
                if instance.score == 'UP':
                    product.upvote +=1
                    product.save()
                else:
                    product.downvote +=1
                    product.save()
                instance.save()                
                messages.success(request, 'Your review has been posted!')
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, 'Your review was not valid. Please, try again!')
                return HttpResponseRedirect(request.path_info)

    

    reviews = ProductReview.objects.filter(product=product).exists()
    series =  Product.objects.filter(series=product.series).all()

    context = {
        # We pass a separate, unbound ReviewForm in the contexts on GET, to avoid issues with anonymous users who lack an instance
        "form": ReviewForm,
        "product": product,
        "product_info": product_info,
        "reviews": reviews,
        "series": series,
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