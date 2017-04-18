from __future__ import unicode_literals

from django.test import SimpleTestCase

from admin_view_permission.enums import DjangoVersion
from admin_view_permission.utils import django_version, get_model_name

from .test_app.models import TestModel1

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestUtils(SimpleTestCase):

    @patch('django.get_version', lambda: '1.8')
    def test_django_version_with_django_18(self):
        assert django_version() == DjangoVersion.DJANGO_18

    @patch('django.get_version', lambda: '1.9')
    def test_django_version_with_django_19(self):
        assert django_version() == DjangoVersion.DJANGO_19

    @patch('django.get_version', lambda: '1.10')
    def test_django_version_with_django_110(self):
        assert django_version() == DjangoVersion.DJANGO_110

    @patch('django.get_version', lambda: '1.11')
    def test_django_version_with_django_111(self):
        assert django_version() == DjangoVersion.DJANGO_111

    @patch('django.get_version', lambda: '1.8')
    def test_get_model_name_with_django_18(self):
        assert get_model_name(TestModel1) == 'test_app.TestModel1'

    @patch('django.get_version', lambda: '1.9')
    def test_get_model_name_with_django_bigger_than_18(self):
        assert get_model_name(TestModel1) == 'test_app.TestModel1'
