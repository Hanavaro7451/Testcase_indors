from rest_framework import serializers
from user.models import Message, Owner
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


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    sender_id = serializers.IntegerField(source='sender.id', read_only=True)
    recipient = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all())
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'sender_id',
            'recipient',
            'recipient_username',
            'content',
            'timestamp'
        ]
        read_only_fields = ['id', 'sender', 'sender_id', 'recipient_username', 'timestamp']
