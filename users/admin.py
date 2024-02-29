from django.contrib import admin
from .models import Users, UserProfile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields  = ['first_name', 'last_name' ,'username', 'email']
    list_display  = ['first_name',  'last_name','username', 'email']


admin.site.register(Users, UserAdmin)
admin.site.register(UserProfile)