from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .models import Project, Team, Task, Worker, TaskPoint
from .forms import TaskForm, TaskPointForm


def index(request):
    projects = Project.objects.all()
    context = {
        "segment": "index",
        "projects": projects
    }

    return render(request, "index.html", context=context)


def team_view(request, project_pk, team_pk):
    teams = Team.objects.filter(project_id=project_pk)
    workers = Worker.objects.filter(team_id=team_pk)
    tasks = Task.objects.filter(team_id=team_pk)
    team = Team.objects.get(id=team_pk)
    context = {
        "team": team,
        "project_id": project_pk,
        "teams": teams,
        "team_id": team_pk,
        "workers": workers,
        "tasks": tasks
    }
    return render(request, "teams_list.html", context=context)


def task_create_view(request, project_pk, team_pk):

    if request.method == "GET":
        teams = Team.objects.filter(project_id=project_pk)
        form = TaskForm(team_pk=team_pk)
        context = {
            "form": form,
            "teams": teams,
            "project_id": project_pk,
            "team_id": team_pk
        }
        return render(request, "task_create.html", context=context)

    if request.method == "POST":
        form = TaskForm(request.POST)
        print(form.data)
        if form.is_valid():
            task = Task.objects.create(
                name=form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
                deadline=form.cleaned_data.get("deadline"),
                priority=form.cleaned_data.get("priority"),
                task_type=form.cleaned_data.get("task_type"),
                team=form.cleaned_data.get("team")
            )
            task.assignees.set(form.cleaned_data.get("assignees"))
            return HttpResponseRedirect(reverse(
                "task:task-list", kwargs={
                    "project_pk": project_pk,
                    "team_pk": team_pk
                }
            ))
        return HttpResponseRedirect(reverse(
            "task:task-list", kwargs={
                "project_pk": project_pk,
                "team_pk": team_pk
            }
        ))


def task_view(request, project_pk, team_pk):
    form = TaskPointForm()
    workers = Worker.objects.filter(team_id=team_pk)
    teams = Team.objects.filter(project_id=project_pk)
    tasks = Task.objects.filter(team_id=team_pk)
    team = Team.objects.get(id=team_pk)
    context = {
        "form": form,
        "team": team,
        "project_id": project_pk,
        "teams": teams,
        "team_id": team_pk,
        "workers": workers,
        "tasks": tasks,
    }
    return render(request, "task_list.html", context=context)


def task_point_view(request, project_pk, team_pk, pk):
    task_point = TaskPoint.objects.get(id=pk)
    if task_point.is_done:
        task_point.is_done = False
        task_point.save()
    else:
        task_point.is_done = True
        task_point.save()
    return redirect("task:task-list", project_pk=project_pk, team_pk=team_pk)


def create_task_point_view(request, project_pk, team_pk, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        form = TaskPointForm(request.POST)
        if form.is_valid():
            task_point = form.save(commit=False)
            task_point.task = task
            task_point.save()
    return redirect("task:task-list", project_pk=project_pk, team_pk=team_pk)
