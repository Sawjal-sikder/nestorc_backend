from django.core.files.storage import default_storage
from rest_framework import serializers
from django.utils import timezone
from .models import *

class CitySerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = City
        fields = ['id', 'name', 'imageUrls', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        city = City.objects.create(**validated_data)

        image_urls = []
        for image in images:
            # Save each file manually
            path = default_storage.save(f"city_images/{image.name}", image)
            full_url = self.context['request'].build_absolute_uri(default_storage.url(path))
            image_urls.append(full_url)

        city.imageUrls = image_urls
        city.save()
        return city


class VenueSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Venue
        fields = ['id', 'city', 'venue_name', 'image', 'status_text', 'open_time', 'close_time', 'lat', 'lon']
        
        
    def get_status_text(self, obj):
        if obj.open_time and obj.close_time:
            now = timezone.localtime().time()
            print(f"Current time: {now}, Open time: {obj.open_time}, Close time: {obj.close_time}")
            if obj.open_time <= now <= obj.close_time:
                return "Open"
            else:
                return "Closed"
        return "Always Open"

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        venue = Venue.objects.create(**validated_data)

        if image:
            path = default_storage.save(f"venue_images/{image.name}", image)
            venue.image = path  
            venue.save()

        return venue