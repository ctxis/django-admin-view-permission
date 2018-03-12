from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from model_mommy import mommy
from model_mommy.recipe import seq

SIMPLE_USERNAME = seq('simple_user_')
SUPER_USERNAME = seq('super_user_')


def create_simple_user(username=None):
    if not username:
        username = SIMPLE_USERNAME

    simple_user = mommy.make(get_user_model(), username=username)
    simple_user.set_password('simple_user')
    # Django 1.8 compatibility
    simple_user.is_staff = True
    simple_user.save()

    return simple_user


def create_super_user(username=None):
    if not username:
        username = SUPER_USERNAME

    super_user = mommy.make(
        get_user_model(),
        username=username, is_superuser=True)
    super_user.set_password('super_user')
    # Django 1.8 compatibility
    super_user.is_staff = True
    super_user.save()

    return super_user


def create_urlconf(admin_site):
    return type(
        str('Urlconf'),
        (object,),
        {'urlpatterns': [
            url('test_admin/', admin_site.urls)
        ]}
    )


class DataMixin(object):

    @classmethod
    def setUpTestData(cls):
        # Permissions
        cls.add_permission_model1 = Permission.objects.get(
            name='Can add test model1')
        cls.view_permission_model1 = Permission.objects.get(
            name='Can view testmodel1')
        cls.change_permission_model1 = Permission.objects.get(
            name='Can change test model1')
        cls.delete_permission_model1 = Permission.objects.get(
            name='Can delete test model1')

        cls.view_permission_model1parler = Permission.objects.get(
            name='Can view testmodelparler'
        )
        cls.view_permission_model1parlertranslation = Permission.objects.get(
            name='Can view testmodelparlertranslation'
        )

        cls.add_permission_model4 = Permission.objects.get(
            name='Can add test model4')
        cls.view_permission_model4 = Permission.objects.get(
            name='Can view testmodel4')
        cls.change_permission_model4 = Permission.objects.get(
            name='Can change test model4')
        cls.delete_permission_model4 = Permission.objects.get(
            name='Can delete test model4')

        cls.add_permission_model5 = Permission.objects.get(
            name='Can add test model5')
        cls.view_permission_model5 = Permission.objects.get(
            name='Can view testmodel5')
        cls.change_permission_model5 = Permission.objects.get(
            name='Can change test model5')
        cls.delete_permission_model5 = Permission.objects.get(
            name='Can delete test model5')

        cls.add_permission_model6 = Permission.objects.get(
            name='Can add test model6')
        cls.view_permission_model6 = Permission.objects.get(
            name='Can view testmodel6')
        cls.change_permission_model6 = Permission.objects.get(
            name='Can change test model6')
        cls.delete_permission_model6 = Permission.objects.get(
            name='Can delete test model6')


class AdminViewPermissionViewsTestCase(DataMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super(AdminViewPermissionViewsTestCase, cls).setUpTestData()

        cls.user_with_v_perm_on_model1 = create_simple_user(
            username='user_with_v_perm_on_model1',
        )
        cls.user_with_v_perm_on_model1.user_permissions.add(
            cls.view_permission_model1,
        )

        cls.user_with_vd_perm_on_moedl1 = create_simple_user(
            username='user_with_vd_perm_on_model1',
        )
        cls.user_with_vd_perm_on_moedl1.user_permissions.add(
            cls.view_permission_model1,
            cls.delete_permission_model1,
        )

        cls.user_with_v_perm_on_model1parler = create_simple_user(
            username='user_with_v_perm_on_model1parler'
        )
        cls.user_with_v_perm_on_model1parler.user_permissions.add(
            cls.view_permission_model1parler,
        )
        cls.user_with_v_perm_on_model1parler.user_permissions.add(
            cls.view_permission_model1parlertranslation,
        )

        cls.super_user = create_super_user(username='super_user')

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        self.client.logout()
