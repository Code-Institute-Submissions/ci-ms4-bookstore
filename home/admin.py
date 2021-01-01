from django.contrib import admin
from .models import NewsPost, UserProfile

# Register your models here.

admin.site.register(NewsPost)
admin.site.register(UserProfile)