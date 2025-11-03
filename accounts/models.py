from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer')
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='farmer')
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} ({self.role})"