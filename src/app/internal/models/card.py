from django.db import models
from app.internal.models.checking_account import CheckingAccount
from django.core.validators import MaxValueValidator, MinValueValidator


class Card(models.Model):
    card_number = models.DecimalField(primary_key=True, max_digits=16, decimal_places=0,
                                      validators=[MinValueValidator(1000000000000000)])
    balance = models.FloatField()
    expiration_date = models.DateField()
    cvv_code = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(999)])
    checking_account = models.ForeignKey(CheckingAccount, on_delete=models.PROTECT)