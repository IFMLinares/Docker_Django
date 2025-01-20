# forms code
from django.forms import *
from .models import Category, Product, Client, Sale

from .choices import gender_choices

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

class ClientForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['names'].widget.attrs.update({
            'autofocus': 'autofocus',
            'class': 'form-control col-md-6'
        })
        self.fields['surnames'].widget.attrs.update({
            'class': 'form-control col-md-6'
        })

    class Meta:
        model = Client
        fields = ['names', 'surnames', 'dni', 'date_birthday', 'address', 'gender']
        labels = {
            'names': 'Nombre',
            'surnames': 'Apellidos',
            'dni': 'Identificación',
            'date_birthday': 'Fecha de nacimiento',
            'address': 'Dirección',
            'gender': 'Género',
        }
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del cliente',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos del cliente',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese la identificación del cliente',
                }
            ),
            'date_birthday': DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese la dirección del cliente',
                }
            ),
            'gender': Select(
                choices=gender_choices,
                attrs={
                    'placeholder': 'Seleccione el género del cliente',
                }
            ),
        }

class SaleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control bg-light border-0',
                'autocomplete': 'off'
            })

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'autofocus': True,
                'class': 'form-control',
                'data-choices': '',
                'data-choices-search-false': '',
                'data-choices-removeItem': '',
                }
            ),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'date-field',
                    'data-provider': 'flatpickr',
                    'data-time': 'true',
                    'placeholder': 'Select Date-time',
                }
            ),
            'subtotal': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control bg-light border-0',
                }
            ),
            'total': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control bg-light border-0',
                }
            ),
        }


