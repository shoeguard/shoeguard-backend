import pytest
from django.test.client import Client

ENDPOINT = '/api/v1/users/update_password'


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
