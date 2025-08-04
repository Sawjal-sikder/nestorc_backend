from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *

class CityView(generics.ListCreateAPIView):
      serializer_class = CitySerializer
      permission_classes = [permissions.AllowAny]
      parser_classes = [MultiPartParser, FormParser]


      def get(self, request, *args, **kwargs):
          cities = City.objects.all()
          serializer = self.get_serializer(cities, many=True)
          return Response(serializer.data)

      def post(self, request, *args, **kwargs):
            if not request.user.is_superuser:
                return Response({"error": "Only superusers are allowed to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)
          
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                  city = serializer.save()
                  return Response(self.get_serializer(city).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAdminUser]
# use method get for retrieving a city
    def get(self, request, *args, **kwargs):
        city = self.get_object()
        serializer = self.get_serializer(city)
        return Response(serializer.data)
# use method put for updating a city
    def put(self, request, *args, **kwargs):
        city = self.get_object()
        serializer = self.get_serializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            city = serializer.save()
            return Response(self.get_serializer(city).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# use method delete for deleting a city
    def delete(self, request, *args, **kwargs):
        city = self.get_object()
        city.delete()
        return Response(
                  {"message": "City deleted successfully"},
                  status=status.HTTP_200_OK 
            )
        
        
        
class VenueCreateListView(generics.ListCreateAPIView):
    serializer_class = VenueSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        venues = Venue.objects.all()
        serializer = self.get_serializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "Only superusers are allowed to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            venue = serializer.save()
            return Response(self.get_serializer(venue).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class VenueByCityView(generics.ListAPIView):
    serializer_class = VenueSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Venue.objects.filter(city_id=city_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)