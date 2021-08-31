from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.location_history.models import LocationHistory
from apps.location_history.serializers import LocationHistorySerializer


class LocationHistoryViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet,
):
    serializer_class = LocationHistorySerializer
    queryset = LocationHistory.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request: Request, *args, **kwargs):
        if request.user.partner is None:
            raise serializers.ValidationError({"User": "User has no partner."})

        payload = dict(request.data)
        payload['parent_child_pair'] = request.user.partner_id

        serializer: LocationHistorySerializer = self.get_serializer(
            data=payload)
        serializer.is_valid(raise_exception=True)
