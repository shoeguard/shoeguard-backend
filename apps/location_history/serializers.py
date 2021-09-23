from rest_framework import serializers

from apps.location_history.models import LocationHistory
from apps.user.serializers import UserSerializer


class LocationHistorySerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=255, read_only=True)
    reporter = UserSerializer

    class Meta:
        model = LocationHistory
        fields = (
            'id',
            'address',
            'latitude',
            'longitude',
            'created',
        )
