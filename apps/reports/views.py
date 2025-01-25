from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# Create your views here.
class ReportSaleView(TemplateView):
    template_name = 'apps/reports/sale/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Reportes"
        context['title'] = "Reporte de Ventas"
        context['url_create'] = reverse_lazy('report:sale_report')
        return context