from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase

User = get_user_model()


class TestFixProxyPermission(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestFixProxyPermission, cls).setUpClass()

        class Meta:
            proxy = True

        attrs = {
            '__module__': 'tests.test_app.models',
            'Meta': Meta,
        }

        cls.proxy_model = type(str('AppTestProxyModel'), (User, ),
                               attrs.copy())

    def test_fix_proxy_permissions_without_command_and_migration(self):
        model = self.proxy_model._meta.model_name
        ctypes = ContentType.objects.filter(model=model)
        permissions = Permission.objects.filter(
            codename__contains='apptestproxymodel')

        assert ctypes.count() == 0
        assert permissions.count() == 0

    def test_fix_proxy_permissions_without_migration(self):
        call_command('fix_proxy_permissions')
        model = self.proxy_model._meta.model_name
        ctypes = ContentType.objects.filter(model=model)
        permissions = Permission.objects.filter(
            codename__contains='apptestproxymodel')

        assert ctypes.count() == 1
        assert permissions.count() == 4

    def test_fix_proxy_permissions(self):
        call_command('migrate')
        call_command('fix_proxy_permissions')
        model = self.proxy_model._meta.model_name
        ctypes = ContentType.objects.filter(model=model)
        permissions = Permission.objects.filter(
            codename__contains='apptestproxymodel')

        assert ctypes.count() == 1
        assert permissions.count() == 4
