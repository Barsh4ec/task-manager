from django import forms
from django.contrib.auth import get_user_model

from task.models import Task, Team


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
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            )}

