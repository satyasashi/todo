from django.urls import path
from . import views as myapp_views

urlpatterns = [
    path('', myapp_views.home, name="home"),
    path('todo/new', myapp_views.todo_add, name="todo-add"),
    path('todo/complete/<int:pk>', myapp_views.todo_completed, name="todo-completed"),
    path('todo/<int:pk>/update', myapp_views.todo_update, name="todo-update"),
    path('todo/delete/<int:pk>', myapp_views.todo_delete, name="todo-delete"),
    path('todo/subtask/delete/<int:pk>', myapp_views.subtask_delete, name="subtask-delete"),
    path('todo/alert/delete/<int:pk>', myapp_views.alert_task_delete, name="alert-task-delete"),
]