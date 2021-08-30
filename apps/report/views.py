from django.http.request import HttpRequest
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, permissions, serializers
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

    def create(self, request: HttpRequest, *args, **kwargs):
        if request.user.partner is None:
            raise serializers.ValidationError({"User": "User has no partner."})
        return super(ReportViewSet, self).create(request, *args, **kwargs)
