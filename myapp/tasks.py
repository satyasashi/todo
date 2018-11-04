from celery import task 
from celery import shared_task 
from django.utils import timezone
from .models import Task
import datetime

@task(name='alert_tasks')
def alert_tasks(request):
    '''This function checks for Tasks/To-dos which are "Pending" and their alert_notification is near
    and if yes, then it Shows "Alert" with Information in the Alert box on the right of web page.'''
    
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
