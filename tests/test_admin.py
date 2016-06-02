from __future__ import unicode_literals

from django.test import TestCase, Client, RequestFactory
from django.contrib import admin as default_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from admin_view_permission.admin import *

from test_app.models import *
from test_app.admin import ModelAdmin1


class TestAdminViewPermissionModelAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.modeladmin_testmodel1 = ModelAdmin1(TestModel1, admin.site)
        self.super_user = get_user_model().objects.create_superuser(
            username='super_user',
            email='',
            password='super_user',
        )
        self.simple_user = get_user_model().objects.create_user(
            username='simple_user',
            password='simple_user',
            is_staff=True
        )
        self.permission_testmodel1 = Permission.objects.get(
            name='Can view testmodel1')
        self.simple_user.user_permissions.set([self.permission_testmodel1])

        self.object_testmodel0 = TestModel0.objects.create(
            var1='Test',
            var2='Test',
            var3=5
        )
        self.object_testmodel1 = TestModel1.objects.create(
            var1='Test',
            var2='Test',
            var3=5,
        )
        self.object_testmodel1.var4.add(self.object_testmodel0)

    def test_get_readonly_fields_simple_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.simple_user
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            request)
        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_simple_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )
        request.user = self.simple_user
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            request, self.object_testmodel1)
        assert readonly_fields == ('var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields_super_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.super_user
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            request)
        assert readonly_fields == ()

    def test_get_readonly_fields_super_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )
        request.user = self.super_user
        readonly_fields = self.modeladmin_testmodel1.get_readonly_fields(
            request, self.object_testmodel1)
        assert readonly_fields == ()

    def test_get_fields_simple_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.simple_user
        fields = self.modeladmin_testmodel1.get_fields(
            request)
        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_simple_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.simple_user
        fields = self.modeladmin_testmodel1.get_fields(
            request)
        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.super_user
        fields = self.modeladmin_testmodel1.get_fields(
            request)
        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_fields_super_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.super_user
        fields = self.modeladmin_testmodel1.get_fields(
            request)
        assert fields == ['var1', 'var2', 'var3', 'var4']

    def test_get_actions_simple_user(self):
        request = self.factory.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1'))
        )
        request.user = self.super_user
        actions = self.modeladmin_testmodel1.get_actions(request)
        assert len(actions) == 1

    def test_get_actions_super_user(self):
        request = self.factory.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1'))
        )
        request.user = self.simple_user
        actions = self.modeladmin_testmodel1.get_actions(request)
        assert not actions

    def test_has_view_permission_simple_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.simple_user
        assert self.modeladmin_testmodel1.has_view_permission(request)

    def test_has_view_permission_simple_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.simple_user
        assert self.modeladmin_testmodel1.has_view_permission(request, self.object_testmodel1)

    def test_has_change_permission_simple_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.simple_user
        assert self.modeladmin_testmodel1.has_change_permission(request)

    def test_has_change_permission_simple_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.simple_user
        assert self.modeladmin_testmodel1.has_change_permission(request, self.object_testmodel1)

    def test_has_view_permission_super_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.super_user
        assert self.modeladmin_testmodel1.has_view_permission(request)

    def test_has_view_permission_super_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.super_user
        assert self.modeladmin_testmodel1.has_view_permission(request, self.object_testmodel1)

    def test_has_change_permission_super_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.super_user
        assert self.modeladmin_testmodel1.has_change_permission(request)

    def test_has_change_permission_super_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.super_user
        assert self.modeladmin_testmodel1.has_change_permission(request, self.object_testmodel1)

    def test_get_inline_instances_simple_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.simple_user
        inlines = self.modeladmin_testmodel1.get_inline_instances(request)
        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_simple_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.simple_user
        inlines = self.modeladmin_testmodel1.get_inline_instances(request)
        for inline in inlines:
            assert isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_super_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.super_user
        inlines = self.modeladmin_testmodel1.get_inline_instances(request)
        for inline in inlines:
            assert not isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_inline_instances_super_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.super_user
        inlines = self.modeladmin_testmodel1.get_inline_instances(request)
        for inline in inlines:
            assert not isinstance(inline, AdminViewPermissionInlineModelAdmin)

    def test_get_model_perms_simple_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.simple_user
        assert self.modeladmin_testmodel1.get_model_perms(request) == {
            'add': False,
            'change': True,
            'delete': False,
            'view': True
        }

    def test_get_model_perms_simple_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.simple_user
        assert self.modeladmin_testmodel1.get_model_perms(request) == {
            'add': False,
            'change': True,
            'delete': False,
            'view': True
        }

    def test_get_model_perms_super_user_1(self):
        request = self.factory.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = self.super_user
        assert self.modeladmin_testmodel1.get_model_perms(request) == {
            'add': True,
            'change': True,
            'delete': True,
            'view': True
        }

    def test_get_model_perms_super_user_2(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.super_user
        assert self.modeladmin_testmodel1.get_model_perms(request) == {
            'add': True,
            'change': True,
            'delete': True,
            'view': True
        }

    def test_change_view_simple_user(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.simple_user
        change_view = self.modeladmin_testmodel1.change_view(request, str(self.object_testmodel1.pk))
        assert change_view.context_data['title'] == 'View test model1'
        assert not change_view.context_data['show_save']
        assert not change_view.context_data['show_save_and_continue']

    def test_change_view_super_user(self):
        request = self.factory.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )
        request.user = self.super_user
        change_view = self.modeladmin_testmodel1.change_view(request, str(self.object_testmodel1.pk))
        assert change_view.context_data['title'] == 'Change test model1'


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
