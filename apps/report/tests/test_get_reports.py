import pytest
from django.test.client import Client

ENDPOINT = '/api/v1/reports'


@pytest.mark.django_db(transation=True)
def test_fail_when_not_authenticated(client: Client):
    pass


@pytest.mark.django_db(transation=True)
def test_get_only_related_reports(client: Client):
    pass
