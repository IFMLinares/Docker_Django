# forms code
from django.forms import *
from .models import User


class UserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['first_name'].widget.attrs.update({
            'autofocus': 'autofocus'
        })

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'email', 'password', 'image'
        exclude = ['groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'is_active']
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'required',
                    }
                ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    }
                ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus username',
                    }
                ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                    }
                ),
            'password': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su contraseña',
                    }
                ),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user