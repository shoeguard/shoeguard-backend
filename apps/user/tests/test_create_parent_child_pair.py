import pytest

ENDPOINT = '/api/v1/users/parent-child-pair'

@pytest.mark.django_db(transaction=True)
def test_fail_when_not_authenticated():
    pass

@pytest.mark.django_db(transaction=True)
def test_fail_when_parent_child_pair_is_already_created():
    pass


@pytest.mark.django_db(transaction=True)
def test_fail_when_parent_child_pair_is_already_registered_to_child():
    pass


@pytest.mark.django_db(transaction=True)
def test_success():
    pass
