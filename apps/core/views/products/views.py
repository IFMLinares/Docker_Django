# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Project-specific imports
from apps.core.models import Product
from apps.core.forms import ProductForm
from apps.core.mixings import ValidatePermissionMixin
from apps.mixings import FormMessagesMixin

class ProductListView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    model = Product
    template_name = "apps/products/list.html"
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
                for i in Product.objects.all():
                    data.append(i.to_json())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}  # Asegúrate de que data sea un diccionario en caso de error
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Productos"
        context['title'] = "Listado de Productos"
        context['url_create'] = reverse_lazy('core:product_create')
        return context

class ProductCreateView(LoginRequiredMixin, ValidatePermissionMixin, FormMessagesMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "apps/generic/create_image.html"
    success_url = reverse_lazy('core:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Productos"
        context['title'] = "Registro de Productos"
        context['subtitle'] = "Formulario de registro"
        context['return_url'] = self.success_url
        return context

class ProductUpdateView(LoginRequiredMixin, ValidatePermissionMixin, FormMessagesMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "apps/generic/create_image.html"
    success_url = reverse_lazy('core:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Productos"
        context['title'] = "Actualización de Productos"
        context['subtitle'] = "Formulario de actualización"
        context['return_url'] = self.success_url
        return context

class ProductDeleteView(LoginRequiredMixin, ValidatePermissionMixin, FormMessagesMixin, DeleteView):
    model = Product
    template_name = "apps/categories/delete.html"
    success_url = reverse_lazy('core:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Productos"
        context['title'] = "Eliminación de Productos"
        context['subtitle'] = "Formulario de eliminación"
        context['return_url'] = self.success_url
        return context



