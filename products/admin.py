from products.views import products
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Series)
admin.site.register(Product)