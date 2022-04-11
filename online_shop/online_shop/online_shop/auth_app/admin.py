from django.contrib import admin

# Register your models here.

from online_shop.auth_app.models import AppUser


@admin.register(AppUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_superuser', 'is_staff',)
