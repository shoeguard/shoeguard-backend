import pytest
from django.test.client import Client

ENDPOINT = '/api/v1/location-history'
DATA = {
    "latitude": 37.54250185,
    "longitude": 126.96721882587426,
    "reported_device": "IOT"
}


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.post(ENDPOINT)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_fail_when_requested_user_has_no_parent_child_pair():
    pass


@pytest.mark.django_db(transaction=True)
def test_success__reverse_geocoded():
    pass
