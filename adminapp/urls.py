
from django.urls import path

from adminapp.views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView

app_name = 'adminapp'

urlpatterns = [
    path('', index, name='index'),
    path('admin-users-read/', UserListView.as_view(), name='admin_users_read'),
    path('admin-users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('admin-users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('admin-users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
]