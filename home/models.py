from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


# Add a news model, for blog-posts to display on the main page.

class NewsPost(models.Model):

    title = models.CharField(max_length=255)
    post = models.CharField(max_length=2500)
    time = models.DateField(auto_now=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)