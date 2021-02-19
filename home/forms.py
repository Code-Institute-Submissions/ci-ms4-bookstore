# Forms for handling the news items on the main page and the user profile views
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
from .models import NewsPost, UserProfile


class NewsForm(ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'post']
        exclude = ("author", "time")
        labels = {
            'title': "Title",
            'post': 'Content'
        }
        widgets = {
            'title': widgets.Textarea(attrs={'cols': 50, 'rows': 1, 'class': 'form-control'}),
            'post': widgets.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('default_phone_number', 'default_street_address1', 'default_street_address2', 'default_town_or_city', 'default_county', 'default_postcode', 'default_country')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class MailForm(forms.Form):
    subject = forms.CharField(max_length=200, required=True, label="Subject: ")
    message = forms.CharField(max_length=200, required=True, label="Your message: ", widget=forms.Textarea())
    email = forms.EmailField(required=True, label="Your email")
