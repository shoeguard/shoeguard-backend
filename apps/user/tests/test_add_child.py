import pytest
from apps.user.models import User
from django.test.client import Client

ENDPOINT = '/api/v1/users/add-child'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated(client: Client):
    # when
    response = client.post(ENDPOINT)

    # then
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_fail_when_self_to_child(client: Client, create_user, get_token: str):
    # given
    PHONE_NUMBER = "01012341234"
    PASSWORD = "e10nMuskP@ssword"
    user: User = create_user(phone_number=PHONE_NUMBER,
                             password=PASSWORD,
                             name="홍길동")
    token = get_token(PHONE_NUMBER, PASSWORD)

    # when
    response = client.post(
        ENDPOINT,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        content_type='application/json',
        data={"child_id": user.id},
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert "child_id" in result


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_existing_user(client: Client, create_user,
                                     get_token: str):
    # given
    PHONE_NUMBER = "01012341234"
    PASSWORD = "e10nMuskP@ssword"
    create_user(phone_number=PHONE_NUMBER, password=PASSWORD, name="홍길동")
    token = get_token(PHONE_NUMBER, PASSWORD)

    # when
    response = client.post(
        ENDPOINT,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        content_type='application/json',
        data={"child_id": -1},
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert "child_id" in result


@pytest.mark.django_db(transaction=True)
def test_success(client: Client, create_user, get_token):
    # given
    PHONE_NUMBER = "01012341234"
    PASSWORD = "e10nMuskP@ssword"
    child: User = create_user(phone_number="01012341235",
                              password=PASSWORD,
                              name="임꺽정")
    parent: User = create_user(phone_number=PHONE_NUMBER,
                               password=PASSWORD,
                               name="홍길동")
    token = get_token(PHONE_NUMBER, PASSWORD)

    # when
    response = client.post(
        ENDPOINT,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        content_type='application/json',
        data={"child_id": child.id},
    )

    # then
    result = response.json()
    assert response.status_code == 200
    assert "children" in result

    child.refresh_from_db()
    assert child.parent.id == parent.id


@pytest.mark.django_db(transaction=True)
def test_fail_when_pair_parent_as_child(
    client: Client,
    create_user,
    get_token: str,
):
    # given
    PHONE_NUMBER = "01012341234"
    PASSWORD = "e10nMuskP@ssword"
    child_1: User = create_user(phone_number="01012341235",
                                password=PASSWORD,
                                name="임꺽정")
    parent_1: User = create_user(phone_number=PHONE_NUMBER,
                                 password=PASSWORD,
                                 name="홍길동")
    parent_2: User = create_user(phone_number="01011114321",
                                 password=PASSWORD,
                                 name="길동홍")
    child_1.parent = parent_1
    child_1.save()

    token: str = get_token(parent_2.phone_number, PASSWORD)

    # when
    response = client.post(
        ENDPOINT,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        content_type='application/json',
        data={"child_id": parent_1.id},
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert "child_id" in result

    assert not User.objects.filter(parent_id=parent_2.id).exists()


@pytest.mark.django_db(transaction=True)
def test_fail_when_already_paired(
    client: Client,
    create_user,
    get_token: str,
):
    # given
    PHONE_NUMBER = "01012341234"
    PASSWORD = "e10nMuskP@ssword"
    child: User = create_user(phone_number="01012341235",
                              password=PASSWORD,
                              name="임꺽정")
    parent: User = create_user(phone_number=PHONE_NUMBER,
                               password=PASSWORD,
                               name="홍길동")
    child.parent = parent
    child.save()
    token = get_token(parent.phone_number, PASSWORD)

    # when
    response = client.post(
        ENDPOINT,
        HTTP_AUTHORIZATION=f'Bearer {token}',
        content_type='application/json',
        data={"child_id": child.id},
    )

    # then
    result = response.json()
    assert response.status_code == 400
    assert "child_id" in result

    child.refresh_from_db()
    assert child.parent.id == parent.id
