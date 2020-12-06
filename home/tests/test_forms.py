import random, string
from django.contrib.auth.models import User
from django.test import TestCase
from home.forms import NewsForm

# Create your tests here.

class NewsForm(TestCase):
    def empty_form_test(self):
        form = NewsForm()        
        form.title = ''
        form.post = ''
        form.save()

        self.assertFalse(form.is_valid())
        self.assertIn('post', form.errors.keys())
        self.assertIn('title', form.errors.keys())          
    
    # Strings above 500 characters fail both tests. Strings above 255 are invalid length for titles.

    def max_characters_test(self):
            
        letters = string.ascii_lowercase
        max_length_string = ''.join(random.choice(letters) for i in range(500))
        form = NewsForm(self)


        form.post = max_length_string
        form.title = max_length_string
        form.save()

        self.assertFalse(form.is_valid())
        self.assertIn('post', form.errors.keys())
        self.assertIn('title', form.errors.keys())

    # A post that contains no valid foreign key is not valid.
    def invalid_fk_user_test(self):
        user = User.object.models({'pk': 'xx-xx-xx-xx'})

        form = NewsForm(self)
        
        form.author = user
        form.save()

        self.assertFalse(form.is_valid())