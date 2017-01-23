from __future__ import unicode_literals

from django.apps import apps
from django.db import models
from django.db.models.signals import post_migrate
from django.test import TestCase, override_settings


class TestAdminViewPermissionConfig(TestCase):
    def setUp(self):
        class Meta:
            permissions = (
                ("copy_apptestmodel3", "Can copy apptestmodel3"),
            )

        attrs_1 = {
            '__module__': 'tests.test_app.models',
        }
        attrs_2 = {
            '__module__': 'tests.test_app.models',
            'Meta': Meta,
        }

        self.appconfig = apps.get_app_config('test_app')
        self.model1 = type(str('AppTestModel1'), (models.Model, ),
                           attrs_1.copy())
        self.model2 = type(str('AppTestModel2'), (models.Model, ),
                           attrs_1.copy())
        self.model3 = type(str('AppTestModel3'), (models.Model, ),
                           attrs_2.copy())

    def trigger_signal(self):
        post_migrate.send(
            sender=self.appconfig,
            app_config=self.appconfig,
            verbosity=1,
            interactive=True,
            using='default')

    @override_settings(
        ADMIN_VIEW_PERMISSION_MODELS=['test_app.AppTestModel1', ]
    )
    def test_ready_with_one_model(self):
        self.trigger_signal()
        self.assertEqual(self.model1._meta.permissions,
                         [('view_apptestmodel1', 'Can view apptestmodel1'), ])
        self.assertEqual(self.model2._meta.permissions, [])

    @override_settings(
        ADMIN_VIEW_PERMISSION_MODELS=[]
    )
    def test_ready_without_model_list(self):
        self.trigger_signal()
        self.assertEqual(self.model1._meta.permissions, [])
        self.assertEqual(self.model2._meta.permissions, [])

    @override_settings(
        ADMIN_VIEW_PERMISSION_MODELS=()
    )
    def test_ready_without_model_tuple(self):
        self.trigger_signal()
        self.assertEqual(self.model1._meta.permissions, [])
        self.assertEqual(self.model2._meta.permissions, [])

    @override_settings(
        ADMIN_VIEW_PERMISSION_MODELS=None
    )
    def test_ready_with_none(self):
        self.trigger_signal()
        self.assertEqual(self.model1._meta.permissions,
                         [('view_apptestmodel1', 'Can view apptestmodel1'), ])
        self.assertEqual(self.model2._meta.permissions,
                         [('view_apptestmodel2', 'Can view apptestmodel2'), ])

    @override_settings(
        ADMIN_VIEW_PERMISSION_MODELS=['test_app.AppTestModel3', ]
    )
    def test_ready_with_other_permissions(self):
        self.trigger_signal()
        self.assertEqual(self.model3._meta.permissions,
                         ((u'copy_apptestmodel3', u'Can copy apptestmodel3'),
                          (u'view_apptestmodel3', u'Can view apptestmodel3')))

    @override_settings(
        ADMIN_VIEW_PERMISSION_MODELS=[]
    )
    def test_ready_with_other_permissions_and_with_none(self):
        self.trigger_signal()
        self.assertEqual(
            self.model3._meta.permissions,
            ((u'copy_apptestmodel3', u'Can copy apptestmodel3'), )
        )
