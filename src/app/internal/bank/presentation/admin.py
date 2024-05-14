from django.contrib import admin
from app.internal.bank.db.models import CheckingAccount, Card, Transaction


@admin.register(CheckingAccount)
class CheckingAccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "balance", "owner")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("card_number", "expiration_date", "cvv_code", "checking_account")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("sender_account", "receiver_account", "money_amount", "datetime")
