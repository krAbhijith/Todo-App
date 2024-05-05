from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView

from manage_todo.models import Todo

class Index(View):
    
    def get(self, request, *args, **kwargs):
        context = Todo.objects.all().order_by('-pk')
        today = datetime.today().date()
        return render(request, 'manage_todo/index.html', context={'todos' : context, 'today' : today})
    
class CreateTodo(View):
    def post(self, request):
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        date_expire = request.POST.get('date_expire')
        priority = request.POST.get('priority')
        Todo.objects.create(title=title, desc=desc, date_expire=date_expire, priority=priority, user=self.request.user)
        return redirect('index')
    
class UpdateTodo(View):
    def get(self, request, *args, **kwargs):
        context = Todo.objects.all().order_by('-pk')
        edit = Todo.objects.get(pk=kwargs.get('pk'))
        today = datetime.today().date()
        return render(request, 'manage_todo/index.html', context={
            "todos" : context,
            'edit' : edit,
            'today' : today,
        })
    
    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        todo = get_object_or_404(Todo, pk=pk)
        todo.title = request.POST.get('title')
        todo.desc = request.POST.get('desc')
        todo.date_expire = request.POST.get('date_expire')
        todo.priority = request.POST.get('priority')
        todo.save()
        return redirect('index')
    
class DeleteTodo(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        get_object_or_404(Todo, pk=pk).delete()
        return redirect('index')
    
class CompleteToggle(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        todo = get_object_or_404(Todo, pk=pk)
        todo.is_completed = not todo.is_completed
        todo.save()
        return redirect('index')

