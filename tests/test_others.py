from __future__ import unicode_literals

from django.contrib import admin
from django.test import SimpleTestCase

from admin_view_permission.admin import AdminViewPermissionModelAdmin


class TestTestAppModelAdminOverride(SimpleTestCase):

    def test_testapp_modeladmin_override_1(self):
        for model in admin.site._registry:
            assert isinstance(admin.site._registry[model],
                              AdminViewPermissionModelAdmin)
            assert isinstance(admin.site._registry[model], admin.ModelAdmin)
