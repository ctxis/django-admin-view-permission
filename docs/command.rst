Management commands
===================

The admin view permission provides one management command which fixes the
permissions on the proxy models.


fix_proxy_permissions
---------------------
This command will create the appropriate entries on the `ContentType` and
`Permission` models. Then it will delete the permissions, which are created
from django `migrate` command and are associated with the parent model. More
information you can find `here <https://code.djangoproject.com/ticket/11154>_`.

Example
~~~~~~~
::

     python manage.py fix_proxy_permissions