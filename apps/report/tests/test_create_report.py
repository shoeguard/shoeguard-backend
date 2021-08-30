import json

import pytest
from apps.report.models import Report
from apps.user.models import ParentChildPair, User
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
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert 'User' in result
    assert Report.objects.all().count() == 0


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_address(client: Client, child_and_parent):
    # given
    token: str = child_and_parent["child_token"]
    data = DATA.copy()
    del data["address"]
    # when
    response = client.post(
        ENDPOINT,
        json.dumps(data),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert ['address'] == list(result.keys())
    assert Report.objects.all().count() == 0


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_reported_device(client: Client, child_and_parent):
    # given
    token: str = child_and_parent["child_token"]
    data = DATA.copy()
    del data["reported_device"]
    # when
    response = client.post(
        ENDPOINT,
        json.dumps(data),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert ["reported_device"] == list(result.keys())
    assert Report.objects.all().count() == 0


@pytest.mark.django_db(transaction=True)
def test_fail_when_wrong_reported_device_type(client: Client,
                                              child_and_parent):
    # given
    token: str = child_and_parent["child_token"]
    data = DATA.copy()
    data["reported_device"] = "nothing"
    # when
    response = client.post(
        ENDPOINT,
        json.dumps(data),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert ["reported_device"] == list(result.keys())
    assert Report.objects.all().count() == 0


@pytest.mark.django_db(transaction=True)
def test_success__geocoded(client: Client):
    pass


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
