from rest_framework import serializers
from . models import Livestock

class LivestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestock
        fields = ['id','name', 'farmer', 'category', 'age', 'price']
        read_only_fields = ['farmer']
