from django.urls import path

from webapp.views import index, create_todo, todo_detail, todo_delete, todo_update

urlpatterns = [
    path('', index, name='todo'),
    path('create/', create_todo, name='todo_create'),
    path('todo/<int:pk>/', todo_detail, name="todo_detail"),
    path('article/<int:pk>/update/', todo_update, name='todo_update'),
    path('delete/<int:pk>/', todo_delete, name="todo_delete"),
]
