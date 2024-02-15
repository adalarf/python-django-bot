from django.contrib import admin

from app.internal.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number")