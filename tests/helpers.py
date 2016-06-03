from __future__ import unicode_literals

import pytest

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib import admin

from test_app.models import *
from test_app.admin import ModelAdmin1


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        # Create the modeladmin instance
        cls.modeladmin_testmodel1 = ModelAdmin1(TestModel1, admin.site)
        # Create two users
        cls.super_user = get_user_model().objects.create_superuser(
            username='super_user',
            email='',
            password='super_user',
        )
        cls.simple_user = get_user_model().objects.create_user(
            username='simple_user',
            password='simple_user',
            is_staff=True
        )
        # Get the view permission for this model
        cls.permission_testmodel1 = Permission.objects.get(
            name='Can view testmodel1')
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
        cls.object_testmodel1.var4.add(cls.object_testmodel0)


class AdminViewPermissionTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(AdminViewPermissionTestCase, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.simple_user.user_permissions.set([cls.permission_testmodel1])


class AdminViewPermissionViewsTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(AdminViewPermissionViewsTestCase, cls).setUpClass()
        cls.client = Client()
        cls.simple_user.user_permissions.set([cls.permission_testmodel1])
        cls.super_user.user_permissions.set([cls.permission_testmodel1])

    @classmethod
    def tearDownClass(cls):
        cls.client.logout()
        super(AdminViewPermissionViewsTestCase, cls).tearDownClass()


