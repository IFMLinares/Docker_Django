from django.shortcuts import render
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    pass
    
dashboard_view = DashboardView.as_view(template_name="dashboards/index.html")