from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from task.models import Project, Team, Position, TaskType, Task


class ModelTests(TestCase):
    def test_project_str(self):
        project_name = "test_project"
        project = Project.objects.create(
            name=project_name,
            description="test_description",
            image="static/assets/img/team/user-photo-placeholder.png"
        )
        self.assertEqual(str(project), f"{project_name}")

    def test_team_str(self):
        project = Project.objects.create(
            name="test_project",
            description="test_description",
            image="static/assets/img/team/user-photo-placeholder.png"
        )

        team_name = "test_team"
        team = Team.objects.create(
            name=team_name,
            description="team_description",
            project=project
        )
        self.assertEqual(str(team), f"{team_name}, working on {str(project)}")

    def test_position_str(self):
        position_name = "test_position_name"
        position = Position.objects.create(
            name=position_name
        )
        self.assertEqual(str(position), f"{position_name}")

    def test_create_worker_with_position_and_team(self):
        project = Project.objects.create(
            name="test_project",
            description="test_description",
            image="static/assets/img/team/user-photo-placeholder.png"
        )
        team = Team.objects.create(
            name="test_team",
            description="team_description",
            project=project
        )
        position = Position.objects.create(
            name="test_position_name"
        )
        worker_username = "test_worker_username"
        worker_password = "test_password"
        worker = get_user_model().objects.create_user(
            username=worker_username,
            password=worker_password,
            team=team,
            position=position
        )
        self.assertEqual(worker.username, worker_username)
        self.assertEqual(worker.team, team)
        self.assertEqual(worker.position, position)
        self.assertTrue(worker.check_password(worker_password))

    def test_task_type_str(self):
        task_type_name = "test_task_type_name"
        task_type = TaskType.objects.create(
            name=task_type_name
        )
        self.assertEqual(str(task_type), f"{task_type_name}")

    def test_task_str(self):
        task_type = TaskType.objects.create(
            name="test_task_type_name"
        )
        project = Project.objects.create(
            name="test_project",
            description="test_description",
            image="static/assets/img/team/user-photo-placeholder.png"
        )
        team = Team.objects.create(
            name="test_team",
            description="team_description",
            project=project
        )
        task_name = "test_task_name"
        deadline = timezone.now()
        task = Task.objects.create(
            name=task_name,
            description="test_task_description",
            deadline=deadline,
            task_type=task_type,
            team=team
        )
        self.assertEqual(str(task), f"{task_name}")
        self.assertEqual(task.deadline, deadline)
        self.assertEqual(task.priority, "normal")
        self.assertEqual(task.task_type, task_type)
        self.assertEqual(task.team, team)
        self.assertTrue(task.assignees.count() == 0)
        self.assertFalse(task.is_completed)
