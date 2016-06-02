from django.test import SimpleTestCase, override_settings
from django.contrib import admin
from django.db import models

from admin_view_permission.apps import *

from test_app.models import *


class TestAdminViewPermissionConfig(SimpleTestCase):
    def setUp(self):
        attrs = {
            '__module__': 'tests.test_app.models',
        }

        self.appconfig = apps.get_app_config('admin_view_permission')
        self.model1 = type('AppTestModel1', (models.Model, ), attrs.copy())
        self.model2 = type('AppTestModel2', (models.Model, ), attrs.copy())


    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=['test_app.AppTestModel1', ])
    def test_ready_with_one_model(self):
        self.appconfig.ready()
        self.assertEqual(self.model1._meta.permissions,
                         (('view_apptestmodel1', 'Can view apptestmodel1'),))
        self.assertEqual(self.model2._meta.permissions, [])


    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=[])
    def test_read_without_model(self):
        self.appconfig.ready()
        self.assertEqual(self.model1._meta.permissions, [])
        self.assertEqual(self.model2._meta.permissions, [])


    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=())
    def test_read_without_model(self):
        self.appconfig.ready()
        self.assertEqual(self.model1._meta.permissions, [])
        self.assertEqual(self.model2._meta.permissions, [])


    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=None)
    def test_ready_with_none(self):
        self.appconfig.ready()
        self.assertEqual(self.model1._meta.permissions,
                         (('view_apptestmodel1', 'Can view apptestmodel1'),))
        self.assertEqual(self.model2._meta.permissions,
                         (('view_apptestmodel2', 'Can view apptestmodel2'),))
