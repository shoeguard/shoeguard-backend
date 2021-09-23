from typing import List

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.location_history.models import LocationHistory
from apps.location_history.serializers import LocationHistorySerializer
from apps.user.models import User


class LocationHistoryViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    serializer_class = LocationHistorySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return LocationHistory.objects.none()

        requested_user: User = self.request.user
        if requested_user.is_parent:
            children_ids: List[int] = [
                user.id for user in requested_user.children
            ]
            return LocationHistory.objects.filter(
                reporter__in=children_ids).select_related('reporter')
        else:
            return LocationHistory.objects.filter(
                reporter=requested_user).select_related('reporter')

    def create(self, request: Request, *args, **kwargs):
        user: User = request.user
        if user.parent is None:
            raise serializers.ValidationError(
                {"non_field_errors": "Reporter must have parent"})

        serializer: LocationHistorySerializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reporter=user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
