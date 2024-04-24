from django.contrib import admin
from app.internal.models.transaction import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("sender_account", "receiver_account", "money_amount", "datetime")