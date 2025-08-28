from django.core.files.storage import default_storage
from rest_framework import serializers
from django.utils import timezone
from .models import *
import json

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
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type_of_place = serializers.SlugRelatedField(slug_field="name", read_only=True)
    

    class Meta:
        model = Venue
        fields = ["id", "city", "type_of_place", "venue_name", "image", "description", "latitude", "longitude", "distance_km", "scavenger_hunts"]

class CreateVenueSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    type_of_place = serializers.PrimaryKeyRelatedField(queryset=PlaceType.objects.all())
    
    scavenger_hunts = serializers.CharField(
        required=False,
        write_only=True,
        allow_blank=True
    )

    class Meta:
        model = Venue
        fields = [
            "id", "city", "type_of_place", 
            "venue_name", "image", "description", "latitude", "longitude", "scavenger_hunts"
        ]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        """Override to return names instead of IDs in the response"""
        data = super().to_representation(instance)
        # Replace IDs with names
        data['city'] = instance.city.name if instance.city else None
        data['type_of_place'] = instance.type_of_place.name if instance.type_of_place else None
        return data

    def to_internal_value(self, data):
        # Debug: Print raw request data
        # print(f"Raw request data: {data}")
        
        # Create a mutable copy of the data but don't modify scavenger_hunts here
        if hasattr(data, 'copy'):
            data = data.copy()
        
        # Just print what we received for scavenger_hunts
        if 'scavenger_hunts' in data:
            print(f"Raw scavenger_hunts: {data['scavenger_hunts']}")
        
        return super().to_internal_value(data)

    def create(self, validated_data):
        # print(f"Validated Data: {validated_data}")
        scavenger_hunts_data = validated_data.pop("scavenger_hunts", [])
        # print(f"Scavenger Hunts Data: {scavenger_hunts_data}")
        # print(f"Scavenger Hunts Type: {type(scavenger_hunts_data)}")

        venue = Venue.objects.create(**validated_data)

        # Handle scavenger hunts data - could be string, list, or dict
        if isinstance(scavenger_hunts_data, str):
            import json
            try:
                scavenger_hunts_data = json.loads(scavenger_hunts_data)
            except json.JSONDecodeError:
                scavenger_hunts_data = []
        
        if isinstance(scavenger_hunts_data, list):
            for hunt_data in scavenger_hunts_data:
                title = hunt_data.get('title', '') if isinstance(hunt_data, dict) else str(hunt_data)
                if title:
                    ScavengerHunt.objects.create(venue=venue, title=title)

        return venue


    
    
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
        fields = ["id", "title", "alertMessage", "polygon_points", "isRestricted"]

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

    def update(self, instance, validated_data):
        # Update simple fields
        instance.title = validated_data.get("title", instance.title)
        instance.alertMessage = validated_data.get("alertMessage", instance.alertMessage)
        instance.isRestricted = validated_data.get("isRestricted", instance.isRestricted)
        instance.save()

        # Handle polygon_points
        polygon_points_data = validated_data.pop("polygon_points", None)
        if polygon_points_data is not None:
            # Remove old points
            instance.polygon_points.all().delete()
            # Add new ones
            for point_data in polygon_points_data:
                LatLng.objects.create(geo_fenced_area=instance, **point_data)

        return instance
