from __future__ import unicode_literals

import pytest

from admin_view_permission.admin import AdminViewPermissionInlineModelAdmin

from .helpers import AdminViewPermissionTestCase, AdminViewPermissionInlinesTestCase


@pytest.mark.usefixtures("simple_add_request", "simple_change_request",
                         "super_add_request", "super_change_request",
                         "simple_changelist_request", "super_changelist_request")
class TestAdminViewPermissionModelAdmin(AdminViewPermissionTestCase):

## readonly_fields

    def test_get_readonly_fields_simple_user_1(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.simple_add_request)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_2(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.simple_change_request, self.object_testmodel1)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_super_user_1(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.super_add_request)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_2(self):
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.super_change_request, self.object_testmodel1)

        assert readonly_fields == ()

## get_fields

    def test_get_fields_simple_user_1(self):
        fields = self.modeladmin_testmodel1.get_fields(self.simple_add_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_simple_user_2(self):
        fields = self.modeladmin_testmodel1.get_fields(self.simple_change_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_1(self):
        fields = self.modeladmin_testmodel1.get_fields(self.super_add_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_2(self):
        fields = self.modeladmin_testmodel1.get_fields(self.super_change_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

## get_actions

    def test_get_actions_super_user(self):
        actions = self.modeladmin_testmodel1.get_actions(
            self.simple_changelist_request)

        assert not actions

    def test_get_actions_super_user(self):
        actions = self.modeladmin_testmodel1.get_actions(
            self.super_changelist_request)

        assert len(actions) == 1

## has_view_permission

    def test_has_view_permission_simple_user_1(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.simple_add_request)

    def test_has_view_permission_simple_user_2(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.simple_change_request, self.object_testmodel1)

    def test_has_view_permission_super_user_1(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.super_add_request)

    def test_has_view_permission_super_user_2(self):
        assert self.modeladmin_testmodel1.has_view_permission(
            self.super_change_request, self.object_testmodel1)

## has_change_permission

    def test_has_change_permission_simple_user_1(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.simple_add_request)

    def test_has_change_permission_simple_user_2(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.simple_change_request, self.object_testmodel1)


    def test_has_change_permission_super_user_1(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.super_add_request)

    def test_has_change_permission_super_user_2(self):
        assert self.modeladmin_testmodel1.has_change_permission(
            self.super_change_request, self.object_testmodel1)

## get_inline_instances

    def test_get_inline_instances_simple_user_1(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.simple_add_request)

        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_simple_user_2(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.simple_change_request)

        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_super_user_1(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.super_add_request)

        for inline in inlines:
            if inline.model._meta.model_name != 'testmodel4':
                assert not isinstance(inline,
                                      AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_super_user_2(self):
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.super_change_request)

        for inline in inlines:
            if inline.model._meta.model_name != 'testmodel4':
                assert not isinstance(inline,
                                      AdminViewPermissionInlineModelAdmin)

## get_model_perms

    def test_get_model_perms_simple_user_1(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.simple_add_request) == {
            'add': False,
            'change': True,
            'delete': False,
            'view': True
        }

    def test_get_model_perms_simple_user_2(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.simple_change_request) == {
            'add': False,
            'change': True,
            'delete': False,
            'view': True
        }

    def test_get_model_perms_super_user_1(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.super_add_request) == {
            'add': True,
            'change': True,
            'delete': True,
            'view': True
        }

    def test_get_model_perms_super_user_2(self):
        assert self.modeladmin_testmodel1.get_model_perms(
            self.super_change_request) == {
            'add': True,
            'change': True,
            'delete': True,
            'view': True
        }

## change_view

    def test_change_view_simple_user(self):
        change_view = self.modeladmin_testmodel1.change_view(
            self.simple_change_request, str(self.object_testmodel1.pk))

        assert change_view.context_data['title'] == 'View test model1'
        assert not change_view.context_data['show_save']
        assert not change_view.context_data['show_save_and_continue']

    def test_change_view_super_user(self):
        change_view = self.modeladmin_testmodel1.change_view(
            self.super_change_request, str(self.object_testmodel1.pk))

        assert change_view.context_data['title'] == 'Change test model1'


@pytest.mark.usefixtures("simple_add_request", "simple_change_request",
                         "super_add_request", "super_change_request",
                         "simple_changelist_request", "super_changelist_request")
class TestAdminViewPermissionInlineModelAdmin(AdminViewPermissionInlinesTestCase):

## readonly_fields

    def test_get_readonly_fields_simple_user_1(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.simple_add_request)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_2(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.simple_change_request, self.object_testmodel1)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_super_user_1(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.super_add_request)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_2(self):
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.super_change_request, self.object_testmodel1)

        assert readonly_fields == ()

## get_fields

    def test_get_fields_simple_user_1(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.simple_add_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_simple_user_2(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.simple_change_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_1(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.super_add_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_2(self):
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.super_change_request)

        assert fields == ['var1', 'var2', 'var3', 'var4']


'''class TestAdminViewPermissionAdminSite(SimpleTestCase):
    def test_adminsite_class(self):
        self.assertIsInstance(default_admin.site,
                              AdminViewPermissionAdminSite)
        self.assertIsInstance(default_admin.sites.site,
                              AdminViewPermissionAdminSite)



class TestRegistration(SimpleTestCase):
    def test_model_modeladmin_append(self):
        self.assertIsInstance(default_admin.site._registry[TestModel1],
                              AdminViewPermissionModelAdmin)
        self.assertIsInstance(default_admin.site._registry[TestModel1],
                              default_admin.ModelAdmin)

    def test_other_model_modeladmin_append(self):
        for model in default_admin.site._registry:
            self.assertIsInstance(default_admin.site._registry[model],
                                  AdminViewPermissionModelAdmin)
            self.assertIsInstance(default_admin.site._registry[model],
                                  default_admin.ModelAdmin)'''
