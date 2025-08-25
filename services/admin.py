from django.contrib import admin

from services.models import UserScavengerHunt

# Register your models here.
@admin.register(UserScavengerHunt)
class UserScavengerHuntAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "scavenger_hunt", "checked", "uploaded_image"]
    search_fields = ["user__username", "scavenger_hunt__title"]