from django.db import models
from app.internal.models.checking_account import CheckingAccount


class Transaction(models.Model):
    sender_account = models.ForeignKey(CheckingAccount, on_delete=models.PROTECT,
                                       related_name="sender_account", db_index=True)
    receiver_account = models.ForeignKey(CheckingAccount, on_delete=models.PROTECT,
                                         related_name="receiver_account", db_index=True)
    money_amount = models.DecimalField(max_digits=20, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
