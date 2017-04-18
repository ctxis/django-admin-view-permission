from __future__ import unicode_literals

import django

from .enums import DjangoVersion


def django_version():
    if django.get_version().startswith('1.9'):
        return DjangoVersion.DJANGO_19
    elif django.get_version().startswith('1.8'):
        return DjangoVersion.DJANGO_18
    elif django.get_version().startswith('1.10'):
        return DjangoVersion.DJANGO_110
    elif django.get_version().startswith('1.11'):
        return DjangoVersion.DJANGO_111


def get_model_name(model):
    if django_version() == DjangoVersion.DJANGO_18:
        model_name = '%s.%s' % (model._meta.app_label,
                                model._meta.object_name)
    elif django_version() > DjangoVersion.DJANGO_18:
        model_name = model._meta.label

    return model_name
