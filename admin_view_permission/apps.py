from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin
from django.apps import AppConfig
from django.apps import apps as global_apps
from django.db.models.signals import post_migrate

from .admin import AdminViewPermissionAdminSite
from .utils import django_version
from .enums import DjangoVersion


def update_permissions(sender, app_config, verbosity, apps=global_apps, **kwargs):
    settings_models = getattr(settings, 'ADMIN_VIEW_PERMISSION_MODELS', None)

    # TODO: Maybe look at the registry not in all models
    for app in apps.get_app_configs():
        for model in app.get_models():
            if settings_models or (settings_models is not None and len(
                    settings_models) == 0):

                if django_version() == DjangoVersion.DJANGO_18:
                    model_name = '%s.%s' %(model._meta.app_label,
                                           model._meta.object_name)
                elif django_version() > DjangoVersion.DJANGO_18:
                    model_name = model._meta.label

                if model_name in settings_models:
                    model._meta.permissions = (
                        ('view_%s' % model._meta.model_name,
                         'Can view %s' % model._meta.model_name),)
            else:
                model._meta.permissions = (
                    ('view_%s' % model._meta.model_name,
                     'Can view %s' % model._meta.model_name),)


class AdminViewPermissionConfig(AppConfig):
    name = 'admin_view_permission'

    def ready(self):
        if not isinstance(admin.site, AdminViewPermissionAdminSite):
            admin.site = AdminViewPermissionAdminSite('admin')
            admin.sites.site = admin.site

        post_migrate.connect(update_permissions)
