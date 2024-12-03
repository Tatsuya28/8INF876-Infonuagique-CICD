from django.contrib import admin
from django.contrib.auth import login
from django.urls import path

from .views import add_task, task_list, edit_task, delete_task,register,login, logout

urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('edit/',edit_task, name='edit_task'),
    path('delete/',delete_task, name='delete_task'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
