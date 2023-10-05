from django.test import TestCase

from task.forms import TaskPointForm, NewUserForm
from task.models import Position, Project


class FormsTest(TestCase):
    def test_user_creation_form_with_correct_data(self):
        position = Position.objects.create(
            name="test_name"
        )
        form_data = {
            "username": "test_user",
            "email": "test@gmail.com",
            "password1": "password_test",
            "password2": "password_test",
            "first_name": "first_name",
            "last_name": "last_name",
            "position": position
        }
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validation_error_when_passwords_are_not_equal(self):
        form_data = {
            "password1": "password_test",
            "password2": "password",
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_validation_error_when_there_is_no_email_provided(self):
        form_data = {
            "username": "test_user",
            "password1": "password_test",
            "password2": "password_test",
            "first_name": "first_name",
            "last_name": "last_name"
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_point_creation_form_valid_data(self):
        name = "test_task_point"
        form_data = {
            "name": name
        }
        form = TaskPointForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data.get("name"), name)

    def test_team_creation_form_valid_data(self):
        name = "test_task_point",
        description = "test_team_description"
        project = Project.objects.create(
            name="test_project",
            description="test_description",
            image="static/assets/img/team/user-photo-placeholder.png"
        )
        form_data = {
            "name": name,
            "description": description,
            "project": project
        }
        form = TaskPointForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data.get("name"), name)
