from django.http.request import HttpRequest
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.user.models import User
from apps.user.serializer import UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    pass
