from rest_framework.response import Response
from rest_framework.views  import APIView
from django.http import Http404
from rest_framework import status
from .serializers import CropSerializer
from .models import Crop

class CropList(APIView):
    def get(self, request):
        crops = Crop.objects.all()
        serializer = CropSerializer(crops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CropSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CropDetail(APIView):
    def get_obj(request, pk):
        try:
            crop = Crop.objects.get(pk=pk)
        except Crop.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        crop = self.get_obj(pk)
        serializer = CropSerializer(crop)
    
    def put(self, request, pk):
        crop =  self.get_obj(pk)
        serializer = CropSerializer(crop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        crop = self.get_obj(pk)
        crop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
