from bookstore.settings import STRIPE_CURRENCY, STRIPE_PUBLIC_KEY
from django.shortcuts import render
from django.conf import settings 
from .forms import OrderForm
from bag.contexts import bag_items
import stripe
# Create your views here.

def checkout(request):   
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    form = OrderForm
    current_bag = bag_items(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )
    print(intent)
    if not bag_items:
            messages.error(request,
                    "Your shopping bag is empty, so you cannot visit checkout!")
            return redirect(reverse('products'))

    context = {
        "form": form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout.html', context)