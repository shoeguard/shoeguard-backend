import pytest
from django.test.client import Client

from apps.user.models import User


@pytest.fixture
def create_user():
    def _create_user(phone_number: str, password: str, name: str):
        return User.objects.create_user(
            phone_number=phone_number,
            password=password,
            name=name,
        )

    return _create_user


@pytest.fixture
def get_token(client: Client):
    def _get_token(phone_number: str, password: str) -> str:
        result = client.post(
            '/api/v1/token',
            data={
                "phone_number": phone_number,
                "password": password
            },
        )
        response = result.json()
        return response['access']

    return _get_token
