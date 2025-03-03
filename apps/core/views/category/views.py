# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Project-specific imports
from apps.core.models import Category
from apps.core.forms import CategoryForm
from apps.core.mixings import ValidatePermissionMixin
from apps.mixings import FormMessagesMixin

class CategoryListView(LoginRequiredMixin,ValidatePermissionMixin, ListView):
    model = Category
    template_name = "apps/categories/list.html"
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
                for i in Category.objects.all():
                    data.append(i.to_json())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}  # Asegúrate de que data sea un diccionario en caso de error
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Listado de Categorias"
        context['url_create'] = reverse_lazy('core:category_create')
        return context

class CategoryCreateView(LoginRequiredMixin,ValidatePermissionMixin, FormMessagesMixin, CreateView ):
    model = Category
    form_class = CategoryForm
    template_name = "apps/generic/create.html"
    success_url = reverse_lazy('core:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Registro de Categorias"
        context['subtitle'] = "Formulario de registro"
        context['return_url'] = self.success_url
        return context

class CategoryUpdateView(LoginRequiredMixin,ValidatePermissionMixin, FormMessagesMixin, UpdateView ):
    model = Category
    form_class = CategoryForm
    template_name = "apps/generic/create.html"
    success_url = reverse_lazy('core:category_list')
    type_operation = 'update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Actualización de Categorias"
        context['subtitle'] = "Formulario de actualización"
        context['return_url'] = self.success_url
        return context

class CategoryDeleteView(LoginRequiredMixin,ValidatePermissionMixin, FormMessagesMixin, DeleteView ):
    model = Category
    template_name = "apps/categories/delete.html"
    success_url = reverse_lazy('core:category_list')
    type_operation = 'delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Eliminación de Categorias"
        context['subtitle'] = "Formulario de eliminación"
        context['return_url'] = self.success_url
        return context



