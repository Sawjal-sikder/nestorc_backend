from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PlaceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

  
class Venue(models.Model):
    city = models.ForeignKey(City, related_name='venues', on_delete=models.CASCADE)
    type_of_place = models.ForeignKey(PlaceType, related_name='venues', on_delete=models.CASCADE)
    venue_name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='venue_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.venue_name
    
    
class GeoFenced(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class LatLng(models.Model):
    geo_fenced_area = models.ForeignKey(
        GeoFenced,
        related_name="polygon_points",
        on_delete=models.CASCADE
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"
