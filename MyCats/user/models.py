from django.db import models
from django.contrib.auth.models import AbstractUser


class Owner(AbstractUser):
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(
        Owner,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    recepient = models.ForeignKey(
        Owner,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recepient.username}"
