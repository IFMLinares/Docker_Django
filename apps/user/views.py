from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView
# Create your views here.
from apps.user.models import User
from apps.user.forms import UserForm, UserProfileForm
from apps.core.mixings import ValidatePermissionMixin
from apps.mixings import FormMessagesMixin
from django.forms import CharField, HiddenInput

# Vista para listar los usuarios
class UserListView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    model = User
    template_name = "apps/user/list.html"
    context_object_name = "objects"

    # Método dispath para requerir autenticación
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    data.append(i.to_json())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}  # Asegúrate de que data sea un diccionario en caso de error
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Usuario"
        context['title'] = "Listado de Usuarios"
        context['url_create'] = reverse_lazy('user:user_create')
        return context

# Vista para crear un usuario 
class UserCreateView(LoginRequiredMixin, ValidatePermissionMixin,FormMessagesMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "apps/generic/create_image.html"
    success_url = reverse_lazy('user:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Usuarios"
        context['title'] = "Registro de usuarios"
        context['subtitle'] = "Formulario de registro"
        context['return_url'] = self.success_url
        return context

# Vista para actualizar un usuario
class UserUpdate(LoginRequiredMixin, ValidatePermissionMixin,FormMessagesMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "apps/generic/create_image.html"
    success_url = reverse_lazy('user:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Usuarios"
        context['title'] = "Actualización de usuarios"
        context['subtitle'] = "Formulario de actualización"
        context['return_url'] = self.success_url
        return context

# Vista para eliminar un usuario
class UserDeleteView(LoginRequiredMixin, ValidatePermissionMixin,FormMessagesMixin, DeleteView):
    model = User
    template_name = "apps/categories/delete.html"
    success_url = reverse_lazy('user:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Usuarios"
        context['title'] = "Eliminación de usuarios"
        context['subtitle'] = "Formulario de eliminación"
        context['return_url'] = self.success_url
        return context

#  Vista para Actualizar el usuario
class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "apps/generic/create_image.html"
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Usuario"
        context['title'] = "Edición de perfil"
        context['subtitle'] = "Formulario de edición"
        context['return_url'] = self.success_url
        return context

#  Vista para Actualizar el usuario
class UserChangePassword(LoginRequiredMixin, ValidatePermissionMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = "apps/generic/create.html"
    success_url = reverse_lazy('auth:login')

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        self.update_form_widgets(form)
        return form

    def update_form_widgets(self, form):
        for field in form.fields:
            form.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        form.fields['old_password'].widget.attrs.update({
            'autofocus': 'autofocus',
            'placeholder': 'Ingrese su contraseña actual',
        })
        form.fields['new_password1'].widget.attrs.update({
            'placeholder': 'Ingrese su nueva contraseña'
        })
        form.fields['new_password2'].widget.attrs.update({
            'placeholder': 'Repita su nueva contraseña'
        })

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return super().post(request, *args, **kwargs)
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
            self.update_form_widgets(form)  # Asegúrate de actualizar los widgets aquí también
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Usuario"
        context['title'] = "Edición de contraseña"
        context['subtitle'] = "Formulario de edición"
        context['return_url'] = self.success_url
        return context

# Vista para cambiar de grupo
class UserChangeGroupView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = kwargs['pk']
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('index'))