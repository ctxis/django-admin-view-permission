from __future__ import unicode_literals

from collections import OrderedDict, namedtuple

import pytest
from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.test import (
    RequestFactory,
    SimpleTestCase,
    TestCase,
    override_settings,
)
from model_mommy import mommy
from nose_parameterized import parameterized

from admin_view_permission.admin import (
    AdminViewPermissionAdminSite,
    AdminViewPermissionInlineModelAdmin,
    AdminViewPermissionModelAdmin,
)

from .helpers import (
    DataMixin,
    create_simple_user,
    create_super_user,
    create_urlconf,
)
from .test_app.admin import ModelAdmin1
from .test_app.models import TestModel1, TestModel5

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class TestAdminViewPermissionBaseModelAdmin(DataMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TestAdminViewPermissionBaseModelAdmin, cls).setUpTestData()

        # Users
        cls.user_without_permissions = create_simple_user()

        cls.user_with_a_perm_on_model1 = create_simple_user()
        cls.user_with_a_perm_on_model1.user_permissions.add(
            cls.add_permission_model1)

        cls.user_with_v_perm_on_model1 = create_simple_user()
        cls.user_with_v_perm_on_model1.user_permissions.add(
            cls.view_permission_model1)

        cls.user_with_c_perm_on_model1 = create_simple_user()
        cls.user_with_c_perm_on_model1.user_permissions.add(
            cls.change_permission_model1)

        cls.user_with_d_perm_on_model1 = create_simple_user()
        cls.user_with_d_perm_on_model1.user_permissions.add(
            cls.delete_permission_model1)

        cls.user_with_av_perm_on_model1 = create_simple_user()
        cls.user_with_av_perm_on_model1.user_permissions.add(
            cls.add_permission_model1,
            cls.view_permission_model1)

        cls.user_with_cv_perm_on_model1 = create_simple_user()
        cls.user_with_cv_perm_on_model1.user_permissions.add(
            cls.change_permission_model1,
            cls.view_permission_model1)

        cls.user_with_dv_perm_on_model1 = create_simple_user()
        cls.user_with_dv_perm_on_model1.user_permissions.add(
            cls.delete_permission_model1,
            cls.view_permission_model1)

        cls.user_with_avc_perm_on_model1 = create_simple_user()
        cls.user_with_avc_perm_on_model1.user_permissions.add(
            cls.add_permission_model1,
            cls.view_permission_model1,
            cls.change_permission_model1)

        cls.user_with_avcd_perm_on_model1 = create_simple_user()
        cls.user_with_avcd_perm_on_model1.user_permissions.add(
            cls.add_permission_model1,
            cls.view_permission_model1,
            cls.change_permission_model1,
            cls.delete_permission_model1)

        cls.user_with_v_perm_on_model5 = create_simple_user()
        cls.user_with_v_perm_on_model5.user_permissions.add(
            cls.view_permission_model5)

        cls.super_user = create_super_user()

    @classmethod
    def setUpClass(cls):
        super(TestAdminViewPermissionBaseModelAdmin, cls).setUpClass()
        cls.factory = RequestFactory()

    def setUp(self):
        self.admin_site = AdminSite(name='test_admin')

    RequestUser = namedtuple('RequestUser', 'user, view')

    # Modeladmin

    def _modeladmin_simple(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        return ModelAdmin1(TestModel1, self.admin_site)

    def _modeladmin_with_id_on_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, self.admin_site)
        modeladmin.fields = ['id']
        modeladmin.readonly_fields = ('id', )

        return modeladmin

    def _modeladmin_with_property_on_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, self.admin_site)
        modeladmin.fields = ['var1', 'var2', 'var3', 'var4', 'var5', 'var6']

        return modeladmin

    def _modeladmin_with_exclude_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, ModelAdmin1)
        modeladmin.exclude = ['var1']

        return modeladmin

    def _modeladmin_with_tuple_as_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, ModelAdmin1)
        modeladmin.fields = (('var1', 'var2'), 'var3', 'var4', 'var5', 'var6')

        return modeladmin

    def _modeladmin_with_form_containing_exclude_fields(self):

        class TestModel1Form(forms.ModelForm):
            class Meta:
                model = TestModel1
                exclude = ['var1']

        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, ModelAdmin1)
        modeladmin.form = TestModel1Form

        return modeladmin

    def _modeladmin_with_func_on_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, self.admin_site)
        modeladmin.fields = ['var1', 'func']

        return modeladmin

    # Objects

    def _obj_simple(self, obj_params):
        return TestModel1()

    GeneralParams = namedtuple(
        'GeneralParams', 'name, request_user, obj_func, obj_params, '
                         'modeladmin_func, result')

    general_params = [
        # Add objects
        GeneralParams(
            name='add_from_a_simple_user_without_permissions',
            request_user=RequestUser('user_without_permissions', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': False,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_add_permission',
            request_user=RequestUser('user_with_a_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': False,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_view_permission',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_view_permission_and_id_on'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_with_id_on_fields,
            result={
                'get_readonly_fields': ('id', ),
                'get_fields': ['id'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        # View permission only, var5 is a non-editable field and var6 is a
        # property field. Get_readonly_fields will return this field but the
        # change_view will raise FieldError on change_permission. This is
        # normal because the default modeladmin requires those field to be on
        # the readonly_fields option
        GeneralParams(
            name='add_from_a_simple_user_with_view_permission_and_property_on'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_with_property_on_fields,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4', 'var5',
                                        'var6'),
                'get_fields': ['var1', 'var2', 'var3', 'var4', 'var5', 'var6'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_view_permission_and_tuple_as'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_with_property_on_fields,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4', 'var5',
                                        'var6'),
                'get_fields': ['var1', 'var2', 'var3', 'var4', 'var5', 'var6'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_view_permission_and_func_on'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_with_func_on_fields,
            result={
                'get_readonly_fields': ('var1', 'func'),
                'get_fields': ['var1', 'func'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_view_permission_and_exclude'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_with_exclude_fields,
            result={
                'get_readonly_fields': ('var2', 'var3', 'var4'),
                'get_fields': ['var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_change_permission',
            request_user=RequestUser('user_with_c_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_delete_permission',
            request_user=RequestUser('user_with_d_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': False,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_add_view_permission',
            request_user=RequestUser('user_with_av_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_change_view_permission',
            request_user=RequestUser('user_with_cv_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_delete_view_permission',
            request_user=RequestUser('user_with_dv_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_add_view_change_permission',
            request_user=RequestUser('user_with_avc_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_simple_user_with_all_permissions',
            request_user=RequestUser('user_with_avcd_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        GeneralParams(
            name='add_from_a_super_user',
            request_user=RequestUser('super_user', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),

        # Change objects
        # TODO: exam why this happening, we expect all the fields
        GeneralParams(
            name='change_from_a_simple_user_without_permissions',
            request_user=RequestUser('user_without_permissions', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': False,
                    'change_only': False,
                },
            }
        ),
        # TODO: exam why this happening, we expect all the fields
        GeneralParams(
            name='change_from_a_simple_user_with_add_permission',
            request_user=RequestUser('user_with_a_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': False,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_view_permission',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_view_permission_and_id_on'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_with_id_on_fields,
            result={
                'get_readonly_fields': ('id',),
                'get_fields': ['id'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        # View permission only, var5 is a non-editable field and var6 is a
        # propery field. Get_readonly_fields will return this field but the
        # change_view will raise FieldError on change_permission. This is
        # normal because the default modeladmin requires those field to be on
        # the readonly_fields option
        GeneralParams(
            name='change_from_a_simple_user_with_view_permission_and_property'
                 '_on_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_with_property_on_fields,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4', 'var5',
                                        'var6'),
                'get_fields': ['var1', 'var2', 'var3', 'var4', 'var5', 'var6'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_view_permission_and_func_on'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_with_func_on_fields,
            result={
                'get_readonly_fields': ('var1', 'func'),
                'get_fields': ['var1', 'func'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_view_permission_and_exclude'
                 '_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_with_exclude_fields,
            result={
                'get_readonly_fields': ('var2', 'var3', 'var4'),
                'get_fields': ['var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_view_permission_and_custom_'
                 'form_with_exclude',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_with_form_containing_exclude_fields,
            result={
                'get_readonly_fields': ('var2', 'var3', 'var4'),
                'get_fields': ['var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_change_permission',
            request_user=RequestUser('user_with_c_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        # TODO: exam why this happening, we expect all the fields
        GeneralParams(
            name='change_from_a_simple_user_with_delete_permission',
            request_user=RequestUser('user_with_d_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': False,
                'has_change_permission': {
                    'default': False,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_add_view_permission',
            request_user=RequestUser('user_with_av_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_change_view_permission',
            request_user=RequestUser('user_with_cv_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_delete_view_permission',
            request_user=RequestUser('user_with_dv_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': ('var1', 'var2', 'var3', 'var4'),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': False,
                },
            }
        ),
        # TODO: exam why actions return something. We expect to return None
        GeneralParams(
            name='change_from_a_simple_user_with_add_view_change_permission',
            request_user=RequestUser('user_with_avc_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_all_permissions',
            request_user=RequestUser(
                'user_with_avcd_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
        GeneralParams(
            name='change_from_a_super_user',
            request_user=RequestUser('super_user', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_readonly_fields': (),
                'get_fields': ['var1', 'var2', 'var3', 'var4'],
                'has_view_permission': True,
                'has_change_permission': {
                    'default': True,
                    'change_only': True,
                },
            }
        ),
    ]

    @parameterized.expand(general_params)
    def test_get_readonly_fields(self, name, request_user, obj_func,
                                 obj_params, modeladmin_func, result):
        modeladmin = modeladmin_func(self)
        obj = obj_func(self, obj_params) if obj_func else None
        url_args = (obj.pk,) if obj else ()
        url = reverse(
            'test_admin:test_app_testmodel1_%s' % request_user.view,
            args=url_args,
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        readonly_fields = modeladmin.get_readonly_fields(request, obj)

        assert readonly_fields == result['get_readonly_fields']

    def test_get_readonly_fields__add_with_custom_id(self):
        """
        Normally the user with view permisssion will get a PermissionDenied
        from the add_view. The function must return all the fields as
        readonly
        """
        modeladmin = ModelAdmin1(TestModel5, self.admin_site)
        self.admin_site.register(TestModel5, ModelAdmin1)
        url = reverse(
            'test_admin:test_app_testmodel5_add',
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = self.user_with_v_perm_on_model5
        readonly_fields = modeladmin.get_readonly_fields(request)

        assert readonly_fields == ('var0', 'var1', 'var2', 'var3', 'var4')

    def test_get_readonly_fields__change_with_custom_id(self):
        modeladmin = ModelAdmin1(TestModel5, self.admin_site)
        self.admin_site.register(TestModel5, ModelAdmin1)
        obj = TestModel5()
        url = reverse(
            'test_admin:test_app_testmodel5_change',
            args=(1, ),
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = self.user_with_v_perm_on_model5
        readonly_fields = modeladmin.get_readonly_fields(request, obj)

        assert readonly_fields == ('var0', 'var1', 'var2', 'var3', 'var4')

    @parameterized.expand(general_params)
    def test_get_fields(self, name, request_user, obj_func, obj_params,
                        modeladmin_func, result):
        modeladmin = modeladmin_func(self)
        obj = obj_func(self, obj_params) if obj_func else None
        url_args = (obj.pk,) if obj else ()
        url = reverse(
            'admin:test_app_testmodel1_%s' % request_user.view,
            args=url_args,
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        readonly_fields = modeladmin.get_fields(request, obj)

        assert readonly_fields == result['get_fields']

    @parameterized.expand(general_params)
    def test_has_view_permission(self, name, request_user, obj_func,
                                 obj_params, modeladmin_func, result):
        modeladmin = modeladmin_func(self)
        obj = obj_func(self, obj_params) if obj_func else None
        url_args = (obj.pk,) if obj else ()
        url = reverse(
            'test_admin:test_app_testmodel1_%s' % request_user.view,
            args=url_args,
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        has_view_permission = modeladmin.has_view_permission(request)

        assert has_view_permission == result['has_view_permission']

    @parameterized.expand(general_params)
    def test_has_change_permission(self, name, request_user, obj_func,
                                   obj_params, modeladmin_func, result):
        modeladmin = modeladmin_func(self)
        obj = obj_func(self, obj_params) if obj_func else None
        url_args = (obj.pk,) if obj else ()
        url = reverse(
            'test_admin:test_app_testmodel1_%s' % request_user.view,
            args=url_args,
            urlconf=create_urlconf(self.admin_site)
        )
        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        has_change_permission_default = modeladmin.has_change_permission(
            request, obj=obj)
        has_change_permission_only = modeladmin.has_change_permission(
            request, obj=obj, only_change=True)

        assert (has_change_permission_default ==
                result['has_change_permission']['default'])
        assert (has_change_permission_only ==
                result['has_change_permission']['change_only'])

    ActionParams = namedtuple(
        'ActionParam', 'name, request_user, modeladmin_func, result')

    action_params = [
        # Add objects
        # Weird but the default implementation return the delete action
        # so we trust the view to return PermissionDenied
        ActionParams(
            name='simple_user_without_permissions',
            request_user=RequestUser('user_without_permissions', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        # Weird but the default implementation return the delete action
        # so we trust the view to return PermissionDenied
        ActionParams(
            name='add_from_a_simple_user_with_add_permission',
            request_user=RequestUser('user_with_a_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_view_permission',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: x == OrderedDict()},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_change_permission',
            request_user=RequestUser('user_with_c_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_delete_permission',
            request_user=RequestUser('user_with_d_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_add_view_permission',
            request_user=RequestUser('user_with_av_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: x == OrderedDict()},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_change_view_permission',
            request_user=RequestUser('user_with_cv_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_delete_view_permission',
            request_user=RequestUser('user_with_dv_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_add_view_change_permission',
            request_user=RequestUser('user_with_avc_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        ActionParams(
            name='add_from_a_simple_user_with_all_permissions',
            request_user=RequestUser('user_with_avcd_perm_on_model1', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),
        ActionParams(
            name='add_from_a_super_user',
            request_user=RequestUser('super_user', 'add'),
            modeladmin_func=_modeladmin_simple,
            result={'get_actions': lambda x: len(x) == 1},
        ),

    ]

    @parameterized.expand(action_params)
    def test_get_actions(self, name, request_user, modeladmin_func, result):
        modeladmin = modeladmin_func(self)
        url = reverse(
            'admin:test_app_testmodel1_%s' % request_user.view,
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        actions = modeladmin.get_actions(request)

        assert result['get_actions'](actions)


class TestAdminViewPermissionModelAdmin(DataMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TestAdminViewPermissionModelAdmin, cls).setUpTestData()

        # Users
        cls.user_without_permissions = create_simple_user()

        cls.user_with_a_perm = create_simple_user()
        cls.user_with_a_perm.user_permissions.add(
            cls.add_permission_model1,
        )

        cls.user_with_v_perm_on_model1 = create_simple_user()
        cls.user_with_v_perm_on_model1.user_permissions.add(
            cls.view_permission_model1,
        )

        cls.user_with_v_perm_on_model1_4 = create_simple_user()
        cls.user_with_v_perm_on_model1_4.user_permissions.add(
            cls.view_permission_model1,
            cls.view_permission_model4,
        )

        cls.user_with_av_perm_on_model1_4 = create_simple_user()
        cls.user_with_av_perm_on_model1_4.user_permissions.add(
            cls.view_permission_model1,
            cls.add_permission_model4,
        )

        cls.user_with_cv_perm_on_model1_4 = create_simple_user()
        cls.user_with_cv_perm_on_model1_4.user_permissions.add(
            cls.view_permission_model1,
            cls.change_permission_model4,
        )

        cls.user_with_dv_perm_on_model1_4 = create_simple_user()
        cls.user_with_dv_perm_on_model1_4.user_permissions.add(
            cls.view_permission_model1,
            cls.delete_permission_model4,
        )

        cls.user_with_vcd_perm_on_model1_4 = create_simple_user()
        cls.user_with_vcd_perm_on_model1_4.user_permissions.add(
            cls.view_permission_model1,
            cls.change_permission_model4,
            cls.delete_permission_model4,
        )

        cls.user_with_v_perm_on_model1_4_6 = create_simple_user()
        cls.user_with_v_perm_on_model1_4_6.user_permissions.add(
            cls.view_permission_model1,
            cls.view_permission_model4,
            cls.view_permission_model6,
        )

        cls.user_with_cv_perm_on_model1_4_6 = create_simple_user()
        cls.user_with_cv_perm_on_model1_4_6.user_permissions.add(
            cls.view_permission_model1,
            cls.view_permission_model4,
            cls.change_permission_model4,
            cls.view_permission_model6,
            cls.change_permission_model6,
        )

        cls.user_with_av_perm_on_model1_4_6 = create_simple_user()
        cls.user_with_av_perm_on_model1_4_6.user_permissions.add(
            cls.view_permission_model1,
            cls.view_permission_model4,
            cls.add_permission_model4,
            cls.view_permission_model6,
            cls.add_permission_model6,
        )

        cls.super_user = create_super_user()

    @classmethod
    def setUpClass(cls):
        super(TestAdminViewPermissionModelAdmin, cls).setUpClass()
        cls.factory = RequestFactory()

    def setUp(self):
        self.admin_site = AdminSite('test_admin')

    RequestUser = namedtuple('RequestUser', 'user, view')

    # Modeladmin

    def _modeladmin_simple(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        return ModelAdmin1(TestModel1, self.admin_site)

    def _modeladmin_with_id_on_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, self.admin_site)
        modeladmin.fields = ['id']
        modeladmin.readonly_fields = ('id',)

        return modeladmin

    def _modeladmin_with_property_on_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, self.admin_site)
        modeladmin.fields = ['var1', 'var2', 'var3', 'var4', 'var5', 'var6']

        return modeladmin

    def _modeladmin_with_func_on_fields(self):
        self.admin_site.register(TestModel1, ModelAdmin1)
        modeladmin = ModelAdmin1(TestModel1, self.admin_site)
        modeladmin.fields = ['var1', 'func']

        return modeladmin

    def _modeladmin_with_custom_id(self):
        return ModelAdmin1(TestModel5, self.admin_site)

    # Objects

    def _obj_simple(self, obj_params):
        return mommy.make('test_app.TestModel1', **obj_params)

    GeneralParams = namedtuple(
        'GeneralParams', 'name, request_user, obj_func, obj_params, '
                         'modeladmin_func, result')

    general_params = [
        # Add objects
        GeneralParams(
            name='add_from_a_user_with_view_permission_on_testmodel1',
            request_user=RequestUser('user_with_v_perm_on_model1', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {'count': 0, 'inlines': None},
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': None,
            }
        ),
        GeneralParams(
            name='add_from_a_user_with_view_permission_on_testmodel1_4',
            request_user=RequestUser('user_with_v_perm_on_model1_4', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 1,
                    'inlines': [
                        {'can_delete': False, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin}
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': None,
            }
        ),
        GeneralParams(
            name='add_from_a_user_with_view_permission_on_testmodel1_4_6',
            request_user=RequestUser('user_with_v_perm_on_model1_4_6', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': False, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': False, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': None,
            }
        ),
        GeneralParams(
            name='add_from_a_user_with_change_view_permission_on_'
                 'testmodel1_4_6',
            request_user=RequestUser('user_with_cv_perm_on_model1_4_6', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': True, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': True, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': None,
            }
        ),
        GeneralParams(
            name='add_from_a_user_with_add_view_permission_on_'
                 'testmodel1_4_6',
            request_user=RequestUser('user_with_av_perm_on_model1_4_6', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': False, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': False, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': None,
            }
        ),
        GeneralParams(
            name='add_from_a_super_user',
            request_user=RequestUser('super_user', 'add'),
            obj_func=None,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': True, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': True, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': True,
                    'change': True,
                    'delete': True,
                    'view': True,
                },
                'change_view': None,
            }
        ),

        # Change objects
        GeneralParams(
            name='change_from_a_user_with_view_permission_on_testmodel1',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {'count': 0, 'inlines': None},
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': False,
                        'show_save_and_continue': False,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_simple_user_with_view_permission_and_property'
                 '_on_fields',
            request_user=RequestUser('user_with_v_perm_on_model1', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_with_property_on_fields,
            result={
                'get_inline_instances': {'count': 0, 'inlines': None},
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': False,
                        'show_save_and_continue': False,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_user_with_view_permission_on_testmodel1_4',
            request_user=RequestUser('user_with_v_perm_on_model1_4', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 1,
                    'inlines': [
                        {'can_delete': False, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin}
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': False,
                        'show_save_and_continue': False,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_user_with_add_view_permission_on_'
                 'testmodel1_4',
            request_user=RequestUser(
                'user_with_av_perm_on_model1_4', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 1,
                    'inlines': [
                        {'can_delete': True, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin}
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': True,
                        'show_save_and_continue': True,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_user_with_change_view_permission_on_'
                 'testmodel1_4',
            request_user=RequestUser(
                'user_with_cv_perm_on_model1_4', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 1,
                    'inlines': [
                        {'can_delete': True, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin}
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': True,
                        'show_save_and_continue': True,
                    }
                },
            }
        ),
        # Here it's bit weird, but by default django needs change and delete
        # permission in order to be able to delete an inline, see next test.
        GeneralParams(
            name='change_from_a_user_with_delete_view_permission_on_'
                 'testmodel1_4',
            request_user=RequestUser(
                'user_with_dv_perm_on_model1_4', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 1,
                    'inlines': [
                        {'can_delete': True, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin}
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': False,
                        'show_save_and_continue': False,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_user_with_view_change_delete_permission_on_'
                 'testmodel1_4',
            request_user=RequestUser(
                'user_with_vcd_perm_on_model1_4', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 1,
                    'inlines': [
                        {'can_delete': True, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin}
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': True,
                        'show_save_and_continue': True,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_user_with_view_permission_on_testmodel1_4_6',
            request_user=RequestUser(
                'user_with_v_perm_on_model1_4_6', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': False, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': False, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': False,
                        'show_save_and_continue': False,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_user_with_change_view_permission_on_'
                 'testmodel1_4_6',
            request_user=RequestUser(
                'user_with_cv_perm_on_model1_4_6', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': True, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': True, 'max_num': 0,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': True,
                        'show_save_and_continue': True,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_user_with_add_view_permission_on_'
                 'testmodel1_4_6',
            request_user=RequestUser(
                'user_with_av_perm_on_model1_4_6', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': False, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': False, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': False,
                    'change': True,
                    'delete': False,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'View test model1',
                        'show_save': True,
                        'show_save_and_continue': True,
                    }
                },
            }
        ),
        GeneralParams(
            name='change_from_a_super_user',
            request_user=RequestUser('super_user', 'change'),
            obj_func=_obj_simple,
            obj_params={},
            modeladmin_func=_modeladmin_simple,
            result={
                'get_inline_instances': {
                    'count': 2,
                    'inlines': [
                        {'can_delete': True, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                        {'can_delete': True, 'max_num': None,
                         'class': AdminViewPermissionInlineModelAdmin},
                    ]
                },
                'get_model_perms': {
                    'add': True,
                    'change': True,
                    'delete': True,
                    'view': True,
                },
                'change_view': {
                    'status_code': 200,
                    'context_data': {
                        'title': 'Change test model1',
                    }
                },
            }
        ),
    ]

    @parameterized.expand(general_params)
    def test_get_inline_instances(self, name, request_user, obj_func,
                                  obj_params, modeladmin_func, result):
        modeladmin = modeladmin_func(self)
        obj = obj_func(self, obj_params) if obj_func else None
        url_args = (obj.pk,) if obj else ()
        url = reverse(
            'test_admin:test_app_testmodel1_%s' % request_user.view,
            args=url_args,
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        inlines = modeladmin.get_inline_instances(request, obj)

        assert len(inlines) == result['get_inline_instances']['count']
        if result['get_inline_instances']:
            for i, inline in enumerate(inlines):
                assert (inline.can_delete ==
                        result['get_inline_instances']['inlines'][i][
                            'can_delete'])
                assert (inline.max_num ==
                        result['get_inline_instances']['inlines'][i][
                            'max_num'])

    @parameterized.expand(general_params)
    def test_get_model_perms(self, name, request_user, obj_func,
                             obj_params, modeladmin_func, result):
        modeladmin = modeladmin_func(self)
        obj = obj_func(self, obj_params) if obj_func else None
        url_args = (obj.pk,) if obj else ()
        url = reverse(
            'test_admin:test_app_testmodel1_%s' % request_user.view,
            args=url_args,
            urlconf=create_urlconf(self.admin_site),
        )
        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        model_perms = modeladmin.get_model_perms(request)

        assert model_perms == result['get_model_perms']

    @parameterized.expand(general_params)
    def test_change_view(self, name, request_user, obj_func, obj_params,
                         modeladmin_func, result):
        if not result['change_view']:
            pytest.skip('not a case')

        modeladmin = modeladmin_func(self)
        obj = obj_func(self, obj_params) if obj_func else None
        url_args = (obj.pk,) if obj else ()
        url = reverse(
            'test_admin:test_app_testmodel1_%s' % request_user.view,
            args=url_args,
            urlconf=create_urlconf(self.admin_site)
        )

        request = self.factory.get(url)
        request.user = getattr(self, request_user.user)
        response = modeladmin.change_view(request, str(obj.pk))

        assert response.status_code == result['change_view']['status_code']
        assert (response.context_data['title'] ==
                result['change_view']['context_data']['title'])
        if 'show_save' in result['change_view']['context_data']:
            assert (response.context_data['show_save'] ==
                    result['change_view']['context_data']['show_save'])
        if 'show_save_and_continue' in result['change_view']['context_data']:
            assert (response.context_data['show_save_and_continue'] ==
                    result['change_view']['context_data'][
                        'show_save_and_continue'])


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
