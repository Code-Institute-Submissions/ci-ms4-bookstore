from django.http import HttpResponse
from django.http import request
from .models import Order, OrderItem
from products.models import Product
from home.models import UserProfile

import json
import time

class StripeWebhook_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Generic webhook handler
        """ 
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_pi_succeeded(self, event):
        """
        Handles payment_intent.succeeded from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.data.charges[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Profile update handler
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user_id__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()
            
        order_exists = False
        attempt = 1
        #Conditional try-block to make sure we do not overload the server nor create duplicate orders. 
        while attempt <= 5:
            try: 
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name, 
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.country,
                    postcode__iexact=shipping_details.postcode,
                    town_or_city__iexact=shipping_details.city,
                    street_address1__iexact=shipping_details.line1,
                    street_address2__iexact=shipping_details.line2,
                    county__iexact=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                    grand_total=grand_total
                )
                order_exists = True
                break
            except Order.DoesNotExist: 
                attempt += 1
                time.sleep(1)
                
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified order already in database'),
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    user_id = profile,
                    full_name=shipping_details.address.name, 
                    email=billing_details.email,
                    phone_number=shipping_details.address.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postcode,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                    grand_total=grand_total
                )

            
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_pi_failed(self, event):
        """
        Handles payment_intent.payment_failed from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

        