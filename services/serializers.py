from django.core.files.storage import default_storage
from rest_framework import serializers
from django.utils import timezone
from .models import *

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name', 'description']

class PlaceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceType
        fields = ['id', 'name', 'description']
        
class ScavengerCreateHuntSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScavengerHunt
        fields = ['id', 'venue', 'title']
        

class UserScavengerHuntSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScavengerHunt
        fields = ["checked", "uploaded_image"]


class ScavengerHuntSerializer(serializers.ModelSerializer):
    check = serializers.SerializerMethodField()
    # image = serializers.ImageField(required=False)  # if you have images

    class Meta:
        model = ScavengerHunt
        fields = ["id", "title", "check"]

    def get_check(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated:
            us = UserScavengerHunt.objects.filter(user=user, scavenger_hunt=obj).first()
            if us:
                return UserScavengerHuntSerializer(us).data
            return {"checked": False, "uploaded_image": None}
        return {"checked": False, "uploaded_image": None}



class VenueSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)
    scavenger_hunts = ScavengerHuntSerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = ["id", "city", "type_of_place", "venue_name", "image", "description", "latitude", "longitude", "distance_km", "scavenger_hunts"]

class UserScavengerHuntUpdateSerializer(serializers.ModelSerializer):
    check = serializers.BooleanField(source="checked", required=False)
    image = serializers.ImageField(source="uploaded_image", required=False)

    class Meta:
        model = UserScavengerHunt
        fields = ["check", "image"]

    def update(self, instance, validated_data):
        instance.checked = validated_data.get("checked", instance.checked)
        instance.uploaded_image = validated_data.get("uploaded_image", instance.uploaded_image)
        instance.save()
        return instance



class PlaceWiseVenueSerializer(serializers.ModelSerializer):
    venues = VenueSerializer(many=True)

    class Meta:
        model = PlaceType
        fields = ["id", "name", "venues",]
        

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
