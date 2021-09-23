from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.decorators import check_partner_available_class_view
from apps.location_history.models import LocationHistory
from apps.location_history.serializers import (LocationHistorySerializer,
                                               NewLocationHistorySerializer)
from apps.user.models import User


class LocationHistoryViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet,
):
    def get_serializer_class(self):
        if self.action == 'create':
            return NewLocationHistorySerializer
        return LocationHistorySerializer

    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return LocationHistory.objects.none()

        partner_id: int = self.request.user.partner_id
        return LocationHistory.objects.filter(
            parent_child_pair_id=partner_id).order_by('-created')

    def create(self, request: Request, *args, **kwargs):
        user: User = request.user
        if user.parent is None:
            raise serializers.ValidationError(
                {"non_field_errors": "Reporter must have parent"})

        serializer: NewLocationHistorySerializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reporter=user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @extend_schema(
        responses={
            200: LocationHistorySerializer(many=False),
            204: None,
        }, )
    @action(methods=['GET'], detail=False, url_path='recent')
    def get_recent(self, request: Request):
        location_history: LocationHistory = self.get_queryset().first()
        if location_history is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer: LocationHistorySerializer = self.get_serializer(
            location_history, )
        return Response(serializer.data)
