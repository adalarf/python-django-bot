from django.db import models
from app.internal.models.checking_account import CheckingAccount
from django.core.validators import MaxValueValidator, MinValueValidator


class Card(models.Model):
    id = models.IntegerField(primary_key=True)
    card_number = models.CharField(max_length=16, unique=True)
    expiration_date = models.DateField()
    cvv_code = models.CharField(max_length=3)
    checking_account = models.ForeignKey(CheckingAccount, on_delete=models.PROTECT)
