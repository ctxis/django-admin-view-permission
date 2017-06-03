from django.apps import apps
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from admin_view_permission.apps import update_permissions


class Command(BaseCommand):
    """
    Add permissions for proxy model. This is needed because of the
    bug https://code.djangoproject.com/ticket/11154.

    When a permission is created for a proxy model, it actually
    creates it for it's base model app_label (eg: for "article"
    instead of "about", for the About proxy model).
    """
    help = "Fix permissions for proxy models."

    def handle(self, *args, **options):
        update_permissions(
            apps.get_app_config('admin_view_permission'),
            apps.get_app_config('admin_view_permission'),
            verbosity=1,
            interactive=True,
            using='default',
        )

        for model in apps.get_models():
            opts = model._meta
            ctype, created = ContentType.objects.get_or_create(
                app_label=opts.app_label,
                model=opts.object_name.lower(),
            )

            for codename, name in _get_all_permissions(opts):
                p, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=ctype,
                    defaults={'name': name},
                )
                if created:
                    self.stdout.write('Adding permission {}\n'.format(p))
