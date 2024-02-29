from django import forms
from users.models import UserProfile
from .models import Blog

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'display_name', 'skill_occupation', 'bio', 'profile_image']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
