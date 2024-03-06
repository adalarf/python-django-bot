from django.contrib import admin

from app.internal.models.card import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("card_number", "balance", "expiration_date", "cvv_code", "checking_account")