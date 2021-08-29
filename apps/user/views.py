from django.http.request import HttpRequest
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.user.models import User
from apps.user.serializer import UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
