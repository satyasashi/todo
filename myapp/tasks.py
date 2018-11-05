from celery import task 
from celery import shared_task 
from django.utils import timezone
from .models import Task, AlertTask
import datetime

@task(name='alert_tasks')
def alert_tasks(request):
    '''This function checks for Tasks/To-dos which are "Pending" and their alert_notification is near
    and if yes, then it Shows "Alert" with Information in the Alert box on the right of web page.'''
    
    alert_pending_tasks = Task.objects.filter(status="Pending", due_date__date__lte=timezone.now())
    print("Alert pending tasks", alert_pending_tasks)

    # task_alerts = []

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
            # task_alerts.append(task)
            alert_tasks, created = AlertTask.objects.get_or_create(alert_title=task.title, task=task)
            if created:
                alert_tasks.save()
            print("Added to Database")
    # print(task_alerts)

    return


# Calling this, checks if any 'soft deleted' To-dos need to be deleted permanently today.
@task(name='permanent-delete-task')
def perm_delete(request):
    '''Soft deleted To-dos are being filtered, and checked against the days.
    If any of those are need to be deleted by today, then we Permanently delete them.'''
    delete_these = Task.objects.filter(soft_del=True)
    today = timezone.now()
    for del_item in delete_these:
        if del_item.soft_del_timestamp:
            if today.date() >= del_item.soft_del_timestamp.date():
                del_item.delete()
                print("Task was deleted after 30 days")
            else:
                print("Not today")
    return
