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
        self.fields['groups'].widget.attrs.update({
            'class': 'select2'
        })

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'email', 'password', 'groups', 'image'
        exclude = [ 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'is_active']
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
                render_value=True,
                attrs={
                    'placeholder': 'Ingrese su contraseña',
                    }
                ),
            'groups': SelectMultiple(
                attrs={
                    'style': 'width: 100%',
                    'multiple': 'multiple',
                    }
                ),
        }

    def save(self, commit=True):
        try:
            if self.is_valid():
                pwd = self.cleaned_data['password']
                u = super(UserForm, self).save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                if commit:
                    u.save()

                for g in self.cleaned_data['groups']:
                    u.groups.add(g)

                return u
            else:
                raise ValueError(self.errors)
        except Exception as e:
            raise e