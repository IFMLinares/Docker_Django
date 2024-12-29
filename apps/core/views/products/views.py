from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from apps.core.models import Product
from apps.core.forms import ProductForm

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "core/categories/list.html"
    context_object_name = "categories"

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
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "core/categories/create.html"
    success_url = reverse_lazy('core:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Productos"
        context['title'] = "Registro de Productos"
        context['subtitle'] = "Formulario de registro"
        return context

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "core/categories/create.html"
    success_url = reverse_lazy('core:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Productos"
        context['title'] = "Actualización de Productos"
        context['subtitle'] = "Formulario de actualización"
        return context

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "core/categories/delete.html"
    success_url = reverse_lazy('core:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Productos"
        context['title'] = "Eliminación de Productos"
        context['subtitle'] = "Formulario de eliminación"
        return context



