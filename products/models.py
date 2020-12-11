from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


# The following models will help users and admins organize the collections of books.

class Genre(models.Model):
    title = models.CharField(max_length=200, default="Genre title")
    desc = models.CharField(max_length=200, default="Genre description")

    def __str__(self):
        return self.title

# A class for series of books, often requiring them to be read in order.

class Series(models.Model):

    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)

    def __str__(self):
        return self.title

# Specific authors can be tagged with multiple genres and multiple series.
class Author(models.Model):
    name = models.CharField(max_length=100)
    summary = models.CharField(max_length=500, default="We currently have no information on this authors work! Get in the comments and inform us!")
    series = models.ForeignKey(Series, null=True, blank=True, on_delete=models.SET_NULL)
    genres = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

"""
 The books themselves. Note that all foreign keys are set to set null on delete because while we don't want dangling references in the DB, neither do we want 
 products to be invalidated and removed from the store when administering many-to-many relationships.
"""

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    cover = models.ImageField(upload_to='covers', null=True, blank=True) 
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    series = models.ForeignKey(Series, null=True, blank=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)
    featured = models.BooleanField(default=False)
    price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title

# Class for product reviews, tied to both user and 

class ProductReview(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    plus = models.IntegerField()
    minus = models.IntegerField()