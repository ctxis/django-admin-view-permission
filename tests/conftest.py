from __future__ import unicode_literals

import pytest

from django.core.urlresolvers import reverse


"""
-- deprecated
@pytest.fixture
def fixture_add_request(request, rf):

    def _get_request(cls, user):
        request = rf.get(
            reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
        )
        request.user = user
        return request

    request.cls.fixture_add_request = _get_request
"""

@pytest.fixture
def simple_add_request(request, rf):
    fixture_request = rf.get(
        reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
    )
    fixture_request.user = request.cls.simple_user
    request.cls.simple_add_request = fixture_request


@pytest.fixture
def simple_change_request(request, rf):
    fixture_request = rf.get(
        reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                args=(request.cls.object_testmodel1.pk, ))
    )
    fixture_request.user = request.cls.simple_user
    request.cls.simple_change_request = fixture_request


@pytest.fixture
def super_add_request(request, rf):
    fixture_request = rf.get(
        reverse('admin:%s_%s_add' % ('test_app', 'testmodel1'))
    )
    fixture_request.user = request.cls.super_user
    request.cls.super_add_request = fixture_request


@pytest.fixture
def super_change_request(request, rf):
    fixture_request = rf.get(
        reverse('admin:%s_%s_change' % ('test_app', 'testmodel1'),
                args=(request.cls.object_testmodel1.pk, ))
    )
    fixture_request.user = request.cls.super_user
    request.cls.super_change_request = fixture_request


@pytest.fixture
def simple_changelist_request(request, rf):
    fixture_request = rf.get(
        reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1'))
    )
    fixture_request.user = request.cls.simple_user
    request.cls.simple_changelist_request = fixture_request


@pytest.fixture
def super_changelist_request(request, rf):
    fixture_request = rf.get(
        reverse('admin:%s_%s_changelist' % ('test_app', 'testmodel1'))
    )
    fixture_request.user = request.cls.super_user
    request.cls.super_changelist_request = fixture_request