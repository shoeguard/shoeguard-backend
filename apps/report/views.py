from rest_framework import mixins, permissions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.common.decorators import check_partner_available_class_view
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

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Report.objects.none()

        partner_id: int = self.request.user.partner_id
        return Report.objects.filter(parent_child_pair_id=partner_id
                                     ).select_related('parent_child_pair')

    def get_permissions(self):
        return (permissions.IsAuthenticated(), )

    @check_partner_available_class_view
    def create(self, request: Request, *args, **kwargs):
        user: User = request.user

        payload = dict(request.data)
        payload['parent_child_pair'] = user.partner_id
        serializer: ReportSerializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
