import pytest

ENDPOINT = '/api/v1/location-history/recent'


@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated():
    pass


@pytest.mark.django_db(transaction=True)
def test_success():
    pass
