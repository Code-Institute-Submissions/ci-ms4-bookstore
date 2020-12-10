from django.forms import ModelForm, widgets, ImageField
from .models import Product, Author, Genre, Series

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ("__all__")
        verbose_name_plural = 'Products'
        image = ImageField(label='Cover',
                             required=False,
                            )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
