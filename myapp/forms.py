from django.contrib.admin import widgets
from django.conf import settings
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Task
import datetime

PENDING=[('Pending','Pending')]
COMPLETED=[('Completed','Completed')]

STATUS = [('Pending','Pending'), ('Completed', 'Completed')]


class TodoForm(forms.ModelForm):
    due_date = forms.DateTimeField(label="Due-Date format yyyy-mm-dd hh:mm", widget=DateTimePickerInput(format='%Y-%m-%d %H:%M'))
    notify_before = forms.IntegerField(label="Mention number of hours before 'Due-Date' time you want to get notified.")
    status = forms.ChoiceField(choices=STATUS, widget=forms.RadioSelect())
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['created_on', 'soft_del']

    # def __init__(self, *args, **kwargs):
    #     super(TodoForm, self).__init__(*args, **kwargs)
    #     self.fields['due_date'].widget = widgets.AdminDateWidget()
    #     self.fields['due_date'].widget.attrs.update({'id': 'datetimepicker'})

class ActionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']