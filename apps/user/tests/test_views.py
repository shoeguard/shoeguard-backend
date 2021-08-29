import pytest
from django.test.client import Client


@pytest.mark.django_db(transaction=True)
def test_fail_when_no_phone_number(client: Client):
    response = client.post(
        '/api/v1/users/register',
        data={"password": "e10nMuskP@ssword"},
    )
    assert response.status_code == 400


def test_fail_when_no_phone_number(client: Client):
    pass


def test_success(client):
    pass


def test_fail_when_phone_number_duplicates():
    pass
