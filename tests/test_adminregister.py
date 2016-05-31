from __future__ import unicode_literals

from django.test import SimpleTestCase, override_settings
from django.contrib import admin as default_admin
from django.apps import apps

from admin_view_permission.admin import *

from test_app.models import *


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
