from typing import List

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.report.models import Report
from apps.report.serializers import ReportSerializer
from apps.user.models import User


class ReportViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet,
):
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('reported_device', )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Report.objects.none()

        requested_user: User = self.request.user
        if requested_user.is_parent:
            children_ids: List[int] = [
                user.id for user in requested_user.children
            ]
            return Report.objects.filter(
                reporter__in=children_ids).select_related('reporter')
        else:
            return Report.objects.filter(
                reporter=requested_user).select_related('reporter')

    def get_permissions(self):
        return (permissions.IsAuthenticated(), )

    def create(self, request: Request, *args, **kwargs):
        user: User = request.user
        if user.parent is None:
            raise serializers.ValidationError(
                {"non_field_errors": "Reporter must have parent"})

        serializer: ReportSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reporter=user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
