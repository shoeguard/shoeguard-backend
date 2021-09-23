from typing import Dict, Union

from rest_framework import serializers

from apps.user.models import Auth, User


class UserSerializer(serializers.ModelSerializer):
    is_child = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data: Dict[str, Union[int, str]]):
        authorized: bool = Auth.objects.filter(
            phone_number=data.get('phone_number'), is_verified=True).exists()
        if not authorized:
            raise serializers.ValidationError(
                "Phone number verification has not done")

        Auth.objects.filter(phone_number=data.get('phone_number'),
                            is_verified=True).delete()

        return data

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password', 'name', 'is_child')


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


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ('id', 'phone_number')


class AuthVerifySerializer(serializers.Serializer):
    is_verified = serializers.BooleanField(read_only=True)
    phone_number = serializers.CharField(write_only=True)
    code = serializers.IntegerField(write_only=True)


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
