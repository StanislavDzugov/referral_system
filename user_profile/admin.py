from django.contrib import admin
from user_profile import models
from user_profile.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number')


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_referral_code', 'activated_referral_code', 'reg_date')
