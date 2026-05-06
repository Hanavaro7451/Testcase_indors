from django.db import models
from django.contrib.auth.models import AbstractUser


class Owner(AbstractUser):
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
