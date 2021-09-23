from rest_framework import serializers

from apps.report.models import Report
from apps.user.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer

    class Meta:
        model = Report
        fields = (
            'id',
            'address',
            'latitude',
            'longitude',
            'audio_url',
            'reported_device',
        )
