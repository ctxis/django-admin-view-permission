from django.contrib import admin
from admin_view_permission import admin as view_admin
from .models import *


class StackedModelAdmin(admin.StackedInline):
    model = TestModel2


class TabularModelAdmin(admin.TabularInline):
    model = TestModel3


class InlineModelAdmin1(view_admin.AdminViewPermissionInlineModelAdmin):
    model = TestModel4


class ModelAdmin1(view_admin.AdminViewPermissionModelAdmin):
    inlines = [
        StackedModelAdmin,
        TabularModelAdmin,
        InlineModelAdmin1
    ]

admin.site.register(TestModel1, ModelAdmin1)
