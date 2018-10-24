from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import TodoForm, ActionForm
from .models import Task

# Create your views here.
def home(request):
    try:
        pending_tasks = Task.objects.filter(status="Pending").order_by('due_date')
        try:
            pending_tasks[0]
        except:
            pending_tasks = None
    except Task.DoesNotExist:
        pending_tasks = None
        print(pending_tasks)

    try:
        completed_tasks = Task.objects.filter(status="Completed").order_by("-due_date")
        print(completed_tasks)
        try:
            completed_tasks[0]
        except:
            completed_tasks = None
    except:
        completed_tasks = None
        print(completed_tasks)


    return render(request, 'myapp/home.html', context={'tasks': pending_tasks, 'completed_tasks': completed_tasks})

def todo_add(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm()
    return render(request, 'myapp/add-todo.html', context={'form': form})

def todo_update(request, pk):
    todo = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'To-do Updated.')
            return redirect(reverse('home'))
    else:
        form = TodoForm(instance=todo)
    return render(request, 'myapp/todo_update.html', context={'form': form, 'todo':todo,})

def todo_completed(request, pk):
    todo = get_object_or_404(Task, pk=pk)
    todo.status = "Completed"
    todo.save()
    return redirect('home')

def  filter_tasks(request):
    pass