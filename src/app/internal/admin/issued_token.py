from django.contrib import admin
from app.internal.models.issued_token import IssuedToken


@admin.register(IssuedToken)
class IssuedTokenAdmin(admin.ModelAdmin):
    list_display = ("jti", "user", "created_at", "revoked")
