from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Mixin para validar superusuario
class isSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            print('Es superusuario')
            return super().dispatch(request, *args, **kwargs)
        print('No es superusuario')
        return redirect('index')

# Mixin para validar permisos
class ValidatePermissionMixin(object):
    permission_required = None
    url_redirect = None

    # Método para obtener los permisos, si es un string lo convierte en tupla
    def get_perms(self):
        if isinstance(self.permission_required, str):
            return (self.permission_required, )
        return self.permission_required

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('index')
        return self.url_redirect

    # Método para validar permisos
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_url_redirect())