from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('change/group/<int:pk>/', UserChangeGroupView.as_view(), name='user_change_group'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
