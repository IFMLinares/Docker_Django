# Django imports
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Third-party imports
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

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

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(self.request.POST)
            if action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJson())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return JsonResponse(data, safe=False)

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
                    data = {'id': sale.id}
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
        context['det'] = []
        return context

class SaleUpdateView(LoginRequiredMixin, ValidatePermissionMixin, UpdateView):
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
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale.objects.get(pk=self.get_object().id)
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete()
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

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJson()
                item['quantity'] = i.cant
                data.append(item)
        except Exception as e:
            pass

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Ventas"
        context['title'] = "Actualización de Ventas"
        context['subtitle'] = "Formulario registro"
        context['url_create'] = reverse_lazy('core:client_list')
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
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

class SaleInvocePdfView(View):

    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT
        
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception(
                'media uri must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('apps/sale/invoice.html')
            context = {
                # title con nro de venta
                'title': 'Venta nro. #{}'.format(self.kwargs['pk']),
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Sistema de Ventas', 'ruc': '', 'address': 'Av. Siempre Viva'},
                'icon': '{}{}'.format(settings.STATIC_URL , 'images/logo-dark.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback= self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('core:sale_list'))

