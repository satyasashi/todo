from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, reverse
from django.contrib import messages
from django.urls import reverse
from celery import Celery
from celery.schedules import crontab
from .forms import TodoForm, ActionForm
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from .models import Task, SubTask
from .tasks import alert_tasks
import datetime
# import schedule

# scheduler = BackgroundScheduler()

def perm_delete(request):
    '''Soft deleted To-dos are being filtered, and checked against the days.
    If any of those are need to be deleted by today, then we Permanently delete them.'''
    delete_these = Task.objects.filter(soft_del=True)
    today = timezone.now()
    for del_item in delete_these:
        if del_item.soft_del_timestamp:
            if today.date() >= del_item.soft_del_timestamp.date():
                del_item.delete()
            else:
                print("Not today")
    return

# Create your views here.
def custom_filters(request):
    filters = ['Today', 'This-Week', 'Next-Week', 'Over-due']
    return filters

def home(request):
    '''We list all the pending tasks to the user on home page.'''
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
    
    # we call the custom_filters to get the list of 'filters' we use
    filters=custom_filters(request)

    # We call this when the page gets loaded. Usually this needs to be added to 
    # Scheduled tasks / periodic tasks and run this Once every 30 Seconds.
    task_alerts = alert_tasks(request)
    
    # Calling this, checks if any 'soft deleted' To-dos need to be deleted permanently today.
    perm_delete(request)

    if request.method == "GET":
        # Passing 'filter' to 'Home page' via GET request, we show only those filtered To-dos.
        if request.GET.get('filter'):
            filter_arg = request.GET.get('filter')
            from datetime import date
            today = timezone.now()
            today_weekday = timezone.now().weekday()
            total_week = 6

            if filter_arg.lower() == filters[0].lower():
                # Today
                filtered_tasks = Task.objects.filter(due_date__date=today, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            elif filter_arg.lower() == filters[1].lower():
                # This week
                remaining_weekday = total_week - today_weekday
                from_date = today-datetime.timedelta(today_weekday)
                end_date = today+datetime.timedelta(remaining_weekday)
                filtered_tasks = Task.objects.filter(due_date__date__gte=from_date, status="Pending", due_date__date__lte=end_date, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            elif filter_arg.lower() == filters[2].lower():
                # Next week
                remaining_weekday = total_week - today_weekday
                from_date = today+datetime.timedelta(remaining_weekday+1)
                end_weekday = total_week - from_date.weekday()
                end_date = from_date+datetime.timedelta(end_weekday)
                filtered_tasks = Task.objects.filter(due_date__date__gte=from_date, due_date__date__lte=end_date, status="Pending", soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            elif filter_arg.lower() == filters[3].lower():
                # Over due
                filtered_tasks = Task.objects.filter(due_date__lt=today, status="Pending", soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters, 'filter_arg':filter_arg})

            else:
                messages.add_message(request, messages.INFO, 'Filter unavailable please come back later')
                return redirect(reverse('home'))

        search_todos = ""
        # Passing the 'title' via GET request, we show All the To-dos which has specific keyword in its "Title"
        # Entered by the user in the 'Search Box' 
        if request.GET.get('title'):
            print("inside title")
            title_value = request.GET.get('title')
            search_todos = get_list_or_404(Task, title__icontains=str(title_value))
            print("search_todos is ", search_todos)
            return render(request, 'myapp/home.html', context={'search_todos':search_todos, 'title_value': title_value, 'filters':filters, 'task_alerts':task_alerts})


    return render(request, 'myapp/home.html', 
        context={'pending_tasks': pending_tasks, 'completed_tasks': completed_tasks, 'filters': filters, 'task_alerts': task_alerts})


# @scheduler.scheduled_job("interval", seconds=30, id="alert")
# def alert_tasks(request):
#     '''This function checks for Tasks/To-dos which are "Pending" and their alert_notification is near
#     and if yes, then it Shows "Alert" with Information in the Alert box on the right of web page.'''
    
#     alert_pending_tasks = Task.objects.filter(status="Pending", due_date__date__lte=timezone.now())
#     print("Alert pending tasks", alert_pending_tasks)

#     task_alerts = []

#     for task in alert_pending_tasks:
#         print("Inside task_alerts loop")
#         print(task.due_date)
#         present = timezone.localtime(timezone.now())
#         present_hour = present.hour
#         present_minute = present.minute
#         alert_task_time = timezone.localtime(task.due_date-datetime.timedelta(hours=task.notify_before))
#         alert_task_hour = alert_task_time.hour
#         alert_task_minute = alert_task_time.minute

#         if present_hour == alert_task_hour and present_minute == alert_task_minute:
#             print("Inside if statement in task_alerts")
#             task_alerts.append(task)
#             print("Appended ", task)
#     print(task_alerts)

#     return task_alerts


def todo_add(request):
    '''This gives users the option to Add a Todo.'''
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
    '''This gives users the option to Update a Todo.'''
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
        subtasks = todo.subtask_set.all()
    return render(request, 'myapp/todo_update.html', context={'form': form, 'todo':todo, 'subtasks': subtasks,'filters':filters, 'task_alerts':task_alerts})

def todo_completed(request, pk):
    '''This gives users the option to Mark a Todo as Completed.'''
    todo = get_object_or_404(Task, pk=pk)
    todo.status = "Completed"
    todo.save()
    return redirect('home')


def todo_delete(request, pk):
    '''This will not delete the Todo permanently from the database until it\'s been a Month
    since the user deleted the Todo from the UI'''
    todo = get_object_or_404(Task, pk=pk)
    todo.soft_del = True
    todo.soft_del_timestamp = timezone.now() + datetime.timedelta(days=30)
    todo.save()
    return redirect('home')

# schedule.every(30).seconds.do(home)

def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    task_id = subtask.task.id
    print("task_id is ", task_id)
    subtask.delete()
    print(reverse('todo-update', args=[task_id]))
    return redirect(reverse('todo-update', args=[task_id]))
    