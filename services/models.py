from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    imageUrls = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
  
class Venue(models.Model):
    city = models.ForeignKey(City, related_name='venues', on_delete=models.CASCADE)
    venue_name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='venue_images/', blank=True, null=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    lat = models.FloatField()
    lon = models.FloatField() 
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.venue_name