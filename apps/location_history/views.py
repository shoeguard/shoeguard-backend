from rest_framework import mixins, permissions, viewsets

from apps.location_history.models import LocationHistory
from apps.location_history.serializers import LocationHistorySerializer


class LocationHistoryViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet,
):
    serializer_class = LocationHistorySerializer
    queryset = LocationHistory.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
