from django.urls import path

from .views import (
    ProjectListView,
    TeamListView,
    TaskCreateView,
    TaskListView,
    change_task_point_status,
    create_task_point_view,
    delete_task_point_view,
    register_view,
    ProjectCreationView,
    create_team_view,
    toggle_assign_to_task,
    delete_task_view,
    assign_worker_to_team_view,
    remove_worker_from_team_view
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="index"),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/teams/",
        TeamListView.as_view(),
        name="team-list"
    ),
    path("project/<int:project_pk>/team/create", create_team_view, name="team-create"),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/task/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/task-point-mark/<int:pk>/",
        change_task_point_status,
        name="mark-task-point"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/create-task-point/<int:pk>/",
        create_task_point_view,
        name="create-task-point"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/delete-task-point/<int:pk>/",
        delete_task_point_view,
        name="delete-task-point"
    ),
    path("accounts/register/", register_view, name="register"),
    path("project/create/", ProjectCreationView.as_view(), name="project-create"),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/task/<int:task_pk>/assign/",
        toggle_assign_to_task,
        name="task-assign"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/task/<int:task_pk>/delete/",
        delete_task_view,
        name="task-delete"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/assign-worker/",
        assign_worker_to_team_view,
        name="worker-assign"
    ),
    path(
        "project/<int:project_pk>/team/<int:team_pk>/remove-worker/",
        remove_worker_from_team_view,
        name="worker-remove"
    )
]

app_name = "task"
