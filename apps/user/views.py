from typing import Dict

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import Auth, User
from apps.user.serializers import (AddChildSerializer, AuthSerializer,
                                   PasswordUpdateSerializer,
                                   UserParentChildSerializer, UserSerializer)


class UserViewSet(viewsets.GenericViewSet):
    AUTHENTICATION_REQUIRED_ACTIONS = ['me', 'update_password', 'add_child']
    PAIR_REQUIRED_ACTIONS = ['me', 'add_child']

    def get_permissions(self):
        if self.action in self.AUTHENTICATION_REQUIRED_ACTIONS:
            return (permissions.IsAuthenticated(), )
        return (permissions.AllowAny(), )

    def get_queryset(self):
        if self.action in self.PAIR_REQUIRED_ACTIONS:
            return User.objects.all().select_related(
                'parent_user').prefetch_related('parent_user__user_set')
        return User.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'me':
            return UserParentChildSerializer
        if self.action == 'update_password':
            return PasswordUpdateSerializer
        if self.action == 'add_child':
            return AddChildSerializer
        return UserSerializer

    @action(methods=['post'], detail=False)
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        User.objects.create_user(**serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses={200: UserParentChildSerializer(many=False)})
    @action(methods=['GET'], detail=False)
    def me(self, request: HttpRequest, *args, **kwargs):
        serializer: UserParentChildSerializer = self.get_serializer(
            request.user)
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

    @action(methods=['POST'], detail=False, url_path='add-child')
    def add_child(self, request: HttpRequest, *args, **kwargs):
        serializer: AddChildSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        child_id: int = serializer.validated_data['child_id']
        child_user: User = User.objects.filter(id=child_id).first()
        is_valid_child = child_user is not None and not child_user.is_parent
        if not is_valid_child:
            raise serializers.ValidationError({
                "child_id":
                "This field should be the valid id of non-parent user"
            })

        if child_user.parent_id == request.user.id:
            raise serializers.ValidationError({
                "child_id":
                "The given child_id is already paired with you as a child"
            })

        child_user.parent = request.user
        child_user.save()

        self.request.user.refresh_from_db()

        response_serializer: AddChildSerializer = self.get_serializer(
            instance=self.request.user)

        return Response(response_serializer.data)


class PhoneVerificationViewSet(mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AuthSerializer
    queryset = Auth.objects.none()
