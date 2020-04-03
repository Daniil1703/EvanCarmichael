from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Todo

# Create your views here.

def list_todo_items(request):
    todos = Todo.objects.all()
    return render(request, 'todos.html', context={'todos': todos})

def insert_todo_item(request:HttpResponse):
    todo = Todo(content = request.POST['content'])
    todo.save()
    return redirect('/todos/')

def delete_todo_item(request, todo_id):
    todos_delete = Todo.objects.get(id=todo_id)
    todos_delete.delete()
    return redirect('/todos')
