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
            content=f'Webhook received: {event["type"]}',
            status=200)



