from django.core.files.storage import default_storage
from rest_framework import serializers
from django.utils import timezone
from .models import *

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name', 'description']


class VenueSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = Venue
        fields = ["id", "city", "venue_name", "image", "description", "latitude", "longitude", "distance_km"]



class LatLngSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatLng
        fields = ["latitude", "longitude"]


class GeoFencedSerializer(serializers.ModelSerializer):
    polygon_points = LatLngSerializer(many=True)

    class Meta:
        model = GeoFenced
        fields = ["id", "title", "polygon_points"]

    def validate_polygon_points(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("A polygon must have at least 4 points.")
        return value

    def create(self, validated_data):
        polygon_points_data = validated_data.pop("polygon_points")
        geo_fenced_area = GeoFenced.objects.create(**validated_data)
        for point_data in polygon_points_data:
            LatLng.objects.create(geo_fenced_area=geo_fenced_area, **point_data)
        return geo_fenced_area