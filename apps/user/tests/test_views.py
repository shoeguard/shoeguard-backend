import pytest
from apps.user.models import User
from django.test.client import Client


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_phone_number(client: Client):
    response = client.post(
        '/api/v1/users/register',
        data={"password": "e10nMuskP@ssword"},
    )
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_password(client: Client):
    response = client.post(
        '/api/v1/users/register',
        data={"phone_number": "01012341234"},
    )
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_success(client: Client):
    response = client.post(
        '/api/v1/users/register',
        data={
            "phone_number": "01012341234",
            "password": "e10nMuskP@ssword",
            "name": "홍길동",
        },
    )
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
    User.objects.create_user(phone_number="01012341234",
                             name="홍길동",
                             password="e10nMuskP@ssword")
    response = client.post(
        '/api/v1/users/register',
        data={
            "phone_number": "01012341234",
            "password": "e10nMuskP@ssword",
            "name": "홍길동",
        },
    )
    assert response.status_code == 400
    assert User.objects.all().count() == 1
