from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.core.models import Client
from apps.core.forms import ClientForm

class ClientListView(ListView):
    model = Client
    template_name = "apps/client/list.html"
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Clientes"
        context['title'] = "Listado de Clientes"
        context['url_create'] = reverse_lazy('core:client_create')
        return context

class ClientCreateView(CreateView):
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

class ClientUpdateView(UpdateView):
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
