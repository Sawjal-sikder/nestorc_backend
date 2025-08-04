from rest_framework import serializers
from django.core.files.storage import default_storage
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

    class Meta:
        model = Venue
        fields = ['id', 'city', 'venue_name', 'image', 'open_time', 'close_time', 'lat', 'lon']

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        venue = Venue.objects.create(**validated_data)

        if image:
            path = default_storage.save(f"venue_images/{image.name}", image)
            venue.image = path  
            venue.save()

        return venue