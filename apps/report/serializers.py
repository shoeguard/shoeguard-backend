from rest_framework import serializers

from apps.report.models import Report
from apps.user.serializers import ParentChildSerializer


class ReportSerializer(serializers.ModelSerializer):
    parent_child_pair = ParentChildSerializer
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'parent_child_pair',
            'address',
            'latitude',
            'longitude',
            'reported_device',
            'created',
        )
