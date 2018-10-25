from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import TodoForm, ActionForm
from .models import Task

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
            import datetime
            from datetime import date
            if filter_arg.lower() == filters[0].lower():
                today = date.today()
                # today = datetime.datetime.now().strftime("%d-%m-%y")
                filtered_tasks = Task.objects.filter(due_date=today, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            elif filter_arg.lower() == filters[1].lower():
                today_weekday = date.today().weekday()
                today = date.today()
                from_date = date.today()-datetime.timedelta(today_weekday)
                end_date = date.today()+datetime.timedelta(today_weekday)
                filtered_tasks = Task.objects.filter(due_date__gte=from_date, due_date__lte=end_date, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            elif filter_arg.lower() == filters[2].lower():
                today_weekday = date.today().weekday()
                total_week = 6
                today_weekday = total_week - today_weekday
                today=date.today()
                from_date = date.today()+datetime.timedelta(today_weekday)
                filtered_tasks = Task.objects.filter(due_date__gt=from_date, soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            elif filter_arg.lower() == filters[3].lower():
                today = date.today()
                filtered_tasks = Task.objects.filter(due_date__lte=today, status="Pending", soft_del=False)
                return render(request, 'myapp/home.html', context={'filtered_tasks': filtered_tasks, 'filters': filters})
            else:
                messages.add_message(request, messages.INFO, 'Filter unavailable please come back later')
                return redirect(reverse('home'))


    return render(request, 'myapp/home.html', 
        context={'pending_tasks': pending_tasks, 'completed_tasks': completed_tasks, 'filters': filters,})

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
