from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from .helpers import AdminViewPermissionViewsTestCase

from .test_app.models import TestModel1


class TestModelAdminViews(AdminViewPermissionViewsTestCase):

## admin index

    def test_index_view_simple_user(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.get(reverse('admin:index'))

        assert len(response.context['app_list']) == 1
        assert response.context['app_list'][0]['app_label'] == 'test_app'
        assert len(response.context['app_list'][0]['models']) == 2
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

    def test_change_view_property_field_shown(self):
        self.client.login(username='simple_user', password='simple_user')

        response = self.client.get(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel4'),
                    args=(self.object_testmodel4.pk,))
        )
        assert response.status_code == 200
        assert b'property field value' in response.content

    def test_change_view_simple_user_unauthorized_post(self):
        self.client.login(username='simple_user', password='simple_user')
        data = {
            'var1': 'test',
            'var2': 'test',
            'var3': 1,
            'var4': self.object_testmodel0,
            'testmodel2_set-TOTAL_FORMS': 0,
            'testmodel2_set-INITIAL_FORMS': 0,
            'testmodel3_set-TOTAL_FORMS': 0,
            'testmodel3_set-INITIAL_FORMS': 0
        }
        response = self.client.post(
            reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,)),
            data
        )
        obj = TestModel1.objects.get(pk=self.object_testmodel1.pk)

        assert response.status_code == 302
        assert obj.var1 == 'Test' and obj.var1 != 'test'
        assert obj.var2 == 'Test' and obj.var2 != 'test'
        assert obj.var3 == 5 and obj.var3 != 1

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

    def test_delete_view_simple_user_unauthorized_post(self):
        self.client.login(username='simple_user', password='simple_user')
        response = self.client.post(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )

        obj = TestModel1.objects.get(pk=self.object_testmodel1.pk)

        assert response.status_code == 403
        assert obj

    def test_delete_view_super_user(self):
        self.client.login(username='super_user', password='super_user')
        response = self.client.get(
            reverse('admin:%s_%s_delete' % ('test_app', 'testmodel1'),
                    args=(self.object_testmodel1.pk,))
        )

        assert response.status_code == 200

