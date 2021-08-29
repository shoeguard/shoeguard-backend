import pytest
from apps.user.models import User
from django.test.client import Client

ENDPOINT = '/api/v1/users/me'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.get(ENDPOINT)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_success(client: Client):
    pass
