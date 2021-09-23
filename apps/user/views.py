from typing import Dict

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.models import ParentChildPair, User
from apps.user.serializers import (ParentChildPairSerializer,
                                   PasswordUpdateSerializer,
                                   UserParentChildSerializer, UserSerializer)


class UserViewSet(viewsets.GenericViewSet):
    AUTHENTICATION_REQUIRED_ACTIONS = ['me', 'update_password', 'add_child']

    def get_permissions(self):
        if self.action in self.AUTHENTICATION_REQUIRED_ACTIONS:
            return (permissions.IsAuthenticated(), )
        return (permissions.AllowAny(), )

    def get_queryset(self):
        if self.action == 'me':
            return User.objects.all().select_related('parent_user')
        return User.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'me':
            return UserParentChildSerializer
        if self.action == 'update_password':
            return PasswordUpdateSerializer
        return UserSerializer

    @action(methods=['post'], detail=False)
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses={200: UserParentChildSerializer(many=False)})
    @action(methods=['GET'], detail=False)
    def me(self, request: HttpRequest, *args, **kwargs):
        serializer: UserParentChildSerializer = UserParentChildSerializer(
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


class ParentChildPairViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ParentChildPairSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return ParentChildPair.objects.none()

        partner_id: int = self.request.user.partner_id
        return ParentChildPair.objects.filter(
            parent_child_pair_id=partner_id).order_by('-created')

    def create(self, request, *args, **kwargs):
        # validation
        user: User = request.user
        data: Dict[str, any] = request.data
        if user.partner is not None:
            raise serializers.ValidationError(
                {"non_field_errors": ["ParentChildPair already exists."]})

        child_id = data.get('child_id')
        parent_id = data.get('parent_id')
        if user.pk not in (child_id, parent_id):
            raise serializers.ValidationError({
                "non_field_errors": [
                    "One of child_id or parent_id should include requested user's pk."
                ]
            })

        return super(ParentChildPairViewSet,
                     self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValueError as e:
            raise serializers.ValidationError({"non_field_errors": [str(e)]})
