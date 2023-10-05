from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task.forms import TaskForm
from task.models import Project, Team, Task, Worker, TaskPoint, TaskType, Position

PROJECT_LIST_URL = reverse("task:index")
PROJECT_CREATE_URL = reverse("task:project-create")
TEAM_LIST_URL = "task:team-list"
TEAM_CREATE_URL = "task:team-create"
TASK_CREATE_URL = "task:task-create"
TASK_LIST_URL = "task:task-list"
CHANGE_TASK_POINT_STATUS_URL = "task:mark-task-point"
CREATE_TASK_POINT_URL = "task:create-task-point"
DELETE_TASK_POINT_URL = "task:delete-task-point"
REGISTER_URL = reverse("task:register")
LOGIN_URL = reverse("login")
LOGOUT_URL = reverse("logout")
TASK_ASSIGN_URL = "task:task-assign"
TASK_DELETE_URL = "task:task-delete"
WORKER_ASSIGN_URL = "task:worker-assign"
WORKER_REMOVE_URL = "task:worker-remove"


class UserWithoutLoginTest(TestCase):
    def test_index_login_is_not_required(self):
        res = self.client.get(PROJECT_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_project_create_login_required(self):
        res = self.client.get(PROJECT_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_register_url_is_not_login_required(self):
        res = self.client.get(REGISTER_URL)
        self.assertEqual(res.status_code, 200)

    def test_login_url_is_not_login_required(self):
        res = self.client.get(LOGIN_URL)
        self.assertEqual(res.status_code, 200)

    def test_logout_url_is_not_login_required(self):
        res = self.client.get(LOGOUT_URL)
        self.assertEqual(res.status_code, 200)


class LoggedInUserTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="test_task_type_name"
        )
        self.project = Project.objects.create(
            name="test_project",
            description="test_description",
            image="static/assets/img/team/user-photo-placeholder.png"
        )
        self.team = Team.objects.create(
            name="test_team",
            description="team_description",
            project=self.project
        )
        self.task = Task.objects.create(
            name="test_task_name",
            description="test_task_description",
            deadline=timezone.now(),
            task_type=self.task_type,
            team=self.team
        )
        self.task_point = TaskPoint.objects.create(
            name="task_point_name",
            task=self.task
        )
        self.position = Position.objects.create(
            name="test_position_name"
        )
        worker_username = "test_worker_username"
        worker_password = "test_password"
        self.worker = get_user_model().objects.create_user(
            username=worker_username,
            password=worker_password,
            team=self.team,
            position=self.position
        )
        self.client.force_login(self.worker)

    def test_project_list_success(self):
        response = self.client.get(PROJECT_LIST_URL)

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertIn("project_list", context)
        self.assertEqual(context["project_list"].count(), 1)
        self.assertEqual(context["project_list"].first(), self.project)

    def test_team_create_view(self):
        new_team_data = {
            "name": "new_team_name",
            "description": "new_team_description",
            "project": self.project
        }
        response = self.client.post(
            reverse(
                TEAM_CREATE_URL, kwargs={"project_pk": self.project.id}
            ),
            new_team_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Team.objects.count(), 2)

    def test_task_create_view(self):
        new_task_data = {
            "name": "new_test_task_name",
            "description": "test_task_description",
            "deadline": timezone.now(),
            "priority": "low",
            "task_type": self.task_type.id,
            "team": self.team.id,
            "assignees": [self.worker.id, ]
        }
        response = self.client.post(
            reverse(
                TASK_CREATE_URL, kwargs={
                    "project_pk": self.project.id,
                    "team_pk": self.team.id
                }
            ),
            new_task_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_list_view(self):
        response = self.client.get(
            reverse(
                TASK_LIST_URL, kwargs={
                    "project_pk": self.project.id,
                    "team_pk": self.team.id
                }
            )
        )

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertIn("task_list", context)
        self.assertEqual(context["task_list"].count(), 1)
        self.assertEqual(context["task_list"].first(), self.task)

    def test_change_task_point_status(self):
        current_task_point_status = self.task_point.is_done
        response = self.client.get(
            reverse(
                CHANGE_TASK_POINT_STATUS_URL, kwargs={
                    "project_pk": self.project.id,
                    "team_pk": self.team.id,
                    "pk": self.task_point.id
                }
            )
        )
        self.task_point.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(not current_task_point_status, self.task_point.is_done)

    def test_create_task_point_view(self):
        new_task_point_data = {
            "name": "new_test_task_name",
        }
        response = self.client.post(
            reverse(
                CREATE_TASK_POINT_URL, kwargs={
                    "project_pk": self.project.id,
                    "team_pk": self.team.id,
                    "pk": self.task.id
                }
            ),
            new_task_point_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskPoint.objects.count(), 2)
        self.assertEqual(self.task.task_points.count(), 2)

    def test_delete_task_point_view(self):
        response = self.client.post(
            reverse(
                DELETE_TASK_POINT_URL, kwargs={
                    "project_pk": self.project.id,
                    "team_pk": self.team.id,
                    "pk": self.task_point.id
                }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskPoint.objects.count(), 0)
        self.assertEqual(self.task.task_points.count(), 0)
