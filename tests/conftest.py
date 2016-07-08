from __future__ import unicode_literals

import pytest

from django.core.urlresolvers import reverse


@pytest.fixture
def django_request(request, rf):

    def _django_request(cls, user):
        fixture_request = rf.get(
            reverse('admin:index')
        )
        fixture_request.user = user

        return fixture_request

    request.cls.django_request = _django_request


