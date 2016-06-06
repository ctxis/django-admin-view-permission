from __future__ import unicode_literals

import pytest

from django.test import SimpleTestCase

from admin_view_permission.admin import AdminViewPermissionInlineModelAdmin, \
    AdminViewPermissionModelAdmin, AdminViewPermissionAdminSite

from .helpers import AdminViewPermissionTestCase, \
    AdminViewPermissionInlinesTestCase

from test_app.models import *


@pytest.mark.usefixtures("simple_request", "super_request")
class TestAdminViewPermissionModelAdmin(AdminViewPermissionTestCase):

## readonly_fields

    def test_get_readonly_fields_simple_user_1(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_2(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.simple_request, self.object_testmodel1)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_3(self):
        self.modeladmin_testmodel1.fields = ['id']
        self.modeladmin_testmodel1.readonly_fields = ('id',)
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_simple_user_4(self):
        self.modeladmin_testmodel1.fields = ['var1', 'var2']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('var1', 'var2')

    def test_get_readonly_fields_simple_user_5(self):
        self.modeladmin_testmodel1.fields = ['var1', 'func']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('var1', 'func')

    def test_get_readonly_fields_simple_user_6(self):
        readonly_fields = self.modeladmin_testmodel5.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('var0', 'var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_super_user_1(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_2(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.super_request, self.object_testmodel1)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_3(self):
        self.modeladmin_testmodel1.fields = ['id']
        self.modeladmin_testmodel1.readonly_fields = ('id',)
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_super_user_4(self):
        self.modeladmin_testmodel1.fields = ['var1', 'var2']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_5(self):
        self.modeladmin_testmodel1.fields = ['var1', 'func']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_6(self):
        readonly_fields = self.modeladmin_testmodel5.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ()

## get_fields

    def test_get_fields_simple_user_1(self):
        fields = self.modeladmin_testmodel1.get_fields(self.simple_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_simple_user_2(self):
        fields = self.modeladmin_testmodel1.get_fields(self.simple_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_1(self):
        fields = self.modeladmin_testmodel1.get_fields(self.super_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_2(self):
        fields = self.modeladmin_testmodel1.get_fields(self.super_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    ## get_actions

    def test_get_actions_simple_user(self):
        actions = self.modeladmin_testmodel1.get_actions(self.simple_request)

        assert not actions

    def test_get_actions_super_user(self):
        actions = self.modeladmin_testmodel1.get_actions(self.super_request)

        assert len(actions) == 1

## has_view_permission

    def test_has_view_permission_simple_user_1(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.simple_request)

    def test_has_view_permission_simple_user_2(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.simple_request, self.object_testmodel1)

    def test_has_view_permission_super_user_1(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.super_request)

    def test_has_view_permission_super_user_2(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.super_request, self.object_testmodel1)

## has_change_permission

    def test_has_change_permission_simple_user_1(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.simple_request)

    def test_has_change_permission_simple_user_2(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.simple_request, self.object_testmodel1)

    def test_has_change_permission_super_user_1(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.super_request)

    def test_has_change_permission_super_user_2(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.super_request, self.object_testmodel1)

## get_inline_instances

    def test_get_inline_instances_simple_user_1(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.simple_request)

        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_simple_user_2(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.simple_request)

        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_super_user_1(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.super_request)

        for inline in inlines:
            assert not isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_super_user_2(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.super_request)

        for inline in inlines:
            assert not isinstance(inline, AdminViewPermissionInlineModelAdmin)

        ## get_model_perms

    def test_get_model_perms_simple_user_1(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.simple_request) == {
                   'add': False,
                   'change': True,
                   'delete': False,
                   'view': True
               }

    def test_get_model_perms_simple_user_2(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.simple_request) == {
                   'add': False,
                   'change': True,
                   'delete': False,
                   'view': True
               }

    def test_get_model_perms_super_user_1(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.super_request) == {
                   'add': True,
                   'change': True,
                   'delete': True,
                   'view': True
               }

    def test_get_model_perms_super_user_2(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.super_request) == {
                   'add': True,
                   'change': True,
                   'delete': True,
                   'view': True
               }

## change_view

    def test_change_view_simple_user(self):
        change_view = self.modeladmin_testmodel1.change_view(
            self.simple_request, str(self.object_testmodel1.pk))

        assert change_view.context_data['title'] == 'View test model1'
        assert not change_view.context_data['show_save']
        assert not change_view.context_data['show_save_and_continue']

    def test_change_view_super_user(self):
        change_view = self.modeladmin_testmodel1.change_view(
            self.super_request, str(self.object_testmodel1.pk))

        assert change_view.context_data['title'] == 'Change test model1'


@pytest.mark.usefixtures("simple_request", "super_request")
class TestAdminViewPermissionInlineModelAdmin(
    AdminViewPermissionInlinesTestCase):

## readonly_fields

    def test_get_readonly_fields_simple_user_1(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_2(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.simple_request, self.object_testmodel1)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_3(self):
        self.inlinemodeladmin_testmodel4.fields = ['var1', 'var2']
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('var1', 'var2')

    def test_get_readonly_fields_simple_user_4(self):
        self.inlinemodeladmin_testmodel4.fields = ['id']
        self.inlinemodeladmin_testmodel4.readonly_fields = ('id',)
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_simple_user_5(self):
        readonly_fields = self.inlinemodeladmin_testmodel6.get_readonly_fields(
            self.simple_request)

        assert readonly_fields == ('var0', 'var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_super_user_1(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_2(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.super_request, self.object_testmodel1)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_3(self):
        self.inlinemodeladmin_testmodel4.fields = ['var1', 'var2']
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_4(self):
        self.inlinemodeladmin_testmodel4.fields = ['id']
        self.inlinemodeladmin_testmodel4.readonly_fields = ('id',)
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_super_user_5(self):
        readonly_fields = self.inlinemodeladmin_testmodel6.get_readonly_fields(
            self.super_request)

        assert readonly_fields == ()

## get_fields

    def test_get_fields_simple_user_1(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.simple_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_simple_user_2(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.simple_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_1(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.super_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_2(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.super_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']


class TestAdminViewPermissionAdminSite(SimpleTestCase):
    def setUp(self):
        self.admin_site = AdminViewPermissionAdminSite('admin')

    def test_register(self):
        self.admin_site.register(TestModel1)
        assert isinstance(self.admin_site._registry[TestModel1],
                          AdminViewPermissionModelAdmin)
