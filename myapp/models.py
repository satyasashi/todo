from django.db import models
import datetime

STATUS = [('Pending','Pending'), ('Completed', 'Completed')]

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(default=datetime.datetime.now())
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, help_text="Choose either Pending or Completed for status", default=STATUS[0][0])
    soft_del = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.title

