# Django imports
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Project-specific imports
from apps.core.models import Sale, Product, DetSale
from apps.core.forms import SaleForm
from apps.core.mixings import ValidatePermissionMixin

class SaleListView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    model = Sale
    template_name = "apps/sale/list.html"
    context_object_name = 'objects'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Ventas"
        context['title'] = "Listado de Ventas"
        context['url_create'] = reverse_lazy('core:sale_create')
        return context

class SaleCreateView(LoginRequiredMixin, ValidatePermissionMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "apps/sale/sale.html"
    context_object_name = 'objects'
    success_url = reverse_lazy('core:sale_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    # llamamos al método toJson que creamos en el modelo (que trae todos los datos incluyendo las llaves foraneas)
                    item = i.toJson()
                    item['text'] = i.name
                    item['quantity'] = 1
                    item['subtotal'] = 0.00
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])

                    sale.save()
                    print(vents)
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['quantity'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No se ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Ventas"
        context['title'] = "Registro de Ventas"
        context['subtitle'] = "Formulario registro"
        context['url_create'] = reverse_lazy('core:client_list')
        context['action'] = 'add'
        return context

class SaleDeleteView(LoginRequiredMixin, ValidatePermissionMixin, DeleteView):
    model = Sale
    template_name = "apps/categories/delete.html"
    success_url = reverse_lazy('core:sale_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Ventas"
        context['title'] = "Eliminación de Ventas"
        context['subtitle'] = "Formulario de eliminación"
        context['return_url'] = self.success_url
        return context



