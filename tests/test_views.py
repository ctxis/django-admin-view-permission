from __future__ import unicode_literals

from django.test import TestCase, Client, RequestFactory
from django.contrib import admin as default_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from admin_view_permission.admin import *

from test_app.models import *
from test_app.admin import ModelAdmin1


class TestModelAdminViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.super_user = get_user_model().objects.create_superuser(
            username='super_user',
            email='',
            password='super_user',
        )
        self.simple_user = get_user_model().objects.create_user(
            username='simple_user',
            password='simple_user',
            is_staff=True
        )
        self.object_testmodel0 = TestModel0.objects.create(
            var1='Test',
            var2='Test',
            var3=5
        )
        self.object_testmodel1 = TestModel1.objects.create(
            var1='Test',
            var2='Test',
            var3=5,
        )
        self.object_testmodel1.var4.add(self.object_testmodel0)


        self.permission = Permission.objects.get(name='Can view testmodel1')
        self.super_user.user_permissions.set([self.permission])
        self.simple_user.user_permissions.set([self.permission])

    def tearDown(self):
        self.client.logout()

    def test_index_view_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(reverse('admin:index'))
        assert len(response.context['app_list']) == 2

    def test_index_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(reverse('admin:index'))
        assert len(response.context['app_list']) == 1
        assert response.context['app_list'][0]['app_label'] == 'test_app'
        assert len(response.context['app_list'][0]['models']) == 1
        assert response.context['app_list'][0]['models'][0]['object_name'] == 'TestModel1'

    def test_changeview_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1'))
        )
        assert response.status_code == 200

    def test_history_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_history' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )
        assert response.status_code == 200

    def test_add_view_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        assert response.status_code == 200

    def test_add_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        assert response.status_code == 403

    def test_change_view_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        assert response.status_code == 200


    def test_change_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )
        assert response.status_code == 200

    def test_delete_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )
        assert response.status_code == 403

