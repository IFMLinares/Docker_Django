from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group

from crum import get_current_request

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
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms
    
        # if self.permission_required is None:
        #     return ()
        # if isinstance(self.permission_required, str):
        #     return (self.permission_required, )
        # return self.permission_required

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('index')
        return self.url_redirect

    # Método para validar permisos
    def dispatch(self, request, *args, **kwargs):
        # Si el usuario tiene los permisos necesarios, se le permite el acceso
        # de lo contrario se le redirige a la página de inicio
        request = get_current_request()

        # Si es superusuario, se le permite el acceso
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        # Si no se ha definido un permiso, se le permite el acceso
        if self.permission_required is None:
            return super().dispatch(request, *args, **kwargs)
        
        # Validamos si el usuario tiene un grupo asignado
        if 'group' in request.session:
            # Obtenemos el grupo
            group = Group.objects.get(pk=request.session['group'])
            # Llamamos al método get_perms para obtener los permisos
            perms = self.get_perms()
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tienes permisos para ingresar a este módulo')
                    return HttpResponseRedirect(self.get_url_redirect())
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())