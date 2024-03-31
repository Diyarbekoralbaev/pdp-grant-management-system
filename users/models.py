import uuid
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, auto_created=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_cook = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_grant = models.BooleanField(default=False)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    courses_year = models.CharField(max_length=10, blank=True, null=True)
    group_number = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_time_eat = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    last_logged_device = models.TextField(blank=True, null=True)
    last_logged_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.username

    def validate_unique(self, exclude=None):
        if self.is_student:
            if self.student_id is None:
                raise ValueError('Student ID is required for student')
            if self.courses_year is None:
                raise ValueError('Courses year is required for student')
            if self.group_number is None:
                raise ValueError('Group number is required for student')
        super().validate_unique(exclude)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users'
        ordering = ['username']


class OTPModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_created=True, default=datetime.now() + timedelta(minutes=5), editable=False, blank=True, null=True)

    def __str__(self):
        return self.otp

    def is_expired(self):
        return datetime.now() > self.expires_at

    def is_valid(self, otp):
        return self.otp == otp and not self.is_expired()