from rest_framework import serializers
from user.models import Owner
from cats.models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['id', 'name', 'age', 'breed', 'owner']
        read_only_fields = ['id', 'owner']


class OwnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Owner
        fields = ['id', 'username', 'email', 'age', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Owner.objects.create_user(password=password, **validated_data)
        return user
