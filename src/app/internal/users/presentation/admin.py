from django.contrib import admin
from app.internal.users.db.models import User
from app.internal.users.db.models import AdminUser
from django.contrib.auth.admin import UserAdmin


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number")
