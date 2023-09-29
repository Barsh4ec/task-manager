from django.urls import path

from .views import index, task_view, task_create_view

urlpatterns = [
    path("", index, name="index"),
    path("project/<int:project_pk>/team/<int:team_pk>/tasks/", task_view, name="task-list"),
    path("project/<int:project_pk>/team/<int:team_pk>/task/create/", task_create_view, name="task-create")
]

app_name = "task"
