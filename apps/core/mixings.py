from django.shortcuts import redirect


class isSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            print('Es superusuario')
            return super().dispatch(request, *args, **kwargs)
        print('No es superusuario')
        return redirect('index')