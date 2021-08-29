import pytest
from apps.user.models import User
from django.test.client import Client

ENDPOINT = '/api/v1/users/update-password'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.post(
        ENDPOINT,
        data={
            "old_password": "e10nMuskP@ssword",
            "new_password": "j3ffB3z0sP@ssword",
        },
    )

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_fail_when_old_password_not_given(client: Client, user, get_token):
    # given
    token = get_token("01012341234", "e10nMuskP@ssword")

    # when
    response = client.post(
        ENDPOINT,
        data={
            "new_password": "j3ffB3z0sP@ssword",
        },
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    assert response.status_code == 400
    assert 'old_password' in response.json()


@pytest.mark.django_db(transaction=True)
def test_fail_when_new_password_not_given(client: Client, user, get_token):
    # given
    token = get_token("01012341234", "e10nMuskP@ssword")

    # when
    response = client.post(
        ENDPOINT,
        data={
            "old_password": "e10nMuskP@ssword",
        },
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    assert response.status_code == 400
    assert 'new_password' in response.json()


@pytest.mark.django_db(transaction=True)
def test_fail_when_old_password_is_wrong(client: Client, user, get_token):
    # given
    token = get_token("01012341234", "e10nMuskP@ssword")

    # when
    response = client.post(
        ENDPOINT,
        data={
            "old_password": "1234",
            "new_password": "j3ffB3z0sP@ssword",
        },
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    assert response.status_code == 400
    assert 'old_password' in response.json()


@pytest.mark.django_db(transaction=True)
def test_success(client: Client, user: User, get_token):
    # given
    token = get_token("01012341234", "e10nMuskP@ssword")

    # when
    response = client.post(
        ENDPOINT,
        data={
            "old_password": "e10nMuskP@ssword",
            "new_password": "j3ffB3z0sP@ssword",
        },
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    # then
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("j3ffB3z0sP@ssword")


@pytest.fixture
def user(create_user):
    return create_user(
        phone_number="01012341234",
        password="e10nMuskP@ssword",
        name="홍길동",
    )
