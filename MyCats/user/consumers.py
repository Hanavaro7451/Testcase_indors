import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from user.models import Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.room_group_name = f"user_{user.id}"
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        recipient_id = data.get("recipient")
        content = data.get("content")

        if not recipient_id or not content:
            return

        message = await self.create_message(
            self.scope["user"], recipient_id, content
        )

        if message:
            payload = {
                "id": message.id,
                "sender": message.sender.username,
                "recipient": message.recipient.username,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
            }
            await self.channel_layer.group_send(
                f"user_{recipient_id}",
                {"type": "chat.message", "message": payload}
            )
            await self.send(text_data=json.dumps(payload))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def create_message(self, sender, recipient_id, content):
        try:
            recipient = User.objects.get(pk=recipient_id)
        except User.DoesNotExist:
            return None
        return Message.objects.create(
            sender=sender,
            recipient=recipient,
            content=content
        )