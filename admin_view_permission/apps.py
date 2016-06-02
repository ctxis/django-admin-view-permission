from __future__ import unicode_literals

from django.conf import settings
from django.apps import AppConfig, apps
from django.contrib import admin

from .admin import AdminViewPermissionAdminSite


class AdminViewPermissionConfig(AppConfig):
    name = 'admin_view_permission'

    def ready(self):
        settings_models = getattr(settings, 'ADMIN_VIEW_PERMISSION_MODELS',
                                  None)

        if not isinstance(admin.site, AdminViewPermissionAdminSite):
            admin.site = AdminViewPermissionAdminSite('admin')
            admin.sites.site = admin.site

        # TODO: Maybe look at the registry not in all models
        for app in apps.get_app_configs():
            for model in app.get_models():
                if settings_models or (settings_models is not None and len(
                        settings_models) == 0):
                    if model._meta.label in settings_models:
                        model._meta.permissions = (
                            ('view_%s' % model._meta.model_name,
                             'Can view %s' % model._meta.model_name),)
                else:
                    model._meta.permissions = (
                        ('view_%s' % model._meta.model_name,
                         'Can view %s' % model._meta.model_name),)
