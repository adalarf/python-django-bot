from django.contrib import admin

from app.internal.models.checking_account import CheckingAccount


@admin.register(CheckingAccount)
class CheckingAccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "balance", "owner")
