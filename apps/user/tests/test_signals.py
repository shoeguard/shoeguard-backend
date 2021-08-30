import pytest
from apps.user.models import ParentChildPair, User


@pytest.mark.django_db(transaction=True)
def test_creating_parent_child_pair_connects_users(create_user):
    # given
    child: User = create_user(phone_number='01012341234')
    parent: User = create_user(phone_number='01043214321')

    # when
    parent_child_pair: ParentChildPair = ParentChildPair.objects.create(
        child=child, parent=parent)

    # then
    child.refresh_from_db()
    parent.refresh_from_db()
    parent_child_pair.refresh_from_db()

    assert child.partner == parent_child_pair
    assert parent.partner == parent_child_pair
