import secrets

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .models import Project, Task


class StudioTests(TestCase):
    def setUp(self):
        self.password = secrets.token_urlsafe(24)
        self.user = get_user_model().objects.create_user('alice', password=self.password)
        self.other = get_user_model().objects.create_user('bob', password=secrets.token_urlsafe(24))
        self.project = Project.objects.create(owner=self.user, title='Мой трек', bpm=120)
        self.task = Task.objects.create(project=self.project, title='Свести бас')
        self.client.force_login(self.user)

    def test_anonymous_cannot_view_projects(self):
        self.client.logout()
        self.assertRedirects(self.client.get('/'), '/login/?next=/')

    def test_login_and_logout(self):
        self.client.logout()
        response = self.client.post('/login/', {'username': 'alice', 'password': self.password})
        self.assertRedirects(response, '/')
        self.assertRedirects(self.client.post('/logout/'), '/login/')

    def test_create_and_edit_project(self):
        response = self.client.post(reverse('project_new'), {'title': 'Новый', 'bpm': 140, 'stage': 'idea', 'musical_key': 'Am', 'notes': 'Идея'})
        new = Project.objects.get(title='Новый')
        self.assertEqual(new.owner, self.user)
        self.assertRedirects(response, reverse('project', args=[new.pk]))
        self.client.post(reverse('project_edit', args=[new.pk]), {'title': 'Готовый', 'bpm': 95, 'stage': 'done'})
        new.refresh_from_db()
        self.assertEqual((new.title, new.bpm, new.stage), ('Готовый', 95, 'done'))

    def test_rejects_invalid_bpm(self):
        for bpm in (0, 301, 'abc'):
            with self.subTest(bpm=bpm):
                response = self.client.post(reverse('project_new'), {'title': 'Ошибка', 'bpm': bpm, 'stage': 'idea'})
                self.assertEqual(response.status_code, 200)
                self.assertIn('bpm', response.context['form'].errors)
        self.assertFalse(Project.objects.filter(title='Ошибка').exists())

    def test_task_lifecycle_and_progress(self):
        url = reverse('project', args=[self.project.pk])
        self.client.post(url, {'title': 'Записать вокал'})
        self.assertEqual(self.project.tasks.count(), 2)
        self.client.post(reverse('task_toggle', args=[self.task.pk]))
        self.assertEqual(self.project.progress, 50)
        self.client.post(reverse('task_edit', args=[self.task.pk]), {'title': 'Свести вокал'})
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Свести вокал')
        self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertEqual(self.project.progress, 0)

    def test_blank_task_is_rejected(self):
        response = self.client.post(reverse('project', args=[self.project.pk]), {'title': '   '})
        self.assertIn('title', response.context['form'].errors)
        self.assertEqual(self.project.tasks.count(), 1)

    def test_get_cannot_delete_or_toggle(self):
        for route in ('project_delete', 'task_delete'):
            pk = self.project.pk if route == 'project_delete' else self.task.pk
            self.assertEqual(self.client.get(reverse(route, args=[pk])).status_code, 200)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        self.assertEqual(self.client.get(reverse('task_toggle', args=[self.task.pk])).status_code, 405)

    def test_project_cascade_delete(self):
        self.client.post(reverse('project_delete', args=[self.project.pk]))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_owner_isolation(self):
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get('/'), 'Мой трек')
        for route, pk in [('project', self.project.pk), ('project_edit', self.project.pk),
                          ('project_delete', self.project.pk), ('task_edit', self.task.pk),
                          ('task_delete', self.task.pk), ('task_toggle', self.task.pk)]:
            with self.subTest(route=route):
                response = self.client.post(reverse(route, args=[pk]), {'title': 'Взлом', 'bpm': 120, 'stage': 'done'})
                self.assertEqual(response.status_code, 404)
        self.project.refresh_from_db()
        self.task.refresh_from_db()
        self.assertEqual(self.project.title, 'Мой трек')
        self.assertFalse(self.task.done)

    def test_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(reverse('task_toggle', args=[self.task.pk])).status_code, 403)

    def test_filter_by_stage(self):
        Project.objects.create(owner=self.user, title='Релиз', stage='done')
        response = self.client.get('/?stage=done')
        self.assertContains(response, 'Релиз')
        self.assertNotContains(response, 'Мой трек')

    def test_user_content_is_escaped(self):
        self.project.title = '<script>alert(1)</script>'
        self.project.save()
        response = self.client.get('/')
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;script&gt;')
