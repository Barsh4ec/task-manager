from django.urls import path

from .views import index, team_view, task_create_view, task_view, task_point_view, create_task_point_view

urlpatterns = [
    path("", index, name="index"),
    path("project/<int:project_pk>/team/<int:team_pk>/teams/", team_view, name="team-list"),
    path("project/<int:project_pk>/team/<int:team_pk>/task/create/", task_create_view, name="task-create"),
    path("project/<int:project_pk>/team/<int:team_pk>/tasks/", task_view, name="task-list"),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/task-point-mark/<int:pk>/",
        task_point_view,
        name="mark-task-point"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/create-task-point/<int:pk>/",
        create_task_point_view,
        name="create-task-point"
    ),

]

app_name = "task"
