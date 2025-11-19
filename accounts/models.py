from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer')
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='farmer')
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class EmailOTP(models.Model):
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"
    
    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def expiry_time():
        return timezone.now() +timedelta(minutes=5)
    
    def is_expired(self):
        return timezone.now() > self.expire_at