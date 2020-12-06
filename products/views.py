from django.shortcuts import render

# Create your views here.


def products(request):
    form = NewsForm()
    # Products view


    return render(request, 'home/index.html', context)