from django.urls import path
from .views import *

urlpatterns = [
    path('cities/', CityView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDeleteUpdateView.as_view(), name='city-detail'),
    path('places/', PlaceTypeView.as_view(), name='place-type-list'),
    path('places/venue/', PlaceWiseVenueView.as_view(), name='place-type-detail'),
#     for venues
    path('venues/', VenueCreateListView.as_view(), name='venue-list'),
    path('venues/create/', VenueCreateView.as_view(), name='venue-list'),
    path('venues/<int:pk>/', VenueDetailView.as_view(), name='venue-detail'),
    path('venues/city/<int:city_id>/', VenueByCityView.as_view(), name='venue-list-by-city'),
    path("nearest-venues/", NearestVenueView.as_view(), name="nearest-venues"),
    path("scavenger-hunts/", ScavengerHuntViews.as_view(), name="scavenger-hunt-list"),
    path("user-scavenger-hunts/<int:pk>/", UserScavengerHuntUpdateView.as_view(), name="user-scavenger-hunt-update"),
    # GeoFencedViews
    path('geofences/', GeoFencedViews.as_view(), name='geofence-list'),
]
