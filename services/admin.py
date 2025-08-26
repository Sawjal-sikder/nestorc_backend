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