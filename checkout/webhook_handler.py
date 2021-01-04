from django.http import HttpResponse
from django.http import request

class StripeWebhook_Handler:


    def __init__():
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
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_pi_failed(self, event):
        """
        Handles ppayment_intent.payment_failed from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

        