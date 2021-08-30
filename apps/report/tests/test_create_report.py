import pytest
from django.test.client import Client

ENDPOINT = "/api/v1/reports"
DATA = {"address": "서울시 용산구 원효로97길 33-4", "reported_device": "IOT"}


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.post(ENDPOINT, data=DATA)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_fail_when_requested_user_has_no_parent_child_pair(client: Client):
    pass


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_address(client: Client):
    pass


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_reported_device(client: Client):
    pass


@pytest.mark.django_db(transaction=True)
def test_fail_when_wrong_reported_device_type(client: Client):
    pass


@pytest.mark.django_db(transaction=True)
def test_success__geocoded(client: Client):
    pass
