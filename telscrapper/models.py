from django.db import models
from django.conf import settings

class TelegramAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_id = models.IntegerField()
    api_hash = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

class TelegramUser(models.Model):
    username = models.CharField(max_length=255)
    user_id = models.IntegerField()
    access_hash = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    group_id = models.IntegerField()
    status = models.CharField(max_length=255)
    was_online = models.DateTimeField(null=True)
