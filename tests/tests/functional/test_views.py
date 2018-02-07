from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django import VERSION
from django.conf import settings
from django.test import override_settings
from model_mommy import mommy

from tests.tests.helpers import AdminViewPermissionViewsTestCase

try:
    from django.urls import reverse
except ImportError:
    # django < 2.0
    from django.core.urlresolvers import reverse


class TestModelAdminViews(AdminViewPermissionViewsTestCase):

    # admin index

    def test_index_view_from_simple_user(self):
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(reverse('admin:index'))

        assert len(response.context['app_list']) == 1
        assert response.context['app_list'][0]['app_label'] == 'test_app'
        assert len(response.context['app_list'][0]['models']) == 1
        assert (response.context['app_list'][0]['models'][0]['object_name'] ==
                'TestModel1')

    def test_index_view_from_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(reverse('admin:index'))

        assert len(response.context['app_list']) == 2

    # changeview

    def test_changelist_view_get_from_user_with_v_perm_on_model1(self):
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')),
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Select test model1 to view'

    def test_changelist_view_get_from_user_with_vd_perm_on_model1(self):
        self.client.login(
            username='user_with_vd_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')),
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Select test model1 to view'

    def test_changelist_view_post_from_user_with_vd_perm_on_model1(self):
        obj = mommy.make('test_app.TestModel1')
        data = {
            'index': ['0'],
            'action': ['delete_selected'],
            'select_across': ['0'],
            '_selected_action': [str(obj.pk)]
        }
        self.client.login(
            username='user_with_vd_perm_on_model1',
            password='simple_user',
        )
        response = self.client.post(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')),
            data=data,
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Are you sure?'

    def test_changelist_view_get_from_simple_user_as_popup(self):
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(
            (reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')) +
             '?_to_field=id&_popup=1'),
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Select test model1'

    def test_changelist_view_get_from_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')),
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Select test model1 to change'

    # history

    def test_history_view_from_simple_user(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(
            reverse('admin:%s_%s_history' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        assert response.status_code == 200

    def test_history_view_from_super_user(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_history' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        assert response.status_code == 200

    # add

    def test_add_view_from_simple_user(self):
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1')),
        )

        assert response.status_code == 403

    def test_add_view_from_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1')),
        )

        assert response.status_code == 200

    # change

    def test_change_view_from_simple_user(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        assert response.status_code == 200

    def test_change_view_from_simple_user_translatable(self):
        """
        Smoke test: check if the change view renders for a django-parler model.
        """
        # Ensure parler's templates are registered through INSTALLED_APPS,
        # but only for this test. This mimics the install steps at
        # http://django-parler.readthedocs.io/en/latest/quickstart.html.
        current_installed_apps = settings.INSTALLED_APPS
        installed_apps_with_parler = current_installed_apps + ['parler']

        with override_settings(INSTALLED_APPS=installed_apps_with_parler):
            obj = mommy.make('test_app.TestModelParler')
            self.client.login(
                username='user_with_v_perm_on_model1parler',
                password='simple_user',
            )
            response = self.client.get(
                reverse(
                    'admin:%s_%s_change' % (
                        'test_app', 'testmodelparler'
                    ),
                    args=(obj.pk,)
                ),
            )
            assert response.status_code == 200

            # var4 is a translatable field on this model. Check that it is
            # marked as read only under Django versions supporting it.
            if VERSION[0:2] == (1, 11) or VERSION[0] == 2:
                bs = BeautifulSoup(response.content.decode('utf-8'),
                                   'html.parser')
                var4_tags = bs.select('.field-var4')
                assert len(var4_tags) == 1
                assert len(var4_tags[0].select('.readonly')) == 1

    def test_change_view_from_simple_user_unauthorized_post(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        data = {
            'var1': 'test',
            'var2': 'test',
            'var3': 1,
            'var4': mommy.make('test_app.TestModel0'),
            'testmodel2_set-TOTAL_FORMS': 0,
            'testmodel2_set-INITIAL_FORMS': 0,
            'testmodel3_set-TOTAL_FORMS': 0,
            'testmodel3_set-INITIAL_FORMS': 0
        }
        response = self.client.post(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
            data,
        )
        obj.refresh_from_db()

        assert response.status_code == 302
        assert obj.var1 != 'test'
        assert obj.var2 != 'test'
        assert obj.var3 != 1

    def test_change_view_from_super_user(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(obj.pk, )),
        )

        assert response.status_code == 200

    # delete

    def test_delete_view_from_simple_user(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.get(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        assert response.status_code == 403

    def test_delete_view_from_simple_user_unauthorized_post(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(
            username='user_with_v_perm_on_model1',
            password='simple_user',
        )
        response = self.client.post(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        obj.refresh_from_db()

        assert response.status_code == 403
        assert obj

    def test_delete_view_from_super_user(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        assert response.status_code == 200
