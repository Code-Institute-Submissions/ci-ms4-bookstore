from django.http import request
from django.views.decorators.http import require_POST
from bookstore.settings import STRIPE_CURRENCY, STRIPE_PUBLIC_KEY
from django.shortcuts import ( 
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.contrib import messages
from django.conf import settings 
from .models import OrderItem, Order
from home.models import UserProfile
from home.forms import ProfileForm
from products.models import Product
from .forms import OrderForm
from home.forms import MailForm
from bag.contexts import bag_items
import stripe
import json
# Create your views here.

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    extra_title = "- Checkout!"

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_item = OrderItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                        order_item.save()        
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't "
                        "found in our database. "
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))

    else:
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user_id=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user_id.get_full_name(),
                    'email': profile.user_id.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        current_bag = bag_items(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )
    
    if not bag_items:
            messages.error(request,
            "Your shopping bag is empty, so you cannot visit checkout!")
            return redirect(reverse('products'))

    context = {
        'mail_form': MailForm,
        "form": order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'extra_title': extra_title,
    }

    return render(request, 'checkout.html', context)

def checkout_success(request, order_id):
    save_info = request.session.get('save_info')
    order_id = get_object_or_404(Order, order_number=order_id)
    order_items = OrderItem.objects.filter(order=order_id)
    extra_title = "- Order placed!"

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=request.user)
        # Attach the user's profile to the order
        order_id.user_id = profile
        order_id.save()

        # Save the user's info, if the checkbox is ticked in checkout
        if save_info:
            profile_data = {
                'default_phone_number': order_id.phone_number,
                'default_country': order_id.country,
                'default_postcode': order_id.postcode,
                'default_town_or_city': order_id.town_or_city,
                'default_street_address1': order_id.street_address1,
                'default_street_address2': order_id.street_address2,
                'default_county': order_id.county,
            }
            user_profile_form = ProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
                
    del request.session['bag']     
    context = {
        "order": order_id,
        "order_items":order_items,
        'extra_title': extra_title
    }

    return render(request, 'checkout_success.html', context)