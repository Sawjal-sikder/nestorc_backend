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
        fields = ["id", "title", "image", "check"]

    def get_check(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated:
            us = UserScavengerHunt.objects.filter(user=user, scavenger_hunt=obj).first()
            if us:
                return UserScavengerHuntSerializer(us).data
            return {"checked": False, "uploaded_image": None}
        return {"checked": False, "uploaded_image": None}


class CreateVenueMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = List_Message
        fields = "__all__"

class ListMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = List_Message
        fields = ["id", "message",]
        
class VenueMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = List_Message
        fields = ["id", "message",]


class VenueSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)
    scavenger_hunts = ScavengerHuntSerializer(many=True, read_only=True)
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type_of_place = serializers.SlugRelatedField(slug_field="name", read_only=True)
    venue_message = ListMessageSerializer(many=True, read_only=True, source="messages")

    class Meta:
        model = Venue
        fields = ["id", "city", "type_of_place", "venue_name","venue_message", "image", "description", "latitude", "longitude", "distance_km", "scavenger_hunts"]

class CreateVenueSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    type_of_place = serializers.PrimaryKeyRelatedField(queryset=PlaceType.objects.all())
    scavenger_hunts = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )
    venue_message = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = Venue
        fields = [
            "id", "city", "type_of_place", 
            "venue_name", "image", "description", "latitude", "longitude","scavenger_hunts", "venue_message"
        ]
        read_only_fields = ["id"]

    def to_internal_value(self, data):
        """Handle FormData with nested arrays"""
        # Convert QueryDict/FormData to regular dict for easier processing
        if hasattr(data, 'dict'):
            # For QueryDict (FormData), use dict() to get all values
            data_dict = {}
            for key in data.keys():
                # Get all values for this key (in case of multiple values)
                values = data.getlist(key)
                if len(values) == 1:
                    data_dict[key] = values[0]
                else:
                    data_dict[key] = values
            data = data_dict
        elif hasattr(data, 'copy'):
            data = data.copy()
        
        # Parse scavenger_hunts from FormData format
        scavenger_hunts = []
        venue_messages = []
        
        # Extract all keys and group by pattern
        keys_to_remove = []
        for key, value in data.items():
            # Handle scavenger_hunts[index][field] pattern
            if key.startswith('scavenger_hunts[') and (key.endswith('][title]') or key.endswith('][image]')):
                try:
                    # Extract index and field from scavenger_hunts[0][title] or scavenger_hunts[0][image]
                    parts = key.split('[')
                    index = int(parts[1].split(']')[0])
                    field = parts[2].split(']')[0]  # 'title' or 'image'
                    
                    # Ensure we have enough items in the list
                    while len(scavenger_hunts) <= index:
                        scavenger_hunts.append({})
                    
                    scavenger_hunts[index][field] = value
                    keys_to_remove.append(key)
                except (ValueError, IndexError):
                    pass  # Skip invalid keys
            
            # Handle venue_message[index][field] pattern
            elif key.startswith('venue_message[') and key.endswith('][message]'):
                try:
                    # Extract index from venue_message[0][message]
                    index = int(key.split('[')[1].split(']')[0])
                    
                    # Ensure we have enough items in the list
                    while len(venue_messages) <= index:
                        venue_messages.append({})
                    
                    venue_messages[index]['message'] = value
                    keys_to_remove.append(key)
                except (ValueError, IndexError):
                    pass  # Skip invalid keys
        
        # Remove processed keys from data
        for key in keys_to_remove:
            if key in data:
                del data[key]
        
        # Add parsed arrays back to data
        if scavenger_hunts:
            data['scavenger_hunts'] = scavenger_hunts
        if venue_messages:
            data['venue_message'] = venue_messages
        
        return super().to_internal_value(data)
    def to_representation(self, instance):
        """Override to return names instead of IDs in the response"""
        data = super().to_representation(instance)
        # Replace IDs with names
        data['city'] = instance.city.name if instance.city else None
        data['type_of_place'] = instance.type_of_place.name if instance.type_of_place else None
        
        # Include related data in response
        data['scavenger_hunts'] = ScavengerHuntSerializer(instance.scavenger_hunts.all(), many=True).data
        data['venue_message'] = ListMessageSerializer(instance.messages.all(), many=True).data
        
        return data

    def create(self, validated_data):
        # Extract nested data
        scavenger_hunts_data = validated_data.pop('scavenger_hunts', [])
        venue_messages_data = validated_data.pop('venue_message', [])
        
        # Create the venue
        venue = Venue.objects.create(**validated_data)
        
        # Create scavenger hunts
        for hunt_data in scavenger_hunts_data:
            if 'title' in hunt_data:
                ScavengerHunt.objects.create(
                    venue=venue,
                    title=hunt_data['title'],
                    image=hunt_data.get('image', None)
                )
        
        # Create venue messages
        for message_data in venue_messages_data:
            if 'message' in message_data:
                List_Message.objects.create(
                    venue=venue,
                    message=message_data['message']
                )
        
        return venue


class UpdateVenueSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    type_of_place = serializers.PrimaryKeyRelatedField(queryset=PlaceType.objects.all())
    scavenger_hunts = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )
    venue_message = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = Venue
        fields = [
            "id", "city", "type_of_place", 
            "venue_name", "image", "description", "latitude", "longitude","scavenger_hunts", "venue_message"
        ]
        read_only_fields = ["id"]

    def to_internal_value(self, data):
        """Handle FormData with nested arrays"""
        # Convert QueryDict/FormData to regular dict for easier processing
        if hasattr(data, 'dict'):
            # For QueryDict (FormData), use dict() to get all values
            data_dict = {}
            for key in data.keys():
                # Get all values for this key (in case of multiple values)
                values = data.getlist(key)
                if len(values) == 1:
                    data_dict[key] = values[0]
                else:
                    data_dict[key] = values
            data = data_dict
        elif hasattr(data, 'copy'):
            data = data.copy()
        
        # Parse scavenger_hunts from FormData format
        scavenger_hunts = []
        venue_messages = []
        
        # Extract all keys and group by pattern
        keys_to_remove = []
        for key, value in data.items():
            # Handle scavenger_hunts[index][field] pattern
            if key.startswith('scavenger_hunts[') and (key.endswith('][title]') or key.endswith('][image]')):
                try:
                    # Extract index and field from scavenger_hunts[0][title] or scavenger_hunts[0][image]
                    parts = key.split('[')
                    index = int(parts[1].split(']')[0])
                    field = parts[2].split(']')[0]  # 'title' or 'image'
                    
                    # Ensure we have enough items in the list
                    while len(scavenger_hunts) <= index:
                        scavenger_hunts.append({})
                    
                    scavenger_hunts[index][field] = value
                    keys_to_remove.append(key)
                except (ValueError, IndexError):
                    pass  # Skip invalid keys
            
            # Handle venue_message[index][field] pattern
            elif key.startswith('venue_message[') and key.endswith('][message]'):
                try:
                    # Extract index from venue_message[0][message]
                    index = int(key.split('[')[1].split(']')[0])
                    
                    # Ensure we have enough items in the list
                    while len(venue_messages) <= index:
                        venue_messages.append({})
                    
                    venue_messages[index]['message'] = value
                    keys_to_remove.append(key)
                except (ValueError, IndexError):
                    pass  # Skip invalid keys
        
        # Remove processed keys from data
        for key in keys_to_remove:
            if key in data:
                del data[key]
        
        # Add parsed arrays back to data
        if scavenger_hunts:
            data['scavenger_hunts'] = scavenger_hunts
        if venue_messages:
            data['venue_message'] = venue_messages
        
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        """Override to return names instead of IDs in the response"""
        data = super().to_representation(instance)
        # Replace IDs with names
        data['city'] = instance.city.name if instance.city else None
        data['type_of_place'] = instance.type_of_place.name if instance.type_of_place else None
        
        # Include related data in response
        data['scavenger_hunts'] = ScavengerHuntSerializer(instance.scavenger_hunts.all(), many=True).data
        data['venue_message'] = ListMessageSerializer(instance.messages.all(), many=True).data
        
        return data

    def update(self, instance, validated_data):
        # Extract nested data
        scavenger_hunts_data = validated_data.pop('scavenger_hunts', [])
        venue_messages_data = validated_data.pop('venue_message', [])
        
        # Update the venue basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle scavenger hunts - replace all existing ones
        if scavenger_hunts_data:
            # Remove existing scavenger hunts
            instance.scavenger_hunts.all().delete()
            # Create new scavenger hunts
            for hunt_data in scavenger_hunts_data:
                if 'title' in hunt_data:
                    ScavengerHunt.objects.create(
                        venue=instance,
                        title=hunt_data['title'],
                        image=hunt_data.get('image', None)
                    )
        
        # Handle venue messages - replace all existing ones
        if venue_messages_data:
            # Remove existing venue messages
            instance.messages.all().delete()
            # Create new venue messages
            for message_data in venue_messages_data:
                if 'message' in message_data:
                    List_Message.objects.create(
                        venue=instance,
                        message=message_data['message']
                    )
        
        return instance


    
    
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



class VenueForCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'venue_name', 'image',] 


class CityByVenueSerializer(serializers.ModelSerializer):
    venues = serializers.SerializerMethodField()  

    class Meta:
        model = City
        fields = ['id', 'name',  'venues']

    def get_venues(self, obj):
        venues = obj.venues.all()[:2]  
        return VenueForCitySerializer(venues, many=True).data