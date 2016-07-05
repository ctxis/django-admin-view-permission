Configuration
=============

The admin view permission provides one setting that you can add in your project's
settings module to customize its behavior.

ADMIN_VIEW_PERMISSION_MODELS
----------------------------

This setting defines which models you want to be added the view permission. If
you don't specify this setting then the view permission will be applied to all
the models.

Example
~~~~~~~
::

     ADMIN_VIEW_PERMISSION_MODELS = [
         auth.User,
         ...
     ]