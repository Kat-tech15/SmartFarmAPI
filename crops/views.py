from rest_framework import generics, permissions
from .models import Crop
from .serializers import CropSerializer


<<<<<<< HEAD
class CropDetail(APIView):
    def get_obj(self, pk):
        try:
            return  Crop.objects.get(pk=pk)
        except Crop.DoesNotExist:
            raise Http4
    
    def get(self, request, pk):
        crop = self.get_obj(pk)
        serializer = CropSerializer(crop)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
=======
class CropList(generics.ListCreateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CropDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
>>>>>>> 4294538fb763fe93126bc76c703e502ff3037e80
