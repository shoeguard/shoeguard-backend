from typing import Dict, Union

from rest_framework import serializers

from apps.user.models import Auth, User


class UserSerializer(serializers.ModelSerializer):
    def phone_number_validator(phone_number: str):
        if not phone_number.isnumeric():
            raise serializers.ValidationError("Phone number must be numeric")
        if not phone_number.startswith('010'):
            raise serializers.ValidationError(
                "Phone number must start with 010")
        if not len(phone_number) == 11:
            raise serializers.ValidationError(
                "The length of Phone Number must be 11, like in format of: 01012345678"
            )

    is_child = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(validators=[phone_number_validator])

    def validate(self, data: Dict[str, Union[int, str]]):
        authorized: bool = Auth.objects.filter(
            phone_number=data.get('phone_number'), is_verified=True).exists()
        if not authorized:
            raise serializers.ValidationError(
                "Phone number verification has not done")

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
