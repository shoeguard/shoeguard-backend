import json

import pytest
from apps.location_history.models import LocationHistory
from apps.user.models import ParentChildPair, User
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
def test_success__reverse_geocoded(client: Client, child_and_parent):
    # given
    token: str = child_and_parent["child_token"]

    # when
    response = client.post(
        ENDPOINT,
        json.dumps(DATA),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    result = response.json()
    assert response.status_code == 201
    assert result[
        "address"] == "선린인터넷고등학교, 33-4, 원효로97길, 청파동, 용산구, 서울, 04314, 대한민국"
    assert result['latitude'] == 37.54250185
    assert result['longitude'] == 126.96721882587426

    assert LocationHistory.objects.all().count() == 1
    location_history: LocationHistory = LocationHistory.objects.all().first()
    assert location_history.address == "선린인터넷고등학교, 33-4, 원효로97길, 청파동, 용산구, 서울, 04314, 대한민국"
    assert location_history.latitude == 37.54250185
    assert location_history.longitude == 126.96721882587426


@pytest.fixture
def child_and_parent(create_user_and_get_token):
    child: User
    parent: User
    child_token: str
    parent_token: str

    child, child_token = create_user_and_get_token(phone_number='01012345678')
    parent, parent_token = create_user_and_get_token(
        phone_number='01087654321')

    ParentChildPair.objects.create(
        child=child,
        parent=parent,
    )

    return {
        "child": child,
        "parent": parent,
        "child_token": child_token,
        "parent_token": parent_token
    }
