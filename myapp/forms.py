from django.contrib.admin import widgets
from django.conf import settings
from django import forms
from .models import Task

PENDING=[('Pending','Pending')]
COMPLETED=[('Completed','Completed')]

STATUS = [('Pending','Pending'), ('Completed', 'Completed')]


class TodoForm(forms.ModelForm):
    # title = forms.CharField(max_length=100, widget=forms.TextInput())
    # description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=widgets.AdminDateWidget(attrs={'id': 'datetimepicker'}))
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
