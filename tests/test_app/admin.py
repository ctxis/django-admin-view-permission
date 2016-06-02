from django.contrib import admin
from admin_view_permission import admin as view_admin
from .models import *


class StackedModelAdmin(admin.StackedInline):
    model = TestModel2


class TabularModelAdmin(admin.TabularInline):
    model = TestModel3


class ModelAdmin1(view_admin.AdminViewPermissionModelAdmin):
    inlines = [
        StackedModelAdmin,
        TabularModelAdmin
    ]

admin.site.register(TestModel1, ModelAdmin1)
