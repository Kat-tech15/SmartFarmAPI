from rest_framework import generics
from .serializers import CropSerializer
from .models import Crop

class CropList(generics.ListCreateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class CropDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    
