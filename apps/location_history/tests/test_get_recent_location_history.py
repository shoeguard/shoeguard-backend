import json
from unittest.mock import patch

import pytest
from apps.location_history.models import LocationHistory
from apps.user.models import ParentChildPair, User
from django.test.client import Client

ENDPOINT = '/api/v1/location-history/recent'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.post(ENDPOINT)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_success(client: Client, child_and_parent, child_and_parent_2):
    # given
    child: User = child_and_parent["child"]
    child2: User = child_and_parent_2["child"]
    child_token: str = child_and_parent["child_token"]

    class DuckTypingLocation:
        latitude: float
        longitude: float
        address: str

        def __init__(self, latitude, longitude, address):
            self.latitude = latitude
            self.longitude = longitude
            self.address = address

    location = DuckTypingLocation(
        37.54250185,
        126.96721882587426,
        "선린인터넷고등학교, 33-4, 원효로97길, 청파동, 용산구, 서울, 04314, 대한민국",
    )

    with patch("apps.common.utils.Nominatim.reverse", return_value=location):
        LocationHistory.objects.create(
            parent_child_pair=child.partner,
            latitude=456,
            longitude=123,
        )
        LocationHistory.objects.create(
            parent_child_pair=child.partner,
            latitude=123,
            longitude=456,
        )
        LocationHistory.objects.create(
            parent_child_pair=child.partner,
            latitude=313,
            longitude=909,
        )
        LocationHistory.objects.create(
            parent_child_pair=child2.partner,
            latitude=333,
            longitude=222,
        )

    # when
    response = client.get(ENDPOINT, HTTP_AUTHORIZATION=f"Bearer {child_token}")

    # then
    assert response.status_code == 200
    result = response.json()
    assert result["latitude"] == 313
    assert result["longitude"] == 909


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_location_history(client: Client, child_and_parent):
    # given
    child_token: str = child_and_parent["child_token"]

    # when
    response = client.get(ENDPOINT, HTTP_AUTHORIZATION=f"Bearer {child_token}")

    # then
    assert response.status_code == 204


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


@pytest.fixture
def child_and_parent_2(create_user_and_get_token):
    child: User
    parent: User
    child_token: str
    parent_token: str

    child, child_token = create_user_and_get_token(phone_number='01012345671')
    parent, parent_token = create_user_and_get_token(
        phone_number='01087654322')

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
