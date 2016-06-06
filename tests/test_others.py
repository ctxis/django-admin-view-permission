from __future__ import unicode_literals

from django.test import SimpleTestCase

from admin_view_permission.admin import *


class TestTestAppModelAdminOverride(SimpleTestCase):

    def test_testapp_modeladmin_override_1(self):
        for model in admin.site._registry:
            assert isinstance(admin.site._registry[model],
                              AdminViewPermissionModelAdmin)
            assert isinstance(admin.site._registry[model], admin.ModelAdmin)