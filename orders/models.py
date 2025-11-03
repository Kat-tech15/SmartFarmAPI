from django.db import models
from accounts.models import CustomUser
from crops.models import Crop
from livestock.models import Livestock

class Order(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    livestock = models.ForeignKey(Livestock, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.d}"
