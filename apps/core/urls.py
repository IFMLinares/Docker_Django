from django.urls import path, include
from .views import *

app_name = 'core'

urlpatterns = [
    path('', dashboard_view, name='index'),
    path('category/list/', CategoryListView.as_view(), name='category_list'),
]