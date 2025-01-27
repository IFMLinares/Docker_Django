from datetime import datetime

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from apps.core.models import Sale

# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/homepage/index/index.html'


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'get_graph_sales_year_month':
                data = self.get__graph_sales_year_months()
        except Exception as e:
            pass
        return JsonResponse(data, safe=False)

    def get__graph_sales_year_months(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                    r=Coalesce(Sum('total'), 0, output_field=DecimalField())
                ).get('r')
                print(total)
                data.append(float(total))
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Panel administrador"
        context['title'] = "Inicio"
        context['graph_sales_year_months'] = self.get__graph_sales_year_months()
        return context