from unittest.mock import patch

import pytest
from apps.report.models import Report
from apps.user.models import ParentChildPair, User
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
    child_and_parent_1,
    child_and_parent_2,
):
    # given
    CAP_1_REPORT_COUNT = 30
    CAP_1_PARENT_CHILD_PAIR: ParentChildPair = child_and_parent_1[
        "child"].partner
    cap1_token: str = child_and_parent_1["child_token"]

    CAP_2_REPORT_COUNT = 43
    CAP_2_PARENT_CHILD_PAIR: ParentChildPair = child_and_parent_2[
        "child"].partner
    cap2_token: str = child_and_parent_2["child_token"]

    class DuckTypingLocation:
        latitude: float
        longitude: float

        def __init__(self, latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

    location = DuckTypingLocation(37.54250185, 126.96721882587426)

    with patch("apps.report.signals.Nominatim.geocode", return_value=location):
        for _ in range(CAP_1_REPORT_COUNT):
            Report.objects.create(
                parent_child_pair=CAP_1_PARENT_CHILD_PAIR,
                address="서울시 용산구 원효로97길 33-4",
                reported_device="IOT",
            )
        for _ in range(CAP_2_REPORT_COUNT):
            Report.objects.create(
                parent_child_pair=CAP_2_PARENT_CHILD_PAIR,
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
    assert len(cap2_response.json()) == CAP_2_REPORT_COUNT


@pytest.fixture
def child_and_parent_1(create_user_and_get_token):
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

    child, child_token = create_user_and_get_token(phone_number='01043214321')
    parent, parent_token = create_user_and_get_token(
        phone_number='01012341234')

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
