Uninstall
=========

To remove the application completely firstly remove the ``admin_view_permission``
from your ``INSTALLED_APPS`` setting and then open a debug shell and execute
the following commands in order to remove these extra permissions from the
database::

    from django.contrib.auth.models import Permission
    permissions = Permission.objects.filter(codename__startswith='view')
    permissions.delete()

.. note:: Before delete the permission would be helpful to check if the
permissions queryset contains only the view permissions and not anything else.
