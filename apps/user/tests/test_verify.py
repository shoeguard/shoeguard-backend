import pytest
from apps.user.models import Auth
from django.test.client import Client

ENDPOINT = '/api/v1/phone-verification/verify'


@pytest.mark.django_db(transaction=True)
def test_success(client: Client):
    # given
    PHONE_NUMBER = "01012341234"
    ## create dummy and real data
    Auth.objects.create(phone_number=PHONE_NUMBER)
    Auth.objects.create(phone_number=PHONE_NUMBER)
    auth: Auth = Auth.objects.create(phone_number=PHONE_NUMBER)

    # when
    response = client.post(
        ENDPOINT,
        content_type='application/json',
        data={
            "phone_number": PHONE_NUMBER,
            "code": auth.code
        },
    )

    # then
    result = response.json()
    print(result)
    assert response.status_code == 200
    auth.refresh_from_db()

    assert auth.is_verified
