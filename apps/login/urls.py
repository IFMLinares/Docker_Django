from django.urls import path, include
from .views import *

app_name = 'auth'

urlpatterns = [
    path('', LoginFormVIew.as_view(), name='login'),
    path('logout/', RedirectView.as_view(), name='logout'),
]