from django.urls import path, include
from .views import *


app_name = 'report'

urlpatterns = [
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
]
