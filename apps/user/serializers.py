from django.db.models import Q
from rest_framework import serializers

from apps.user.models import ParentChildPair, User


class UserSerializer(serializers.ModelSerializer):
    is_child = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'is_child')


class ParentChildPairSerializer(serializers.ModelSerializer):
    def unique_parent_and_child(user_pk: int):
        if ParentChildPair.objects.filter(
                Q(parent_id=user_pk) | Q(child_id=user_pk)).exists():
            raise serializers.ValidationError(
                'Already associated with another ParentChildPair.')

    child = UserSerializer(read_only=True)
    parent = UserSerializer(read_only=True)
    child_id = serializers.IntegerField(
        write_only=True,
        validators=(unique_parent_and_child, ),
    )
    parent_id = serializers.IntegerField(
        write_only=True,
        validators=(unique_parent_and_child, ),
    )

    class Meta:
        model = ParentChildPair
        fields = ('id', 'child', 'parent', 'child_id', 'parent_id')


class UserPartnerSerializer(serializers.ModelSerializer):
    partner = ParentChildPairSerializer()
    is_child = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'is_child', 'partner')


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
