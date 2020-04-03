from django.urls import path, include

from . import views


app_name = 'todos'

urlpatterns = [
    path('todos/', include([
        path('', views.list_todo_items, name='list_todo_items'),
        path('insert_todo/', views.insert_todo_item, name='insert_todo_item'),
        path('delete_todo/<int:todo_id>/', views.delete_todo_item, name='delete_todo_item'),
    ])),
]
