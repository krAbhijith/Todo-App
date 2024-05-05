from django.urls import path

from manage_todo.views import *

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('create/', CreateTodo.as_view(), name='todo-create'),
    path('update/<int:pk>/', UpdateTodo.as_view(), name='todo-update')
]
