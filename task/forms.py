from django import forms
from django.contrib.auth import get_user_model

from task.models import Task, Team, TaskPoint


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime"


class TaskForm(forms.ModelForm):
    team_pk = None

    def __init__(self, *args, **kwargs):
        self.team_pk = kwargs.pop('team_pk', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.team_pk is not None:
            self.fields["assignees"].queryset = get_user_model().objects.filter(team_id=self.team_pk)
            self.fields["team"].queryset = Team.objects.filter(id=self.team_pk)

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees", "team"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": " Enter task name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control",
                       "placeholder": "Enter task description"}
            ),
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local",
                       "class": "form-control"}
            ),
            "priority": forms.Select(
                attrs={"class": "form-control"}
            ),
            "task_type": forms.Select(
                attrs={"class": "form-control"}
            ),
            "assignees": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
        }


class TaskPointForm(forms.ModelForm):
    class Meta:
        model = TaskPoint
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": " Enter task point name"}
            )}
