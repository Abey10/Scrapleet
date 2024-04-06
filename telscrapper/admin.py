from django.contrib import admin
from .models import TelegramAccount, TelegramUser


# Register your models here.
admin.site.register(TelegramAccount)
admin.site.register(TelegramUser)