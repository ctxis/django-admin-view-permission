from __future__ import unicode_literals

from django.test import SimpleTestCase
from django.contrib import admin as default_admin

from admin_view_permission.admin import *


class TestAdminSite(SimpleTestCase):

    def test_adminsite_class(self):
        self.assertIsInstance(default_admin.site,
                              AdminViewPermissionAdminSite)
        self.assertIsInstance(default_admin.sites.site,
                              AdminViewPermissionAdminSite)



