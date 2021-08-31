from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import ParentChildPair, User
from apps.user.serializers import (ParentChildPairSerializer,
                                   PasswordUpdateSerializer,
                                   UserPartnerSerializer, UserSerializer)


class UserViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'me':
            return UserPartnerSerializer
        return UserSerializer

    def get_queryset(self):
        if self.action == 'me':
            return User.objects.all().select_related('partner').select_related(
                'child', 'parent')
        return User.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'update_password':
            return PasswordUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        AUTHENTICATION_REQUIRED_ACTIONS = ['me', 'update_password']
        if self.action in AUTHENTICATION_REQUIRED_ACTIONS:
            return (permissions.IsAuthenticated(), )
        return (permissions.AllowAny(), )

    @action(methods=['post'], detail=False)
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: UserPartnerSerializer(many=False)})
    @action(methods=['GET'], detail=False)
    def me(self, request: HttpRequest, *args, **kwargs):
        serializer: UserPartnerSerializer = UserPartnerSerializer(request.user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, url_path='update-password')
    def update_password(self, request: HttpRequest, *args, **kwargs):
        serializer: PasswordUpdateSerializer = self.get_serializer(
            data=request.data, )
        serializer.is_valid(raise_exception=True)

        old_password: str = request.data['old_password']
        new_password: str = request.data['new_password']

        is_correct: bool = request.user.check_password(old_password)
        if not is_correct:
            raise serializers.ValidationError(
                {"old_password": "old_password is not correct"})

        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError(e.message)

        request.user.set_password(new_password)
        request.user.save()
        return Response()


class ParentChildPairViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ParentChildPairSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ParentChildPair.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.partner is not None:
            raise serializers.ValidationError(
                {"non_field_errors": ["ParentChildPair already exists."]})
        super(ParentChildPairViewSet, self).create(request, *args, **kwargs)
