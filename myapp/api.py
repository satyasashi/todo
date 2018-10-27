from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from myapp.models import Task

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'Task'
        authorization = Authorization()