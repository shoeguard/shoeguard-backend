from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, permissions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.report.models import Report
from apps.report.serializers import ReportSerializer


class ReportViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet,
):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return (permissions.IsAuthenticated(), )
        return super(ReportViewSet, self).get_permissions()

    def create(self, request: Request, *args, **kwargs):
        if request.user.partner is None:
            raise serializers.ValidationError({"User": "User has no partner."})

        payload = dict(request.data)
        payload['parent_child_pair'] = request.user.partner_id

        serializer: ReportSerializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
