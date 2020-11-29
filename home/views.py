from django.shortcuts import render
from .models import NewsPost

# Create your views here.

def index(request):

    # News post sorted by date, newer at the top, limited to five total items
    newsposts = NewsPost.objects.order_by('-time', 'title')[:5]

    context = {
        'news': newsposts
    }

    return render(request, 'home/index.html', context)

def archive(request):

    # All items, sorted by date
    newsposts = NewsPost.objects.order_by('-time')

    context = {
        'news': newsposts
    }

    return render(request, 'home/archive.html', context)

    # API options for managing news below.

    