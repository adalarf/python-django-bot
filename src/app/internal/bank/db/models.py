from django.db import models
from app.internal.users.db.models import User


class CheckingAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    account_number = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, db_index=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)


class Card(models.Model):
    id = models.IntegerField(primary_key=True)
    card_number = models.CharField(max_length=16, unique=True)
    expiration_date = models.DateField()
    cvv_code = models.CharField(max_length=3)
    checking_account = models.ForeignKey(CheckingAccount, on_delete=models.PROTECT, db_index=True)


class Transaction(models.Model):
    sender_account = models.ForeignKey(CheckingAccount, on_delete=models.PROTECT,
                                       related_name="sender_account", db_index=True)
    receiver_account = models.ForeignKey(CheckingAccount, on_delete=models.PROTECT,
                                         related_name="receiver_account", db_index=True)
    money_amount = models.DecimalField(max_digits=20, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)
    postcard = models.FileField(null=True)
