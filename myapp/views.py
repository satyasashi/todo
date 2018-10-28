from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, reverse
from django.contrib import messages
from celery import Celery
from celery.schedules import crontab
from .forms import TodoForm, ActionForm
from django.utils import timezone
from .models import Task
import datetime

app=Celery()

# Create your views here.
def custom_filters(request):
    filters = ['Today', 'This-Week', 'Next-Week', 'Over-due']
    return filters

def home(request):
    try:
        pending_tasks = Task.objects.filter(status="Pending", soft_del=False).order_by('due_date')
        try:
            pending_tasks[0]
        except:
            pending_tasks = None
    except Task.DoesNotExist:
        pending_tasks = None
        print(pending_tasks)

    try:
        completed_tasks = Task.objects.filter(status="Completed", soft_del=False).order_by("-due_date")
        print(completed_tasks)
        try:
            completed_tasks[0]
        except:
            completed_tasks = None
    except:
        completed_tasks = None
        print(completed_tasks)

    filters=custom_filters(request)
    task_alerts = alert_tasks(request)
    
    if request.method == "GET":
        if request.GET.get('filter'):
            filter_arg = request.GET.get('filter')
            from datetime import date
            today = timezone.now()
            today_weekday = timezone.now().weekday()
            total_week = 6

            if filter_arg.lower() == filters[0].lower():
                filtered_tasks = Task.objects.filter(due_date=today, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            elif filter_arg.lower() == filters[1].lower():
                from_date = today-datetime.timedelta(today_weekday)
                today_weekday = total_week - today_weekday
                end_date = today+datetime.timedelta(today_weekday)
                filtered_tasks = Task.objects.filter(due_date__gte=from_date, status="Pending", due_date__lte=end_date, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            elif filter_arg.lower() == filters[2].lower():
                today_weekday = total_week - today_weekday
                from_date = today+datetime.timedelta(today_weekday)
                filtered_tasks = Task.objects.filter(due_date__gt=from_date, status="Pending", soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            elif filter_arg.lower() == filters[3].lower():
                filtered_tasks = Task.objects.filter(due_date__lt=today, status="Pending", soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            else:
                messages.add_message(request, messages.INFO, 'Filter unavailable please come back later')
                return redirect(reverse('home'))

        search_todos = ""

        if request.GET.get('title'):
            print("inside title")
            title_value = request.GET.get('title')
            search_todos = get_list_or_404(Task, title__icontains=str(title_value))
            print("search_todos is ", search_todos)
            return render(request, 'myapp/home.html', context={'search_todos':search_todos, 'title_value': title_value, 'filters':filters, 'task_alerts':task_alerts})


    return render(request, 'myapp/home.html', 
        context={'pending_tasks': pending_tasks, 'completed_tasks': completed_tasks, 'filters': filters})



def alert_tasks(request):
    alert_pending_tasks = Task.objects.filter(status="Pending", due_date__date__lte=timezone.now())
    print("Alert pending tasks", alert_pending_tasks)

    task_alerts = []

    for task in alert_pending_tasks:
        print("Inside task_alerts loop")
        print(task.due_date)
        present = timezone.localtime(timezone.now())
        present_hour = present.hour
        present_minute = present.minute
        alert_task_time = timezone.localtime(task.due_date-datetime.timedelta(hours=task.notify_before))
        alert_task_hour = alert_task_time.hour
        alert_task_minute = alert_task_time.minute

        if present_hour == alert_task_hour and present_minute == alert_task_minute:
            print("Inside if statement in task_alerts")
            task_alerts.append(task)
            print("Appended ", task)
    print(task_alerts)

    return task_alerts


def todo_add(request):
    filters = custom_filters(request)
    task_alerts = alert_tasks(request)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm()

    return render(request, 'myapp/add-todo.html', context={'form': form, 'filters':filters, 'task_alerts':task_alerts})

def todo_update(request, pk):
    todo = get_object_or_404(Task, pk=pk)
    filters = custom_filters(request)
    task_alerts = alert_tasks(request)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'To-do Updated.')
            return redirect(reverse('home'))
    else:
        form = TodoForm(instance=todo)
    return render(request, 'myapp/todo_update.html', context={'form': form, 'todo':todo, 'filters':filters, 'task_alerts':task_alerts})

def todo_completed(request, pk):
    todo = get_object_or_404(Task, pk=pk)
    todo.status = "Completed"
    todo.save()
    return redirect('home')


def todo_delete(request, pk):
    todo = get_object_or_404(Task, pk=pk)
    todo.soft_del = True
    todo.save()
    permanent_delete = timezone.now() + datetime.timedelta(days=30)
    today = timezone.now()
    if today.date() >= permanent_delete.date():
        todo.delete()
    return redirect('home')