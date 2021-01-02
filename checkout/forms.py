from django import forms
from django.core.exceptions import RequestDataTooBig
from django.forms import fields
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county')
    def __init__(self, *args, **kwargs):
        """
        Adding the values of the fields that are assigned automatically
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': "Full Name",
              'email': "Email Address", 
              'phone_number': "Phone Number", 
              'country': "Country",
              'postcode': "Postal Code", 
              'town_or_city': "Town or City", 
              'street_address1': "Street address 1",
              'street_address2': "Street address 2", 
              'county': "County"

        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} * (Required)'
                else: 
                    placeholder = f'{placeholders[field]} * (Required)'
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-input-styles'
                self.fields[field].widget.attrs['label'] = False