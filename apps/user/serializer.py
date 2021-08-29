from rest_framework import serializers

from apps.user.models import ParentChildPair, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name')


class ParentChildSerializer(serializers.ModelSerializer):
    child = UserSerializer()
    parent = UserSerializer()

    class Meta:
        model = ParentChildPair
        fields = ('id', 'child', 'parent')


class UserPartnerSerializer(serializers.ModelSerializer):
    partner = ParentChildSerializer()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'partner')
