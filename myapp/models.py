import datetime
from django.db import models
# from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
# from datetime import date

STATUS = [('Pending','Pending'), ('Completed', 'Completed')]
DEFAULT_SUB_TASK=0

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateField(default=datetime.date.today)
    due_date = models.DateTimeField(help_text="Date format yyyy-mm-dd")
    notify_before = models.IntegerField(null=True, default=1, help_text="Mention number of hours before 'Due-Date' you want to get notified. Default is 1 hour",
     validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS, help_text="Choose either Pending or Completed for status", default=STATUS[0][0])
    soft_del = models.BooleanField(blank=True, default=False)
    soft_del_timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    subtask_title = models.CharField(max_length=100, blank=True, null=True, help_text="If you want to add optional sub-tasks you can do it here.")
    task = models.ForeignKey(Task, default=DEFAULT_SUB_TASK, on_delete=models.CASCADE)

    def __str__(self):
        return self.subtask_title


class AlertTask(models.Model):
    alert_title = models.CharField(max_length=255)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.alert_title