from rest_framework import serializers

from apps.report.models import Report
from apps.user.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer
    audio_url = serializers.CharField(read_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'address',
            'latitude',
            'longitude',
            'audio_url',
            'reported_device',
            'created',
        )


class ReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id',
            'audio_url',
        )
