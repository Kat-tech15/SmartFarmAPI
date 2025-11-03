from django.db import models
from accounts.models import CustomUser

class Crop(models.Model):
    CROP_TYPE_CHOICES = [
        ('cereals', 'Cereals'),
        ('legumes', 'Legumes'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits')
    ]
    planter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='crops')
    title = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=100, choices=CROP_TYPE_CHOICES)
    price_per_kg  = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    #image = models.ImageField(upoad_to='crop_images/' null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.crop_type}"