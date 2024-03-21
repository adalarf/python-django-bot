from django.db import models
from app.internal.models.user import User
from django.core.validators import MinValueValidator


class CheckingAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    account_number = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
