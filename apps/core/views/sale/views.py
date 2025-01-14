# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Project-specific imports
from apps.core.models import Sale
from apps.core.forms import SaleForm
from apps.core.mixings import ValidatePermissionMixin

class SaleCreateView(LoginRequiredMixin, ValidatePermissionMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "apps/sale/sale.html"
    context_object_name = 'objects'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Ventas"
        context['title'] = "Registro de Ventas"
        context['subtitle'] = "Formulario registro"
        context['url_create'] = reverse_lazy('core:client_list')
        return context

