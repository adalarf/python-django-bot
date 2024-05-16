from django.db import models
from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    class Meta:
        verbose_name = 'Admin_User'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    phone_number = models.CharField(max_length=255, null=True, verbose_name="Номер телефона")
    favorite_users = models.ManyToManyField("self", symmetrical=False, blank=True)
    password = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
