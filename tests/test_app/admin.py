from __future__ import unicode_literals

from django.contrib import admin
from parler.admin import TranslatableAdmin

from admin_view_permission import admin as view_admin

from .models import *  # noqa: F403


# Modeladmin for the UI
class StackedModelAdmin(admin.StackedInline):
    model = TestModel2


class TabularModelAdmin(admin.TabularInline):
    model = TestModel3


class DefaultModelAdmin(admin.ModelAdmin):
    inlines = [
        StackedModelAdmin,
        TabularModelAdmin
    ]


admin.site.register(TestModel1, DefaultModelAdmin)


class TestModelParlerAdmin(TranslatableAdmin, admin.ModelAdmin):
    model = TestModelParler


admin.site.register(TestModelParler, TestModelParlerAdmin)


# Modeladmin for testing
class StackedModelAdmin1(admin.StackedInline):
    model = TestModel4


class TabularModelAdmin2(admin.TabularInline):
    model = TestModel6


class ModelAdmin1(view_admin.AdminViewPermissionModelAdmin):
    inlines = [
        StackedModelAdmin1,
        TabularModelAdmin2,
    ]
