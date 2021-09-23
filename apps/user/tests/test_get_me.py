import pytest
from django.test.client import Client

ENDPOINT = '/api/v1/users/me'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.get(ENDPOINT)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_success(client: Client, create_user, get_token):
    # given
    PHONE_NUMBER = "01012341234"
    PASSWORD = "e10nMuskP@ssword"
    create_user(phone_number=PHONE_NUMBER, password=PASSWORD, name="홍길동")
    token = get_token(PHONE_NUMBER, PASSWORD)

    # when
    response = client.get(ENDPOINT, HTTP_AUTHORIZATION=f'Bearer {token}')

    # then
    result = response.json()
    assert response.status_code == 200
    assert result['phone_number'] == PHONE_NUMBER
    assert result['name'] == '홍길동'
