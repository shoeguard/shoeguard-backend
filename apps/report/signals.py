from django.db.models.signals import pre_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim

from apps.report.models import Report


@receiver(pre_save, sender=Report)
def report_pre_save_handler(
    sender,
    instance: Report,
    raw,
    update_fields,
    *args,
    **kwargs,
):

    geolocator = Nominatim(user_agent="shoeguard")
    if instance.latitude is not None and instance.longitude is not None:
        location = geolocator.reverse(instance.latitude, instance.longitude)
        instance.address = location.address

    if instance.address is not None:
        location = geolocator.geocode(instance.address)
        if location is not None:
            instance.latitude = location.latitude
            instance.longitude = location.longitude
