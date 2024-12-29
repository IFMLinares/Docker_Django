# forms code
from django.forms import *
from .models import Category, Product

class CategoryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['name'].widget.attrs.update({
            'autofocus': 'autofocus'
        })

    class Meta:
        model = Category
        fields = ['name', 'desc']
        labels = {
            'name': 'Nombre',
            'desc': 'Descripción'
        }
        exclude = ['created_at', 'updated_at']
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre de la categoría',
                    }
                ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripción de la categoría',
                    'rows': 3,
                    'cols': 3
                    }
                ),
                
        }

class ProductForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['name'].widget.attrs.update({
            'autofocus': 'autofocus'
        })

    class Meta:
        model = Product
        fields = ['name', 'cate', 'image', 'pvp']
        labels = {
            'name': 'Nombre',
            'cate': 'Categoría',
            'image': 'Imagen',
            'pvp': 'Precio de venta'
        }
        exclude = []
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del producto',
                }
            ),
            'cate': Select(
                attrs={
                    'placeholder': 'Seleccione la categoría del producto',
                }
            ),
            'image': FileInput(
                attrs={
                    'placeholder': 'Seleccione la imagen del producto',
                }
            ),
            'pvp': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el precio de venta del producto',
                }
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if not image:
            return self.instance.image
        return image
