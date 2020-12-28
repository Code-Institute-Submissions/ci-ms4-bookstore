from django.db.models.base import Model, ModelBase
from django.forms import ModelForm, widgets, ImageField, Textarea, RadioSelect
from django.forms.models import modelform_factory
from .models import Product, Author, Genre, ProductReview, Series

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ("__all__")
        verbose_name_plural = 'Products'
        widgets = {'description': Textarea,
        'class': 'form-control'
        }
        image = ImageField(label='Cover',
                            required=True)

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

# Product reviews

class ReviewForm(ModelForm):
    class Meta:
        model = ProductReview        
        fields = ("score", "comment")
        exclude = ("product", "reviewer")
        verbose_name_plural = 'Reviews'
        widgets = {'score': RadioSelect}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)