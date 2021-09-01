from typing import Union

from apps.common.utils import geocode, reverse_geocode
from apps.location_history.models import LocationHistory
from apps.report.models import Report


def geocode_pre_save_handler(
    sender,
    instance: Union[Report, LocationHistory],
    raw,
    update_fields,
    *args,
    **kwargs,
):
    coord_in_instance_exists = instance.latitude is not None and instance.longitude is not None
    address_in_instance_exists = instance.address is not None

    if coord_in_instance_exists and not address_in_instance_exists:
        address = reverse_geocode(instance.latitude, instance.longitude)
        if address is not None:
            instance.address = address

    if address_in_instance_exists and not coord_in_instance_exists:
        coordinates = geocode(instance.address)
        if coordinates is not None:
            instance.latitude = coordinates[0]
            instance.longitude = coordinates[1]
