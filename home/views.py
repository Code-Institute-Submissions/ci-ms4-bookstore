from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import NewsPost, UserProfile
from .forms import NewsForm, ProfileForm, UserForm, MailForm
from products.models import Product
from checkout.models import Order

# Create your views here.

def index(request):
    form = NewsForm()
    # News post sorted by date, newer at the top, limited to five total items for the index page.
    newsposts = NewsPost.objects.order_by('-time', 'title')[:5]
    feature = Product.objects.filter(featured=True)[:5]
    context = {
        'news': newsposts,
        'form': form,
        'feature': feature,
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

@login_required
def user_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user_id=user)
    orders = Order.objects.filter(user_id=profile).order_by('-date')
    form = ProfileForm(instance=profile)
    user_form = UserForm(instance=user )

    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        user_form = UserForm(instance=user, data=request.POST )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
        else:
            messages.warning(request, 'Your form was rejected as invalid! Please, try again.')

        if user_form.is_valid():
            messages.success(request, 'Your user-information has been updated!')
            user_form.save()
        else:
            messages.warning(request, 'Your form was rejected as invalid! Please, try again.')
    
    context = {
        'user': user,
        'profile': profile,
        'form':form,
        'user_form': user_form,
        'orders': orders,
    }

    return render(request, 'home/profile.html', context)


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

""" 

  Email API for handling contact-emails

"""

def contact_mailer(request):
      if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():            
            subject = render_to_string('home/custom_email/contact_email_subject.txt', {'subject': form.cleaned_data['subject']})
            message = render_to_string('home/custom_email/contact_email_body.txt', {'message': form.cleaned_data['message'], 'email': form.cleaned_data['email']})

            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['bibliomania@patrikaxelsson.one'])
            except BadHeaderError:
                messages.warning(request, 'An error occured. Please try again')
            
            messages.success(request, 'Your mail has been sent!')
            return HttpResponseRedirect('/')