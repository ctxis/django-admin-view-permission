from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from .helpers import AdminViewPermissionViewsTestCase


class TestModelAdminViews(AdminViewPermissionViewsTestCase):

## admin index

    def test_index_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(reverse('admin:index'))

        assert len(response.context['app_list']) == 1
        assert response.context['app_list'][0]['app_label'] == 'test_app'
        assert len(response.context['app_list'][0]['models']) == 1
        assert response.context['app_list'][0]['models'][0]['object_name'] == 'TestModel1'

    def test_index_view_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(reverse('admin:index'))

        assert len(response.context['app_list']) == 2

## changeview

    def test_changeview_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1'))
        )

        assert response.status_code == 200

## history

    def test_history_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_history' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )

        assert response.status_code == 200

## add

    def test_add_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )

        assert response.status_code == 403

    def test_add_view_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )

        assert response.status_code == 200

## change

    def test_change_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )

        assert response.status_code == 200

    def test_change_view_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk, ))
        )

        assert response.status_code == 200

## delete

    def test_delete_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )

        assert response.status_code == 403

