from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.common.utils import geocode, reverse_geocode
from apps.location_history.models import LocationHistory


@receiver(pre_save, sender=LocationHistory)
def location_history_pre_save_handler(
    sender,
    instance: LocationHistory,
    raw,
    update_fields,
    *args,
    **kwargs,
):
    address = reverse_geocode(instance.latitude, instance.longitude)
    if address is not None:
        instance.address = address
