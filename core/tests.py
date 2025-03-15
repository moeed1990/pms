from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Project, ProjectRole

class ProjectViewsTestCase(TestCase):

    def setUp(self):
        """Creating test users and a sample project."""
        self.owner = User.objects.create_user(username='owner', password='password123')
        self.editor = User.objects.create_user(username='editor', password='password123')
        self.viewer = User.objects.create_user(username='viewer', password='password123')

        self.project = Project.objects.create(name="Test Project", status="active", owner=self.owner)
        ProjectRole.objects.create(user=self.editor, project=self.project, role="editor")

    def test_create_project(self):
        """only logged in user can create a new project."""
        self.client.login(username='owner', password='password123')
        response = self.client.post(reverse('create_project'), {'name': 'New Project', 'status': 'completed'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="New Project").exists())

    def test_edit_project_owner(self):
        """if user try to edit with permission"""
        self.client.login(username='owner', password='password123')
        response = self.client.post(reverse('update_project', args=[self.project.id]), {
            'name': 'Updated Project',
            'status': 'completed'
        })
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project')

    def test_edit_project_without_permission(self):
        """if some  tries to edit the project without permission."""
        self.client.login(username='viewer', password='password123')
        response = self.client.post(reverse('update_project', args=[self.project.id]), {
            'name': 'Hacked Project',
            'status': 'completed'
        })
        self.assertEqual(response.status_code, 403)
        self.project.refresh_from_db()
        self.assertNotEqual(self.project.name, 'Hacked Project')
