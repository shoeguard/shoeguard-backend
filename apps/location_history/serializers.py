from rest_framework import serializers

from apps.location_history.models import LocationHistory


class LocationHistorySerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = LocationHistory
        fields = (
            'id',
            'parent_child_pair',
            'address',
            'latitude',
            'longitude',
            'created',
        )
