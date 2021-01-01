from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


# Add a news model, for blog-posts to display on the main page.

class NewsPost(models.Model):

    title = models.CharField(max_length=255)
    post = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL) # Changed to save all news-posts in case of staff changes

# Adds a userprofile object for each user, on account creation. 

class UserProfile(models.Model):
    # user_id is the OneToOne link between the user account and the profile. Cascades on deletion.
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20,
                                            null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80,
                                               null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80,
                                               null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40,
                                            null=True, blank=True)
    default_county = models.CharField(max_length=80,
                                      null=True, blank=True)
    default_postcode = models.CharField(max_length=20,
                                        null=True, blank=True)
    default_country = CountryField(blank_label='Country',
                                   null=True, blank=True)

    def __str__(self):
        return self.user_id.username

#Using Django signals to ensure there's always a linked profile object to every user account.

@receiver(post_save, sender=User)
def profile_handler (sender, instance, created, **kwargs):
    

    if created:
        UserProfile.objects.create(user_id=instance)
    # Existing users: just save the profile
    instance.userprofile.save()