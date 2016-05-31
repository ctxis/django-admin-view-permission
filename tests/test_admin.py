from __future__ import unicode_literals

from django.test import SimpleTestCase, TestCase, Client
from django.contrib import admin as default_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from admin_view_permission.admin import *

from test_app.models import *



class TestAdminViewPermissionAdminSite(SimpleTestCase):

    def test_adminsite_class(self):
        self.assertIsInstance(default_admin.site,
                              AdminViewPermissionAdminSite)
        self.assertIsInstance(default_admin.sites.site,
                              AdminViewPermissionAdminSite)


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


class TestRegistration(SimpleTestCase):

    def test_model_modeladmin_append(self):
        self.assertIsInstance(default_admin.site._registry[TestModel1],
                              AdminViewPermissionModelAdmin)
        self.assertIsInstance(default_admin.site._registry[TestModel1],
                              default_admin.ModelAdmin)

    def test_other_model_modeladmin_append(self):
        for model in default_admin.site._registry:
            self.assertIsInstance(default_admin.site._registry[model],
                                  AdminViewPermissionModelAdmin)
            self.assertIsInstance(default_admin.site._registry[model],
                                  default_admin.ModelAdmin)


'''class TestAppsReady(SimpleTestCase):

    def setUp(self):
        self.appconfig = apps.get_app_config('admin_view_permission')
        self.admin_site = AdminViewPermissionAdminSite()

    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=['test_app.TestModel1',])
    def test_add_models_to_settings_option(self):
        self.appconfig.ready()
        self.admin_site.register(TestModel0)
        self.admin_site.register(TestModel1)
        self.admin_site.register(TestModel2)
        self.admin_site.register(TestModel3)

        for model in self.admin_site._registry:
            if model._meta.label == 'test_app.TestModel1':
                self.assertEqual(model._meta.permissions,
                                 (('view_testmodel1', 'Can view testmodel1'), ))
            else:
                self.assertEqual(model._meta.permissions, ())

    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=[])
    def test_empty_settings_option(self):
        self.appconfig.ready()
        self.admin_site.register(TestModel0)
        self.admin_site.register(TestModel1)
        self.admin_site.register(TestModel2)
        self.admin_site.register(TestModel3)

        for model in self.admin_site._registry:
            self.assertEqual(model._meta.permissions, ())'''


