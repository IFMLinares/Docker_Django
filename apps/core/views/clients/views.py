# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Project-specific imports
from apps.core.models import Client
from apps.core.forms import ClientForm
from apps.core.mixings import ValidatePermissionMixin

class ClientListView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    model = Client
    template_name = "apps/client/list.html"
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Clientes"
        context['title'] = "Listado de Clientes"
        context['url_create'] = reverse_lazy('core:client_create')
        return context

class ClientCreateView(LoginRequiredMixin, ValidatePermissionMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "apps/generic/create.html"
    context_object_name = 'objects'
    success_url = reverse_lazy('core:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Clientes"
        context['title'] = "Registro de clientes"
        context['subtitle'] = "Formulario registro"
        context['url_create'] = reverse_lazy('core:client_list')
        return context

class ClientUpdateView(LoginRequiredMixin, ValidatePermissionMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "apps/generic/create.html"
    context_object_name = 'objects'
    success_url = reverse_lazy('core:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Clientes"
        context['title'] = "Actualización de clientes"
        context['subtitle'] = "Formulario de actualización"
        context['return_url'] = self.success_url
        return context
    
class ClientDeleteView(LoginRequiredMixin, ValidatePermissionMixin, DeleteView):
    model = Client
    template_name = "apps/categories/delete.html"
    success_url = reverse_lazy('core:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Clientes"
        context['title'] = "Eliminación de clientes"
        context['subtitle'] = "Formulario de eliminación"
        context['return_url'] = self.success_url
        return context
