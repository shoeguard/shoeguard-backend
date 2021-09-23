from typing import Dict, Union
from unittest.mock import patch

import pytest
from apps.report.models import Report
from apps.user.models import User
from django.test.client import Client

ENDPOINT = '/api/v1/reports'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.get(ENDPOINT)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_get_only_related_reports(
    client: Client,
    child_and_parent_1: Dict[str, Union[User, str]],
    child_and_parent_2: Dict[str, Union[User, str]],
    create_user_and_get_token,
):
    # given
    CAP_1_REPORT_COUNT = 30
    cap1_child: User = child_and_parent_1["child"]
    cap1_token: str = child_and_parent_1["child_token"]

    CAP_2_REPORT_COUNT = 43
    cap2_child: User = child_and_parent_2["child"]
    cap2_child_2_user: User
    cap2_child_2_user, _ = create_user_and_get_token(
        phone_number="01044443333", )
    cap2_child_2_user.parent = child_and_parent_2["parent"]
    cap2_child_2_user.save()
    cap2_token: str = child_and_parent_2["parent_token"]
    CAP_2_REPORT_COUNT_2 = 21

    class DuckTypingLocation:
        latitude: float
        longitude: float

        def __init__(self, latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

    location = DuckTypingLocation(37.54250185, 126.96721882587426)

    with patch("apps.common.utils.Nominatim.geocode", return_value=location):
        for _ in range(CAP_1_REPORT_COUNT):
            Report.objects.create(
                reporter_id=cap1_child.id,
                address="서울시 용산구 원효로97길 33-4",
                reported_device="IOT",
            )
        for _ in range(CAP_2_REPORT_COUNT):
            Report.objects.create(
                reporter_id=cap2_child.id,
                address="서울시 용산구 원효로97길 33-4",
                reported_device="IOT",
            )
        for _ in range(CAP_2_REPORT_COUNT_2):
            Report.objects.create(
                reporter_id=cap2_child_2_user.id,
                address="서울시 용산구 원효로97길 33-4",
                reported_device="IOT",
            )

    # when
    cap1_response = client.get(
        ENDPOINT,
        HTTP_AUTHORIZATION=f"Bearer {cap1_token}",
    )
    cap2_response = client.get(
        ENDPOINT,
        HTTP_AUTHORIZATION=f"Bearer {cap2_token}",
    )

    # then
    assert cap1_response.status_code == 200
    assert len(cap1_response.json()) == CAP_1_REPORT_COUNT
    assert cap2_response.status_code == 200
    assert len(
        cap2_response.json()) == CAP_2_REPORT_COUNT + CAP_2_REPORT_COUNT_2


@pytest.fixture
def child_and_parent_1(create_user_and_get_token):
    child: User
    parent: User
    child_token: str
    parent_token: str

    child, child_token = create_user_and_get_token(phone_number='01012345678')
    parent, parent_token = create_user_and_get_token(
        phone_number='01087654321')

    child.parent = parent
    child.save()

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

    child, child_token = create_user_and_get_token(phone_number='01043214321')
    parent, parent_token = create_user_and_get_token(
        phone_number='01012341234')

    child.parent = parent
    child.save()

    return {
        "child": child,
        "parent": parent,
        "child_token": child_token,
        "parent_token": parent_token
    }
