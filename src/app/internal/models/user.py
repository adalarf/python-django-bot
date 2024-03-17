from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    phone_number = models.CharField(max_length=255, null=True, verbose_name="Номер телефона")

    def __str__(self):
        return self.name
    