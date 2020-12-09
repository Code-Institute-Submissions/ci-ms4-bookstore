from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import NewsPost
from .forms import NewsForm

# Create your views here.

def index(request):
    form = NewsForm()
    # News post sorted by date, newer at the top, limited to five total items for the index page.
    newsposts = NewsPost.objects.order_by('-time', 'title')[:5]

    context = {
        'news': newsposts,
        'form': form,
    }

    return render(request, 'home/index.html', context)

def archive(request):
    # All items, sorted by date
    newsposts = NewsPost.objects.order_by('-time')
    form = NewsForm

    context = {
        'news': newsposts,
        'form': form
    }

    return render(request, 'home/archive.html', context)


"""

API options for managing news below.

add_post view:

Login required to access, otherwise redirects to login. 

delete_post view:

Login required, redirects on get and action only taken if request user is an admin.

edit_post view:

Editing current items already in the list.


"""

@login_required
def add_post(request):
    # View for adding new posts
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():

            #Instancing a new news-item.
            instance = form.save(commit=False) 
            instance.author = request.user
            form.save()
            messages.success(request, 'News item added!')
            return HttpResponseRedirect('/')

        else:
            messages.success(request, 'Invalid post, please check your form for validation errors!')
            return HttpResponseRedirect('/')

    # On get, return redirect to main page, with a message. 
    messages.warning(request, 'That URL is restricted!')
    return HttpResponseRedirect('/')


# Handling deleting news items.

@login_required
def delete_post(request, news_id):
    # View for deleting news items
    news_item = NewsPost.objects.filter(pk=news_id)
        
    if request.user.is_superuser:    
        news_item.delete()
        messages.success(request, 'Your post has been deleted.')
        return HttpResponseRedirect('/')
    else:
        messages.warning(request, 'This URL is restricted to Staff members, please login with your staff account.')
        return HttpResponseRedirect('/')

        

# Handling editing news items.

@login_required
def edit_post(request, news_id):    
    if request.method == 'POST':
        instance = get_object_or_404(NewsPost, pk=news_id)
        if request.user.is_superuser:
            form = NewsForm(request.POST, instance=instance)
            if form.is_valid():
                #Instancing the edited news-item.
                form.save()

                messages.success(request, 'News item updated!')
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, 'Form invalid, please check for errors.')
                return HttpResponseRedirect('/')

        else:
            messages.warning(request, 'This URL is restricted to Staff members, please login with your staff account.')
            return HttpResponseRedirect('/')

    else:
        messages.warning(request, 'This URL is restricted to Staff members, please login with your staff account.')
        return HttpResponseRedirect('/')

  