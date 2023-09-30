from django.urls import path

from .views import index, team_view, task_create_view, task_view

urlpatterns = [
    path("", index, name="index"),
    path("project/<int:project_pk>/team/<int:team_pk>/teams/", team_view, name="team-list"),
    path("project/<int:project_pk>/team/<int:team_pk>/task/create/", task_create_view, name="task-create"),
    path("project/<int:project_pk>/team/<int:team_pk>/tasks/", task_view, name="task-list")
]

app_name = "task"
