from products.models import *
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import AuthorForm, GenreForm, ProductForm, ReviewForm, SeriesForm
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView 
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    # Unlike the others, paginate has a set starting value of 10 to fall back on.
    paginate = 10
    

    """
    Search handler

    """

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            filter = request.GET['filter']
            if not query:
                messages.error(request, "You didn't enter any search criteria! Please specify what to search for.")
                return redirect(reverse('products'))
            else: 
                if filter == 'Genre':
                    filter = 'genre'
                elif filter == 'Author':
                    filter = 'author'
                elif filter == 'Series':
                    filter = 'series'
                else:
                    filter = 'title'
                queries = Q(title__icontains=query) | Q(description__icontains=query) | Q(author__name__icontains=query) | Q(series__title__icontains=query) | Q(genre__title__icontains=query)
                products = products.filter(queries).order_by(filter)
                
                if 'paginate' in request.GET:
                    paginate = int(request.GET['paginate'])


    # Feature grabs the first 5 objects that match as featured, so the main page is not inundated.
    feature = Product.objects.filter(featured=True)[:5]
    
    paginator = Paginator(products, paginate)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.get_page(1)

    context = {
        "products": page_obj,
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

    reviews = ProductReview.objects.filter(product=product).all()
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
    'product_form': ProductForm,
    'author_form': AuthorForm,
    'genre_form': GenreForm,
    'series_form': SeriesForm
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


""" 

Generic endpoints for handling form-validation, as well as class-based standard-views providing a FrontEnd layer for staffmembers to edit the forms.

"""

class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

def add_author(request):
    form = AuthorForm
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            messages.success(request, 'New author added succesfully!')
            form.save()
            return redirect('dashboard')
        else: 
            messages.warning(request, 'Author not saved, form invalid!')
            return redirect('dashboard')

    return redirect('dashboard')


def add_genre(request):
    form = GenreForm
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            messages.success(request, 'New genre added succesfully!')
            form.save()
            return redirect('dashboard')
        else: 
            messages.warning(request, 'Genre not saved, form invalid!')
            return redirect('dashboard')

    return redirect('dashboard')

def add_series(request):
    form = SeriesForm
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            messages.success(request, 'New series added succesfully!')
            form.save()
            return redirect('dashboard')
        else: 
            messages.warning(request, 'Series not saved, form invalid!')
            return redirect('dashboard')

    return redirect('dashboard')

class ProductListView(ListView, AdminStaffRequiredMixin):

    model = Product
    ordering = ['-author']
    paginate_by = 50

    def handle_no_permission(self):
        print("Not allowed!")
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProductView(UpdateView, AdminStaffRequiredMixin):
    model = Product
    fields = ['title', 'description', 'cover', 'author', 'series', 'genre', 'featured', 'price']
    template_name_suffix = '_update_form'

class EditGenreView(UpdateView, AdminStaffRequiredMixin):
    model = Genre
    fields = ['title', 'desc']
    template_name_suffix = '_update_form'

class EditSeriesView(UpdateView, AdminStaffRequiredMixin):
    model = Series
    fields = ['title', 'summary']
    template_name_suffix = '_update_form'

class EditAuthorView(UpdateView, AdminStaffRequiredMixin):
    model = Author
    fields = ['name', 'summary', 'series', 'genres']
    template_name_suffix = '_update_form'

class DeleteAuthorView(DeleteView, AdminStaffRequiredMixin):
    model = Author
    success_url = reverse_lazy('product-list')

class DeleteGenreView(DeleteView, AdminStaffRequiredMixin):
    model = Genre
    success_url = reverse_lazy('product-list')

class DeleteSeriesView(DeleteView, AdminStaffRequiredMixin):
    model = Series
    success_url = reverse_lazy('product-list')