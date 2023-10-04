from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task.models import Task, Team, TaskPoint, Worker, Project


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime"


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": " Enter project name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control",
                       "placeholder": "Enter project description"}
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control"}
            ),
        }


class TaskForm(forms.ModelForm):
    team_pk = None

    def __init__(self, *args, **kwargs):
        self.team_pk = kwargs.pop('team_id', None)
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
            "team": forms.Select(
                attrs={"class": "form-control"}
            )
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


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Worker
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "position")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": " Enter team name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control",
                       "placeholder": " Enter team description"}
            )}


class TaskSearchForm(forms.Form):
    search_input = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search"
            }
        )
    )
