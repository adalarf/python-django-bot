from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    class Meta:
        verbose_name = 'Admin_User'
