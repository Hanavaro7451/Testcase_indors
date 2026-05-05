from django.db import models

from django.conf import settings


class Cat(models.Model):
    name = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cats'
    )

    def __str__(self):
        return self.name
