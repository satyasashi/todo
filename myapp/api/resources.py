from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL
from myapp.models import Task

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all().order_by('due_date')
        resource_name = 'task'
        filtering = {
            'status': ALL,
        }