from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import NewsPost
from .forms import NewsForm

# Create your views here.

def index(request):
    form = NewsForm()
    # News post sorted by date, newer at the top, limited to five total items
    newsposts = NewsPost.objects.order_by('-time', 'title')[:5]

    context = {
        'news': newsposts,
        'form': form,
    }

    return render(request, 'home/index.html', context)

def archive(request):
    # Form for posting new items
    form = NewsForm()
    # All items, sorted by date
    newsposts = NewsPost.objects.order_by('-time')

    context = {
        'news': newsposts,
        'form': form
    }

    return render(request, 'home/archive.html', context)


# API options for managing news below.

"""

Add view.

Login required to access, otherwise redirects to login.



"""

@login_required
def add_post(request):
    # View for adding new posts
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():

            #Instancing a new news-item

            instance = form.save(commit=False) 
            instance.author = request.user
            form.save()
            messages.success(request, 'News item added!')
            return HttpResponseRedirect('/')

        else:
            messages.success(request, 'Invalid post, only staff can add news items!')
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