import json

import pytest
from apps.location_history.models import LocationHistory
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
def test_fail_when_requested_user_has_no_parent_child_pair(
    client: Client,
    create_user_and_get_token,
):
    # given
    token: str
    _, token = create_user_and_get_token(phone_number='01012341234')

    # when
    response = client.post(
        ENDPOINT,
        json.dumps(DATA),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert 'User' in result
    assert LocationHistory.objects.all().count() == 0


@pytest.mark.django_db(transaction=True)
def test_success__reverse_geocoded():
    pass
