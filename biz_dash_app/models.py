from django.db import models
from django.contrib.auth.models import AbstractUser 

class CustomUser (AbstractUser ):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    manager = models.ForeignKey('self', related_name='staff_members', null=True, blank=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['first_name', 'last_name']