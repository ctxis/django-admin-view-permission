from __future__ import unicode_literals
from admin_view_permission.admin import AdminViewPermissionModelAdmin
from django.contrib import admin
from django.test import SimpleTestCase


class TestTestAppModelAdminOverride(SimpleTestCase):

    def test_testapp_modeladmin_override(self):
        for model in admin.site._registry:
            assert isinstance(
                admin.site._registry[model], AdminViewPermissionModelAdmin)
            assert isinstance(
                admin.site._registry[model], admin.ModelAdmin)
