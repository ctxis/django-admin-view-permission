from __future__ import unicode_literals

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
        self.client.login(username='simple_user', password='simple_user')
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

    def test_changelist_view_from_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')),
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Select test model1 to view'

    def test_changelist_view_from_simple_user_as_popup(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            (reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')) +
             '?_to_field=id&_popup=1'),
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Select test model1'

    def test_changelist_view_from_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1')),
        )

        assert response.status_code == 200
        assert response.context['title'] == 'Select test model1 to change'

    # history

    def test_history_view_from_simple_user(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(username='simple_user', password='simple_user')
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
        self.client.login(username='simple_user', password='simple_user')
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
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        assert response.status_code == 200

    def test_change_view_from_simple_user_unauthorized_post(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(username='simple_user', password='simple_user')
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
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(obj.pk,)),
        )

        assert response.status_code == 403

    def test_delete_view_from_simple_user_unauthorized_post(self):
        obj = mommy.make('test_app.TestModel1')
        self.client.login(username='simple_user', password='simple_user')
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
