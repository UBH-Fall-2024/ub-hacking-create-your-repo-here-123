# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, null=True, blank=True)

    # Add related_name to avoid clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Specify a unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Specify a unique related_name
        blank=True,
    )
