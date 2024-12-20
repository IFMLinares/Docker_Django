from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from apps.core.models import Category
from apps.core.forms import CategoryForm

class DashboardView(TemplateView):
    pass
    
dashboard_view = DashboardView.as_view(template_name="dashboards/index.html")

class CategoryListView(ListView):
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"

    # Método dispath para requerir autenticación
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.to_json())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}  # Asegúrate de que data sea un diccionario en caso de error
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Listado de Categorias"
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/create.html"
    success_url = reverse_lazy('core:category_list')

    # def post(self, request, *args, **kwargs):
    #     form = CategoryForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return render(request, self.template_name, context)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Registro de Categorias"
        context['subtitle'] = "Formulario de registro"
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/create.html"
    success_url = reverse_lazy('core:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Actualización de Categorias"
        context['subtitle'] = "Formulario de actualización"
        return context
    
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "categories/delete.html"
    success_url = reverse_lazy('core:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = "Categorias"
        context['title'] = "Eliminación de Categorias"
        context['subtitle'] = "Formulario de eliminación"
        return context



