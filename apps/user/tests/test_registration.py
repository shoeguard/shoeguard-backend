import pytest
from apps.user.models import Auth, User
from django.test.client import Client


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_phone_number(client: Client):
    # when
    response = client.post(
        '/api/v1/users/register',
        data={"password": "e10nMuskP@ssword"},
    )

    # then
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_password(client: Client):
    # when
    response = client.post(
        '/api/v1/users/register',
        data={"phone_number": "01012341234"},
    )

    # then
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authorized(client: Client):
    # when
    response = client.post(
        '/api/v1/users/register',
        data={
            "phone_number": "01012341234",
            "password": "e10nMuskP@ssword",
            "name": "홍길동",
        },
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert User.objects.all().count() == 0


@pytest.mark.django_db(transaction=True)
def test_success(client: Client):
    # given
    Auth.objects.create(phone_number='01012341234', is_verified=True)

    # when
    response = client.post(
        '/api/v1/users/register',
        data={
            "phone_number": "01012341234",
            "password": "e10nMuskP@ssword",
            "name": "홍길동",
        },
    )

    # then
    result = response.json()
    assert response.status_code == 201
    assert 'password' not in result
    assert result["phone_number"] == "01012341234"
    assert result["name"] == "홍길동"
    assert User.objects.all().count() == 1
    user: User = User.objects.all().first()
    assert user.phone_number == "01012341234"
    assert user.name == "홍길동"


@pytest.mark.django_db(transaction=True)
def test_fail_when_phone_number_duplicates(client: Client):
    # given
    User.objects.create_user(phone_number="01012341234",
                             name="홍길동",
                             password="e10nMuskP@ssword")

    # when
    response = client.post(
        '/api/v1/users/register',
        data={
            "phone_number": "01012341234",
            "password": "e10nMuskP@ssword",
            "name": "홍길동",
        },
    )

    # then
    assert response.status_code == 400
    assert User.objects.all().count() == 1
