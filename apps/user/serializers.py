from django.db.models import Q
from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    is_child = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'is_child')


class AddChildSerializer(serializers.ModelSerializer):
    child_id = serializers.IntegerField(write_only=True, required=True)
    children = UserSerializer(read_only=True, many=True)

    def validate_child_id(self, child_id: int) -> int:
        user: User = self.context['request'].user
        if user.id == child_id:
            raise serializers.ValidationError(
                'You cannot add yourself as a child')
        return child_id

    class Meta:
        model = User
        fields = (
            'child_id',
            'children',
        )


class UserParentChildSerializer(serializers.ModelSerializer):
    is_child = serializers.BooleanField(read_only=True)
    parent = UserSerializer(read_only=True)
    children = UserSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'phone_number',
            'name',
            'is_child',
            'parent',
            'children',
        )


class UserPartnerSerializer(serializers.ModelSerializer):
    partner = ParentChildPairSerializer()
    is_child = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'is_child', 'partner')


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
