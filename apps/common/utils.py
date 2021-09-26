from apps.user.models import User
from geopy.geocoders import Nominatim
from rest_framework.serializers import ValidationError

geolocator = Nominatim(user_agent="shoeguard")
from typing import Union


def geocode(address: str) -> Union[tuple[float, float], None]:
    location = geolocator.geocode(address)
    if location is None:
        return None
    return (location.latitude, location.longitude)


def reverse_geocode(latitude: float, longitude: float) -> Union[str, None]:
    location = geolocator.reverse((latitude, longitude))
    if location is None:
        return None
    return location.address
