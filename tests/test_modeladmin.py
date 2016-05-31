from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from admin_view_permission.admin import *

from test_app.models import *


class TestModelAdminSuperUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.super_user = get_user_model().objects.create_superuser(
            username='super_user',
            email='',
            password='super_user',
        )

        self.permission = Permission.objects.get(name='Can view testmodel1')
        self.super_user.user_permissions.set([self.permission])
        self.client.login(username='super_user', password='super_user')

    def tearDown(self):
        self.client.logout()

    def test_can_see_everything(self):
        response = self.client.get(reverse('admin:index'))
        # Two apps, Auth and Test app
        self.assertEqual(len(response.context['app_list']), 2)

    def test_can_create_model(self):
        response =  self.client.get(
            reverse('admin:%s_%s_add' %('test_app', 'testmodel1'))
        )
        self.assertEqual(response.status_code, 200)


class TestModelAdminViewUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.view_user = get_user_model().objects.create_user(
            username='view_user',
            password='view_user',
            is_staff=True
        )

        # Create tests
        self.test10 = TestModel1.objects.create(
            var1 = 'Test10',
            var2 = 'Test10',
            var3 = 5
        )

        self.permission = Permission.objects.get(name='Can view testmodel1')
        self.view_user.user_permissions.set([self.permission])
        self.client.login(username='view_user', password='view_user')

    def tearDown(self):
        self.client.logout()

    def test_can_see_only_test_app(self):
        response = self.client.get(reverse('admin:index'))
        # Only one app
        self.assertEqual(len(response.context['app_list']), 1)
        self.assertEqual(response.context['app_list'][0]['app_label'],
                         'test_app')
        self.assertEqual(len(response.context['app_list'][0]['models']), 1)
        self.assertEqual(
            response.context['app_list'][0]['models'][0]['object_name'],
            'TestModel1'
        )

    def test_can_view_changelist(self):
        response =  self.client.get(
            reverse('admin:%s_%s_changelist' %('test_app', 'testmodel1'))
        )
        self.assertEqual(response.status_code, 200)

    def test_can_view_history(self):
        response =  self.client.get(
            reverse('admin:%s_%s_history' %('test_app', 'testmodel1'),
                    args=(self.test10.pk, ))
        )
        self.assertEqual(response.status_code, 200)

    def test_can_create_object(self):
        response =  self.client.get(
            reverse('admin:%s_%s_add' %('test_app', 'testmodel1'))
        )
        self.assertEqual(response.status_code, 403)

    def test_can_change_object(self):
        response = self.client.get(
            reverse('admin:%s_%s_change' %('test_app', 'testmodel1'),
                    args=(self.test10.pk,))
        )
        self.assertEqual(response.status_code, 200)

    def test_can_delete_object(self):
        response = self.client.get(
            reverse('admin:%s_%s_delete' %('test_app', 'testmodel1'),
                    args=(self.test10.pk,))
        )
        self.assertEqual(response.status_code, 403)

