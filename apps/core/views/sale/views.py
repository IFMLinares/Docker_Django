# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Project-specific imports
from apps.core.models import Sale, Product
from apps.core.forms import SaleForm
from apps.core.mixings import ValidatePermissionMixin

class SaleCreateView(LoginRequiredMixin, ValidatePermissionMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "apps/sale/sale.html"
    context_object_name = 'objects'
    success_url = reverse_lazy('index')

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
        return context

