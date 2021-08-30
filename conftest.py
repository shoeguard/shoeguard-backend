import pytest
from django.test.client import Client

from apps.user.models import User


@pytest.fixture
def create_user():
    def _create_user(
        phone_number: str = '01012341234',
        password: str = '310nMuskP@ssw0rd',
        name: str = '홍길동',
    ):
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


@pytest.fixture
def create_user_and_get_token(create_user, get_token):
    def _create_user_and_get_token(
        phone_number: str = '01012341234',
        password: str = '310nMuskP@ssw0rd',
        name: str = '홍길동',
    ) -> tuple[User, str]:
        user: User = create_user(
            phone_number=phone_number,
            password=password,
            name=name,
        )
        token: str = get_token(phone_number=phone_number, password=password)
        return user, token

    return _create_user_and_get_token
