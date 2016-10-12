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
