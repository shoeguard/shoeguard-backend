from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.user.models import ParentChildPair, User


@receiver(post_save, sender=ParentChildPair)
def parent_child_pair_post_save_handler(sender, instance: ParentChildPair,
                                        created: bool, *args, **kwargs):
    child: User = instance.child
    parent: User = instance.parent

    child.partner = instance
    parent.partner = instance

    child.save()
    parent.save()
