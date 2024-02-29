from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model

class Users(AbstractUser):
    agreed_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.username



class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    display_name = models.CharField(max_length=50, default='display_name')
    skill_occupation = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Profile Image
    profile_image = models.ImageField(upload_to='user_profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.display_name}"