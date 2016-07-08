from __future__ import unicode_literals

import pytest

from django.test import SimpleTestCase
from django.test import override_settings
from django.contrib import admin

from admin_view_permission.admin import AdminViewPermissionInlineModelAdmin
from admin_view_permission.admin import AdminViewPermissionModelAdmin
from admin_view_permission.admin import AdminViewPermissionAdminSite

from .helpers import AdminViewPermissionTestCase
from .helpers import AdminViewPermissionInlinesTestCase

from .test_app.models import TestModel1


@pytest.mark.usefixtures("django_request")
class TestAdminViewPermissionBaseModelAdmin(AdminViewPermissionTestCase):

    ## readonly_fields

    def test_get_readonly_fields_simple_user_1(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_2(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(simple_user), self.object_testmodel1)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_3(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        self.modeladmin_testmodel1.fields = ['id']
        self.modeladmin_testmodel1.readonly_fields = ('id',)
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_simple_user_4(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        self.modeladmin_testmodel1.fields = ['var1', 'var2']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('var1', 'var2')

    def test_get_readonly_fields_simple_user_5(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        self.modeladmin_testmodel1.fields = ['var1', 'func']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('var1', 'func')

    def test_get_readonly_fields_simple_user_6(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel5)
        readonly_fields = self.modeladmin_testmodel5.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('var0', 'var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_super_user_1(self):
        super_user = self.create_super_user()
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_2(self):
        super_user = self.create_super_user()
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(super_user), self.object_testmodel1)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_3(self):
        super_user = self.create_super_user()
        self.modeladmin_testmodel1.fields = ['id']
        self.modeladmin_testmodel1.readonly_fields = ('id',)
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_super_user_4(self):
        super_user = self.create_super_user()
        self.modeladmin_testmodel1.fields = ['var1', 'var2']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_5(self):
        super_user = self.create_super_user()
        self.modeladmin_testmodel1.fields = ['var1', 'func']
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_6(self):
        super_user = self.create_super_user()
        readonly_fields = self.modeladmin_testmodel5.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ()

## get_fields

    def test_get_fields_simple_user_1(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        fields = self.modeladmin_testmodel1.get_fields(
            self.django_request(simple_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_simple_user_2(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        fields = self.modeladmin_testmodel1.get_fields(
            self.django_request(simple_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_1(self):
        super_user = self.create_super_user()
        fields = self.modeladmin_testmodel1.get_fields(
            self.django_request(super_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_2(self):
        super_user = self.create_super_user()
        fields = self.modeladmin_testmodel1.get_fields(
            self.django_request(super_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']

    ## get_actions

    def test_get_actions_simple_user(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        actions = self.modeladmin_testmodel1.get_actions(
            self.django_request(simple_user))

        assert not actions

    def test_get_actions_super_user(self):
        super_user = self.create_super_user()
        actions = self.modeladmin_testmodel1.get_actions(
            self.django_request(super_user))

        assert len(actions) == 1

## has_view_permission

    def test_has_view_permission_simple_user_1(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        assert self.modeladmin_testmodel1.has_view_permission(
            self.django_request(simple_user))

    def test_has_view_permission_simple_user_2(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        assert self.modeladmin_testmodel1.has_view_permission(
            self.django_request(simple_user), self.object_testmodel1)

    def test_has_view_permission_super_user_1(self):
        super_user = self.create_super_user()
        assert self.modeladmin_testmodel1.has_view_permission(
            self.django_request(super_user))

    def test_has_view_permission_super_user_2(self):
        super_user = self.create_super_user()
        assert self.modeladmin_testmodel1.has_view_permission(
            self.django_request(super_user), self.object_testmodel1)

## has_change_permission

    def test_has_change_permission_simple_user_1(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        assert self.modeladmin_testmodel1.has_change_permission(
            self.django_request(simple_user))

    def test_has_change_permission_simple_user_2(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        assert self.modeladmin_testmodel1.has_change_permission(
            self.django_request(simple_user), self.object_testmodel1)

    def test_has_change_permission_super_user_1(self):
        super_user = self.create_super_user()
        assert self.modeladmin_testmodel1.has_change_permission(
            self.django_request(super_user))

    def test_has_change_permission_super_user_2(self):
        super_user = self.create_super_user()
        assert self.modeladmin_testmodel1.has_change_permission(
            self.django_request(super_user), self.object_testmodel1)


@pytest.mark.usefixtures("django_request")
class TestAdminViewPermissionModelAdmin(AdminViewPermissionTestCase):

## get_inline_instances

    def test_get_inline_instances_simple_user_1(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.django_request(simple_user))

        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_super_user_1(self):
        super_user = self.create_super_user()
        inlines = self.modeladmin_testmodel1.get_inline_instances(
            self.django_request(super_user))

        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

## get_model_perms

    def test_get_model_perms_simple_user_1(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        assert self.modeladmin_testmodel1.get_model_perms(
            self.django_request(simple_user)) == {
                   'add': False,
                   'change': True,
                   'delete': False,
                   'view': True
               }

    def test_get_model_perms_simple_user_2(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        assert self.modeladmin_testmodel1.get_model_perms(
            self.django_request(simple_user)) == {
                   'add': False,
                   'change': True,
                   'delete': False,
                   'view': True
               }

    def test_get_model_perms_super_user_1(self):
        super_user = self.create_super_user()
        assert self.modeladmin_testmodel1.get_model_perms(
            self.django_request(super_user)) == {
                   'add': True,
                   'change': True,
                   'delete': True,
                   'view': True
               }

    def test_get_model_perms_super_user_2(self):
        super_user = self.create_super_user()
        assert self.modeladmin_testmodel1.get_model_perms(
            self.django_request(super_user)) == {
                   'add': True,
                   'change': True,
                   'delete': True,
                   'view': True
               }

## change_view

    def test_change_view_simple_user(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel1)
        change_view = self.modeladmin_testmodel1.change_view(
            self.django_request(simple_user), str(self.object_testmodel1.pk))

        assert change_view.context_data['title'] == 'View test model1'
        assert not change_view.context_data['show_save']
        assert not change_view.context_data['show_save_and_continue']

    def test_change_view_super_user(self):
        super_user = self.create_super_user()
        change_view = self.modeladmin_testmodel1.change_view(
            self.django_request(super_user), str(self.object_testmodel1.pk))

        assert change_view.context_data['title'] == 'Change test model1'


@pytest.mark.usefixtures("django_request")
class TestAdminViewPermissionInlineModelAdmin(
    AdminViewPermissionInlinesTestCase):

## readonly_fields

    def test_get_readonly_fields_simple_user_1(self):
        simple_user = self.create_simple_user()
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_simple_user_2(self):
        simple_user = self.create_simple_user()
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user), self.object_testmodel1)

        assert readonly_fields == ()

    def test_get_readonly_fields_simple_user_3(self):
        simple_user = self.create_simple_user()
        self.inlinemodeladmin_testmodel4.fields = ['var1', 'var2']
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_simple_user_4(self):
        simple_user = self.create_simple_user()
        self.inlinemodeladmin_testmodel4.fields = ['id']
        self.inlinemodeladmin_testmodel4.readonly_fields = ('id',)
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_simple_user_5(self):
        simple_user = self.create_simple_user()
        readonly_fields = self.inlinemodeladmin_testmodel6.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_simple_user_6(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel4)
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_7(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel4)
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user), self.object_testmodel1)

        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_8(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel4)
        self.inlinemodeladmin_testmodel4.fields = ['var1', 'var2']
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('var1', 'var2')

    def test_get_readonly_fields_simple_user_9(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel4)
        self.inlinemodeladmin_testmodel4.fields = ['id']
        self.inlinemodeladmin_testmodel4.readonly_fields = ('id',)
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(simple_user))

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_super_user_1(self):
        super_user = self.create_super_user()
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_2(self):
        super_user = self.create_super_user()
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(super_user), self.object_testmodel1)

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_3(self):
        super_user = self.create_super_user()
        self.inlinemodeladmin_testmodel4.fields = ['var1', 'var2']
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_4(self):
        super_user = self.create_super_user()
        self.inlinemodeladmin_testmodel4.fields = ['id']
        self.inlinemodeladmin_testmodel4.readonly_fields = ('id',)
        readonly_fields = self.inlinemodeladmin_testmodel4.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ('id',)

    def test_get_readonly_fields_super_user_5(self):
        super_user = self.create_super_user()
        readonly_fields = self.inlinemodeladmin_testmodel6.get_readonly_fields(
            self.django_request(super_user))

        assert readonly_fields == ()

## get_fields

    def test_get_fields_simple_user_1(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel4)
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.django_request(simple_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_simple_user_2(self):
        simple_user = self.create_simple_user()
        simple_user.user_permissions.add(self.view_permission_testmodel4)
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.django_request(simple_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_1(self):
        super_user = self.create_super_user()
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.django_request(super_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_2(self):
        super_user = self.create_super_user()
        fields = self.inlinemodeladmin_testmodel4.get_fields(
            self.django_request(super_user))

        assert fields == ['var1', 'var2', 'var3', 'var4']


class TestAdminViewPermissionAdminSite(SimpleTestCase):
    def setUp(self):
        self.admin_site = AdminViewPermissionAdminSite('admin')

    def test_register_1(self):
        self.admin_site.register(TestModel1)
        assert isinstance(self.admin_site._registry[TestModel1],
                          AdminViewPermissionModelAdmin)

    def test_register_2(self):
        modeladmin1 = type(str('TestModelAdmin1'), (admin.ModelAdmin, ), {})
        self.admin_site.register(TestModel1, modeladmin1)
        assert isinstance(self.admin_site._registry[TestModel1],
                          AdminViewPermissionModelAdmin)
        assert isinstance(self.admin_site._registry[TestModel1],
                          modeladmin1)

    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=['test_app.TestModel1', ])
    def test_register_3(self):
        self.admin_site.register(TestModel1)
        assert isinstance(self.admin_site._registry[TestModel1],
                          AdminViewPermissionModelAdmin)

    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=['test_app.TestModel1', ])
    def test_register_4(self):
        modeladmin1 = type(str('TestModelAdmin1'), (admin.ModelAdmin, ), {})
        self.admin_site.register(TestModel1, modeladmin1)
        assert isinstance(self.admin_site._registry[TestModel1],
                          AdminViewPermissionModelAdmin)
        assert isinstance(self.admin_site._registry[TestModel1],
                          modeladmin1)

    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=[])
    def test_register_5(self):
        self.admin_site.register(TestModel1)
        assert not isinstance(self.admin_site._registry[TestModel1],
                          AdminViewPermissionModelAdmin)

    @override_settings(ADMIN_VIEW_PERMISSION_MODELS=())
    def test_register_6(self):
        self.admin_site.register(TestModel1)
        assert not isinstance(self.admin_site._registry[TestModel1],
                          AdminViewPermissionModelAdmin)

