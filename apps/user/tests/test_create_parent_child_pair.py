import json

import pytest
from apps.user.models import ParentChildPair, User
from django.test.client import Client

ENDPOINT = '/api/v1/users/parent-child-pair'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.post(ENDPOINT)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_fail_when_parent_child_pair_is_already_created(
    client: Client,
    child_and_parent,
):
    # given
    token: str = child_and_parent["child_token"]
    data = {
        'child_id': child_and_parent["child"].pk,
        'parent_id': child_and_parent["parent"].pk,
    }
    # when
    response = client.post(
        ENDPOINT,
        json.dumps(data),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    assert response.status_code == 400
    assert response.json() == {
        'non_field_errors': ["ParentChildPair already exists."]
    }


@pytest.mark.django_db(transaction=True)
def test_fail_when_parent_child_pair_is_already_registered_to_child():
    pass


@pytest.mark.django_db(transaction=True)
def test_success():
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
