from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import TodoForm, ActionForm
from django.utils import timezone
from .models import Task
import datetime


# Create your views here.
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

    filters = ['Today', 'This-Week', 'Next-Week', 'Over-due']

    if request.method == "GET":
        if request.GET.get('filter'):
            filter_arg = request.GET.get('filter')
            from datetime import date
            
            if filter_arg.lower() == filters[0].lower():
                today = timezone.now()
                # today = datetime.datetime.now().strftime("%d-%m-%y")
                filtered_tasks = Task.objects.filter(due_date=today, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            elif filter_arg.lower() == filters[1].lower():
                today_weekday = timezone.now().weekday()
                today = timezone.now()
                from_date = today-datetime.timedelta(today_weekday)
                total_week = 6
                today_weekday = total_week - today_weekday
                end_date = today+datetime.timedelta(today_weekday)
                filtered_tasks = Task.objects.filter(due_date__gte=from_date, status="Pending", due_date__lte=end_date, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            elif filter_arg.lower() == filters[2].lower():
                today_weekday = timezone.now().weekday()
                total_week = 6
                today_weekday = total_week - today_weekday
                today=timezone.now()
                from_date = today+datetime.timedelta(today_weekday)
                filtered_tasks = Task.objects.filter(due_date__gt=from_date, status="Pending", soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            elif filter_arg.lower() == filters[3].lower():
                today = timezone.now()
                filtered_tasks = Task.objects.filter(due_date__lt=today, status="Pending", soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            else:
                messages.add_message(request, messages.INFO, 'Filter unavailable please come back later')
                return redirect(reverse('home'))

    task_alerts = alert_tasks()
    
    return render(request, 'myapp/home.html', 
        context={'pending_tasks': pending_tasks, 'completed_tasks': completed_tasks, 'filters': filters,'task_alerts': task_alerts})


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
    filters = ['Today', 'This-Week', 'Next-Week', 'Over-due']
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm()
    return render(request, 'myapp/add-todo.html', context={'form': form, 'filters':filters})

def todo_update(request, pk):
    todo = get_object_or_404(Task, pk=pk)
    filters = ['Today', 'This-Week', 'Next-Week', 'Over-due']
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'To-do Updated.')
            return redirect(reverse('home'))
    else:
        form = TodoForm(instance=todo)
    return render(request, 'myapp/todo_update.html', context={'form': form, 'todo':todo, 'filters':filters})

def todo_completed(request, pk):
    todo = get_object_or_404(Task, pk=pk)
    todo.status = "Completed"
    todo.save()
    return redirect('home')
