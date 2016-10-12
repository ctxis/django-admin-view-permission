from __future__ import unicode_literals

import django
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib import admin

from .test_app.admin import ModelAdmin1, ModelAdmin2, InlineModelAdmin1, \
    InlineModelAdmin2
from .test_app.models import TestModel0, TestModel1, TestModel5, TestModel4


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        # Get the view permission for this model
        cls.view_permission_testmodel1 = Permission.objects.get(
            name='Can view testmodel1')
        cls.change_permission_testmodel1 = Permission.objects.get(
            name='Can change test model1')
        cls.add_permission_testmodel1 = Permission.objects.get(
            name='Can add test model1')
        cls.delete_permission_testmodel1 = Permission.objects.get(
            name='Can delete test model1')

        cls.add_permission_testmodel4 = Permission.objects.get(
            name='Can add test model4')
        cls.view_permission_testmodel4 = Permission.objects.get(
            name='Can view testmodel4')
        cls.change_permission_testmodel4 = Permission.objects.get(
            name='Can change test model4')

        cls.view_permission_testmodel5 = Permission.objects.get(
            name='Can view testmodel5')

        cls.add_permission_testmodel6 = Permission.objects.get(
            name='Can add test model6')
        cls.view_permission_testmodel6 = Permission.objects.get(
            name='Can view testmodel6')
        cls.change_permission_testmodel6 = Permission.objects.get(
            name='Can change test model6')

        # Create one object
        cls.object_testmodel0 = TestModel0.objects.create(
            var1='Test',
            var2='Test',
            var3=5
        )
        cls.object_testmodel1 = TestModel1.objects.create(
            var1='Test',
            var2='Test',
            var3=5,
        )
        cls.object_testmodel4 = TestModel4.objects.create(
            var1=cls.object_testmodel1,
            var2='Test',
            var4=5,
            var5='non editable field content',
        )
        cls.object_testmodel5 = TestModel5.objects.create(
            var1='Test',
            var2='Test',
            var3=5,
        )
        cls.object_testmodel1.var4.add(cls.object_testmodel0)
        cls.object_testmodel5.var4.add(cls.object_testmodel0)


    def create_simple_user(self):
        simple_user = get_user_model().objects.create_user(
            username='simple_user',
            password='simple_user',
        )
        # Django 1.8 compatibility
        simple_user.is_staff = True
        simple_user.save()

        return simple_user

    def create_super_user(self):
        super_user = get_user_model().objects.create_superuser(
            username='super_user',
            email='',
            password='super_user',
        )

        return super_user


class AdminViewPermissionTestCase(BaseTestCase):

    def setUp(self):
        # Create the modeladmin instance. (Note: right now we set the
        # TestModel1 to have as a ModelAdmin the ModelAdmin1 via the
        # assigned_modeladmin attr. In the other tests we have to change them)
        self.modeladmin_testmodel1 = ModelAdmin1(TestModel1, admin.site)
        self.modeladmin_testmodel5 = ModelAdmin1(TestModel5, admin.site)


class AdminViewPermissionInlinesTestCase(AdminViewPermissionTestCase):

    def setUp(self):
        # Refresh assigned_modeladmin attribute
        self.modeladmin_testmodel2 = ModelAdmin2(TestModel1, admin.site)
        self.inlinemodeladmin_testmodel4 = InlineModelAdmin1(TestModel1,
                                                            admin.site)
        self.inlinemodeladmin_testmodel6 = InlineModelAdmin2(TestModel1,
                                                            admin.site)


class AdminViewPermissionViewsTestCase(BaseTestCase):

    def setUp(self):
        self.client = Client()
        self.simple_user = self.create_simple_user()
        self.super_user = self.create_super_user()
        self.simple_user.user_permissions.add(self.view_permission_testmodel1)
        self.simple_user.user_permissions.add(self.view_permission_testmodel4)
        self.super_user.user_permissions.add(self.view_permission_testmodel1)

    def tearDown(self):
        self.client.logout()

