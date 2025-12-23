from rest_framework import serializers
from .models import Crop

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['id', 'planter', 'crop_type', 'price_per_kg', 'available', 'image', 'created_at']