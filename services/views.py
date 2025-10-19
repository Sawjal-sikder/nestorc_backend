from traitlets import Any
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from .utils import haversine
from django.shortcuts import get_object_or_404


class CityView(generics.ListCreateAPIView):
      serializer_class = CitySerializer
      permission_classes = [permissions.AllowAny]


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

class PlaceTypeView(generics.ListCreateAPIView):
    queryset = PlaceType.objects.all()
    serializer_class = PlaceTypeSerializer
    permission_classes = [permissions.IsAdminUser]
    
    
class CreateVenueMessageView(generics.ListCreateAPIView):
    serializer_class = CreateVenueMessageSerializer
    queryset = List_Message.objects.all()

class VenueMessageDetailView(generics.ListAPIView):
    serializer_class = VenueMessageSerializer
    
    def get_queryset(self):
        venue_id = self.kwargs.get("venue_id")
        return List_Message.objects.filter(venue_id=venue_id)

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

class VenueAdminCreateListView(generics.ListCreateAPIView):
    serializer_class = VenueAdminSerializer
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
    



    
class VenueCreateView(generics.ListCreateAPIView):
    serializer_class = CreateVenueSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Venue.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            venue = serializer.save()
            return Response(self.get_serializer(venue).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VenueUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Venue.objects.all()
    serializer_class = UpdateVenueSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        venue = self.get_object()
        serializer = self.get_serializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            venue = serializer.save()
            return Response(self.get_serializer(venue).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        venue = self.get_object()
        serializer = self.get_serializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            venue = serializer.save()
            return Response(self.get_serializer(venue).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
  
  
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


class PlaceWiseVenueView(APIView):
    serializer_class = PlaceWiseVenueSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = {}
        categories = PlaceType.objects.prefetch_related("venues").all()
        for category in categories:
            venues = category.venues.all()[:5]  # limit to 5 venues
            data[category.name] = VenueSerializer(venues, many=True).data
        return Response(data)


class ScavengerHuntViews(generics.ListCreateAPIView):
    queryset = ScavengerHunt.objects.all()
    serializer_class = ScavengerCreateHuntSerializer
    

class UserScavengerHuntUpdateView(generics.UpdateAPIView):
    serializer_class = UserScavengerHuntUpdateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        scavenger_hunt_id = self.kwargs["pk"]
        obj, _ = UserScavengerHunt.objects.get_or_create(
            user=self.request.user,
            scavenger_hunt_id=scavenger_hunt_id,
        )
        return obj

 
    

class GeoFencedViews(generics.ListCreateAPIView):
    queryset = GeoFenced.objects.all()
    serializer_class = GeoFencedSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionError("Only superusers can create geofences.")
        serializer.save()

class GeoFencedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoFenced.objects.all()
    serializer_class = GeoFencedSerializer


class NearestVenueView(APIView):
    def get(self, request):
        try:
            user_lat = float(request.query_params.get("lat"))
            user_lon = float(request.query_params.get("lon"))
        except (TypeError, ValueError):
            return Response({"error": "lat and lon query parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        venues = Venue.objects.all()

        venue_list = []
        for v in venues:
            distance = haversine(user_lat, user_lon, v.latitude, v.longitude)
            venue_list.append({
                "id": v.id,
                "city": v.city_id,
                "venue_name": v.venue_name,
                "image": v.image.url if v.image else None,
                "latitude": v.latitude,
                "longitude": v.longitude,
                "distance_km": round(distance, 2),
            })

        # Sort by distance and get nearest 2
        nearest = sorted(venue_list, key=lambda x: x["distance_km"])[:2]

        return Response(nearest, status=status.HTTP_200_OK)


class NearestVenueTenView(APIView):
    def get(self, request):
        try:
            user_lat = float(request.query_params.get("lat"))
            user_lon = float(request.query_params.get("lon"))
        except (TypeError, ValueError):
            return Response({"error": "lat and lon query parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        venues = Venue.objects.all()

        venue_list = []
        for v in venues:
            distance = haversine(user_lat, user_lon, v.latitude, v.longitude)
            venue_list.append({
                "id": v.id,
                "city": v.city_id,
                "venue_name": v.venue_name,
                "image": v.image.url if v.image else None,
                "latitude": v.latitude,
                "longitude": v.longitude,
                "distance_km": round(distance, 2),
            })

        # Sort by distance and get nearest 10
        nearest = sorted(venue_list, key=lambda x: x["distance_km"])[:10]

        return Response(nearest, status=status.HTTP_200_OK)



class CityVenuesAPIView(APIView):
    def get(self, request):
        cities = City.objects.all()
        serializer = CityByVenueSerializer(cities, many=True)
        return Response(serializer.data)
    
    
class CreateStopView(generics.CreateAPIView):
    serializer_class = CreateStopSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            stop = serializer.save()
            return Response(self.get_serializer(stop).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ListStopView(generics.ListAPIView):
    serializer_class = ListStopSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Venue.objects.prefetch_related('stops').filter(stops__isnull=False).distinct()

