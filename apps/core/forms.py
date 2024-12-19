# forms code
from django.forms import *
from .models import Category

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