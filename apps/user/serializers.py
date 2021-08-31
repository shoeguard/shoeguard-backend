from rest_framework import serializers

from apps.user.models import ParentChildPair, User


class UserSerializer(serializers.ModelSerializer):
    is_child = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'is_child')


class ParentChildPairSerializer(serializers.ModelSerializer):
    child = UserSerializer()
    parent = UserSerializer()

    class Meta:
        model = ParentChildPair
        fields = ('id', 'child', 'parent')


class UserPartnerSerializer(serializers.ModelSerializer):
    partner = ParentChildPairSerializer()
    is_child = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'is_child', 'partner')


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
