from django.shortcuts import render
from .models import NewsPost

# Create your views here.

def index(request):

    newsposts = NewsPost.objects.all()

    context = {
        'news': newsposts
    }


    return render(request, 'home/index.html', context)