from django.contrib import admin

from services.models import *

# Register your models here.
@admin.register(UserScavengerHunt)
class UserScavengerHuntAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "scavenger_hunt", "checked", "uploaded_image"]
    search_fields = ["user__username", "scavenger_hunt__title"]
    
@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    
# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     list_display = ["id", "name", "state", "country"]
#     search_fields = ["name", "state__name", "country__name"]

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["id", "city", "type_of_place","venue_name","latitude","longitude"]
    # search_fields = ["name", "location__name"]