from django.db import models
from datetime import timedelta, datetime
import uuid

from django.utils import timezone


class QRCodeModel(models.Model):
    user = models.ForeignKey('users.UserModel', on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.code)

    def is_expired(self):
        # Use timezone.now() to get the current time with timezone info
        return timezone.now() > self.expired_at or self.expired_at is None

    def save(self, *args, **kwargs):
        if not self.id:  # Only for new instances, not for updates
            # Delete previous instances if any
            previous_codes = QRCodeModel.objects.filter(user=self.user)
            previous_codes.delete()

            # Set expiration time for the new instance
            self.expired_at = timezone.now() + timedelta(minutes=5)

        super().save(*args, **kwargs)


class FoodIntakeRecord(models.Model):
    user = models.ForeignKey('users.UserModel', on_delete=models.CASCADE)
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.taken_at}"



