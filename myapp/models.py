from django.db import models
# from django.utils import timezone
import datetime
# from datetime import date

STATUS = [('Pending','Pending'), ('Completed', 'Completed')]

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateField(default=datetime.date.today)
    due_date = models.DateTimeField(help_text="Date format yyyy-mm-dd")
    notify_before = models.IntegerField(null=True, help_text="Mention number of hours before 'Due-Date' you want to get notified. Default is 1 hour")
    status = models.CharField(max_length=20, choices=STATUS, help_text="Choose either Pending or Completed for status", default=STATUS[0][0])
    soft_del = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.title