from django.db import models
from app.internal.users.db.models import User


class IssuedToken(models.Model):
    jti = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="refresh_tokens")
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
