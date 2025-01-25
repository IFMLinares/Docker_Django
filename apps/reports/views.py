from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# local imports
from apps.core.models import Sale
from .forms import ReportForm

# Create your views here.
class ReportSaleView(TemplateView):
    template_name = 'apps/reports/sale/report.html'

    
    # Método dispath para requerir autenticación
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            search = Sale.objects.all()
            if len(start_date) and len(end_date):
                search = search.filter(date_joined__range=[start_date, end_date])
            for s in search:
                data.append([
                    s.id,
                    s.cli.names,
                    s.date_joined.strftime('%Y-%m-%d'),
                    format(s.subtotal, '.2f'),
                    format(s.iva, '.2f'),
                    format(s.total, '.2f'),
                ])

            subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
            iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
            total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
            data.append([
                '---',
                '---',
                '---',
                format(subtotal, '.2f'),
                format(iva, '.2f'),
                format(total, '.2f'),
            ])
        except Exception as e:
            pass
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Reportes"
        context['title'] = "Reporte de Ventas"
        context['url_create'] = reverse_lazy('report:sale_report')
        context['form'] = ReportForm()
        return context