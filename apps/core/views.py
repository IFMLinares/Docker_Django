from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from apps.core.models import Category

class DashboardView(TemplateView):
    pass
    
dashboard_view = DashboardView.as_view(template_name="dashboards/index.html")

class CategoryListView(ListView):
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Listado de Categorias"
        return context