# Forms for handling the news items on the main page

from django.forms import ModelForm, Form
from .models import NewsPost


class NewsForm(ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'post']
        exclude = ("author", "time")
        labels = {
            'title': "Title",
            'post': 'Content'
        }
