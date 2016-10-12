=====================
Admin View Permission
=====================

.. image:: https://travis-ci.org/ctxis/django-admin-view-permission.svg?branch=master
    :target: https://travis-ci.org/ctxis/django-admin-view-permission
    :alt: Build Status
.. image:: https://coveralls.io/repos/github/ctxis/django-admin-view-permission/badge.svg?branch=master
   :target: https://coveralls.io/github/ctxis/django-admin-view-permission?branch=master
   :alt: Coverage Status
.. image:: https://codeclimate.com/github/ctxis/django-admin-view-permission/badges/gpa.svg
   :target: https://codeclimate.com/github/ctxis/django-admin-view-permission
   :alt: Code Climate

Reusable application which provides a view permission for the existing models.

Requirements
------------

* Django

Support
-------

* Django: 1.8, 1.9, 1.10
* Python: 2.7, 3.4, 3.5

Documentation
-------------
For a full documentation you can visit: http://django-admin-view-permission.readthedocs.org/

Setup
-----

* ``pip install django-admin-view-permission``

and then add ``admin_view_permission`` at the INSTALLED_APPS like this::

    INSTALLED_APPS = [
        'admin_view_permission',
        'django.contrib.admin',
        ...
    ]

and finally run ``python manage.py migrate``.

Configuration
-------------

This app provides a setting::

    ADMIN_VIEW_PERMISSION_MODELS = [
        auth.User,
        ...
    ]

in which you can provide which models you want to be added the view permission.
If you don't specify this setting then the view permission will be applied to
all the models.

Uninstall
---------

1. Remove the ``admin_view_permission`` from your ``INSTALLED_APPS`` setting
2. Delete the view permissions from the database::

        from django.contrib.auth.models import Permission
        permissions = Permission.objects.filter(codename__startswith='view')
        permissions.delete()

   It will be helpful to check if the queryset contains only the view
   permissions and not anything else (for example: custom permission added)
