from rest_framework import serializers

from apps.report.models import Report
from apps.user.serializers import ParentChildPairSerializer, UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    parent_child_pair = ParentChildPairSerializer

    class Meta:
        model = Report
        fields = (
            'id',
            'parent_child_pair',
            'address',
            'latitude',
            'longitude',
            'reported_device',
            'audio_url',
            'created',
        )


class NewReportSerializer(serializers.ModelSerializer):
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
