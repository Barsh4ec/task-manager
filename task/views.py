from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Team, Task, Worker, TaskPoint
from .forms import (
    TaskForm,
    TaskPointForm,
    NewUserForm,
    TeamForm,
    TaskSearchForm,
    ProjectForm
)


class ProjectListView(generic.ListView):
    model = Project
    template_name = "index.html"


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    template_name = "team_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context["project_id"] = self.kwargs["project_pk"]
        context["team_id"] = self.kwargs["team_pk"]
        context["team"] = Team.objects.get(id=self.kwargs["team_pk"])
        context["teams"] = Team.objects.filter(project_id=self.kwargs["project_pk"])
        context["workers"] = Worker.objects.filter(team_id=self.kwargs["team_pk"])
        context["tasks"] = Task.objects.filter(team_id=self.kwargs["team_pk"])
        context["project"] = Project.objects.get(id=self.kwargs["project_pk"])
        return context


def create_team_view(request, project_pk):
    project = Project.objects.get(id=project_pk)

    if request.method == "GET":
        form = TeamForm()
        context = {
            "form": form,
            "project_id": project_pk,
            "teams": Team.objects.filter(project_id=project_pk),
            "project": Project.objects.get(id=project_pk)
        }
        return render(request, "task/team_create.html", context=context)

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.project = project
            team.save()
            return redirect("task:task-list", project_pk=project_pk, team_pk=team.id)
    return redirect("task:index")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        context["project_id"] = self.kwargs["project_pk"]
        context["team_id"] = self.kwargs["team_pk"]
        context["teams"] = Team.objects.filter(project_id=self.kwargs["project_pk"])
        context["project"] = Project.objects.get(id=self.kwargs["project_pk"])
        return context

    def get_success_url(self):
        return reverse("task:task-list", kwargs={
                    "project_pk": self.kwargs["project_pk"],
                    "team_pk": self.kwargs["team_pk"]
                })

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["team_id"] = self.kwargs["team_pk"]
        if self.kwargs.get("pk"):
            kwargs["worker_pk"] = self.kwargs["pk"]
        return kwargs


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["project_id"] = self.kwargs["project_pk"]
        context["team_id"] = self.kwargs["team_pk"]
        context["team"] = Team.objects.get(id=self.kwargs["team_pk"])
        context["teams"] = Team.objects.filter(project_id=self.kwargs["project_pk"])
        context["workers"] = Worker.objects.filter(team_id=self.kwargs["team_pk"])
        context["project"] = Project.objects.get(id=self.kwargs["project_pk"])
        context["form"] = TaskPointForm()
        name = self.request.GET.get("search_input", "")
        context["search_form"] = TaskSearchForm(
            initial={"search_input": name}
        )
        return context

    def get_queryset(self):
        search_form = TaskSearchForm(self.request.GET)
        if search_form.is_valid():
            return Task.objects.filter(
                name__icontains=search_form.cleaned_data["search_input"],
                team_id=self.kwargs["team_pk"]
            )
        return Task.objects.all()


@login_required()
def change_task_point_status(request, project_pk, team_pk, pk):
    task_point = TaskPoint.objects.get(id=pk)
    if task_point.is_done:  # if task_point status == True, change it to False
        task_point.is_done = False
        task_point.save()
    else:
        task_point.is_done = True
        task_point.save()
    return redirect("task:task-list", project_pk=project_pk, team_pk=team_pk)


@login_required()
def create_task_point_view(request, project_pk, team_pk, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        form = TaskPointForm(request.POST)
        if form.is_valid():
            task_point = form.save(commit=False)
            task_point.task = task
            task_point.save()
    return redirect("task:task-list", project_pk=project_pk, team_pk=team_pk)


@login_required()
def delete_task_point_view(request, project_pk, team_pk, pk):
    point_to_delete = TaskPoint.objects.get(id=pk)
    point_to_delete.delete()
    return redirect("task:task-list", project_pk=project_pk, team_pk=team_pk)


def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task:index")
    form = NewUserForm()
    return render(
        request=request,
        template_name="registration/register.html",
        context={"form": form}
    )


class ProjectCreationView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task:index")


@login_required
def toggle_assign_to_task(request, project_pk, team_pk, task_pk):
    worker = get_user_model().objects.get(id=request.user.id)
    if Task.objects.get(id=task_pk) in worker.tasks.all():  # if worker is already working on this task,
        worker.tasks.remove(task_pk)                        # we remove him from task workers
    else:                                                   # if else, add him
        worker.tasks.add(task_pk)
    return redirect("task:task-list", project_pk=project_pk, team_pk=team_pk)


@login_required()
def delete_task_view(request, project_pk, team_pk, task_pk):
    task_to_delete = Task.objects.get(id=task_pk)
    task_to_delete.delete()
    return redirect("task:task-list", project_pk=project_pk, team_pk=team_pk)


@login_required()
def remove_worker_from_team_view(request, project_pk, team_pk):
    worker = get_user_model().objects.get(id=request.user.id)
    if worker.team:
        for task in worker.tasks.all():
            worker.tasks.remove(task.id)
        worker.team = None
        worker.save()
    return redirect("task:team-list", project_pk=project_pk, team_pk=team_pk)


@login_required()
def assign_worker_to_team_view(request, project_pk, team_pk):
    worker = get_user_model().objects.get(id=request.user.id)
    if not worker.team:
        team = Team.objects.get(id=team_pk)
        worker.team = team
        worker.save()
    return redirect("task:team-list", project_pk=project_pk, team_pk=team_pk)
