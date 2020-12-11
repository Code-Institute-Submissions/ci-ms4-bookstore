from django.db.models.base import Model
from django.forms import ModelForm, widgets, ImageField, Textarea
from django.forms.models import modelform_factory
from .models import Product, Author, Genre, Series

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ("__all__")
        verbose_name_plural = 'Products'
        widgets = {'description': Textarea,
        'class': 'form-control'
        }
        image = ImageField(label='Cover',
                             required=False,
                            )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(size='40')

# Other subforms, for the dashboard.

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)

class SeriesForm(ModelForm):
    class Meta:
        model  = Series
        fields = ("__all__")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AuthorForm(ModelForm):
    class Meta:
        model = Genre
        fields = ("__all__")
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)