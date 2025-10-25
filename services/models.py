from django.db import models

# from accounts.models import User

from django.contrib.auth import get_user_model
User = get_user_model()

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

class ScavengerHunt(models.Model):
    venue = models.ForeignKey('Venue', related_name='scavenger_hunts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="scavenger_hunts/", null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class UserScavengerHunt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scavenger_hunt = models.ForeignKey(ScavengerHunt, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    uploaded_image = models.ImageField(upload_to="user_scavenger_images/", null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.scavenger_hunt.title}"
    
class Stops(models.Model):
    Venue = models.ForeignKey('Venue', related_name='stops', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
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
    
    
class List_Message(models.Model):
    venue = models.ForeignKey(Venue, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message for {self.venue.venue_name}"
    
class GeoFenced(models.Model):
    title = models.CharField(max_length=100)
    alertMessage = models.TextField(blank=True, null=True)
    isRestricted = models.BooleanField(default=False)

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
