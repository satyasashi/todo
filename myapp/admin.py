from django.contrib import admin
from .models import Task


# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'status')
    search_fields = ('title',)
    list_filter = ('due_date',)
    ordering = ['-due_date',]
    date_hierarchy = 'created_on'

admin.site.register(Task, TaskAdmin)