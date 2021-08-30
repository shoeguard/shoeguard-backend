from rest_framework import mixins, permissions
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
