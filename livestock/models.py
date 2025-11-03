from django.db import models
from accounts.models import CustomUser

class Livestock(models.Model):
    CATEGORY_CHOICES = [
        ('cattle', 'Cattle'),
        ('donkey', 'Donkey'),
        ('goat', 'Goat'),
        ('sheep', 'Sheep'),
        ('poultry', 'Poultry'),
        ('pig', 'Pig'),
        

    ]
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='livestock')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    age =  models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='livestock_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.category}"
