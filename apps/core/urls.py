from django.urls import path, include
from .views.category.views import *
from .views.products.views import *
from .views.clients.views import *
from .views.sale.views import *

app_name = 'core'

urlpatterns = [
    # Category urls
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/edit/<int:pk>', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),

    # Product urls
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/edit/<int:pk>', ProductUpdateView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),

    # Clients urls
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

    # Sales urls
    path('sale/create/', SaleCreateView.as_view(), name='sale_create'),
]
