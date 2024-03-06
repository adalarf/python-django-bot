from django.db import models
from app.internal.models.user import User
from django.core.validators import MinValueValidator


class CheckingAccount(models.Model):
    account_number = models.DecimalField(primary_key=True, max_digits=20, decimal_places=0,
                                         validators=[MinValueValidator(10000000000000000000)])
    owner = models.ForeignKey(User, on_delete=models.PROTECT)