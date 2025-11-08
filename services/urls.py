from django.urls import path
from .views import *

urlpatterns = [
    path('cities/', CityView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDeleteUpdateView.as_view(), name='city-detail'),
    path('places/', PlaceTypeView.as_view(), name='place-type-list'),
    path('places/<int:pk>/', PlaceTypeDetailView.as_view(), name='place-type-detail'),
    path('places/venue/', PlaceWiseVenueView.as_view(), name='place-type-detail'),
#     for venues
    path('venues/', VenueCreateListView.as_view(), name='venue-list'),
    path('venues/admin/', VenueAdminCreateListView.as_view(), name='venue-admin-list'),
    path('venues/create/', VenueCreateView.as_view(), name='venue-list'),
    path('venues/<int:pk>/', VenueDetailView.as_view(), name='venue-detail'),
    path('venues/update/<int:pk>/', VenueUpdateView.as_view(), name='venue-update'),
    path('venues/city/<int:city_id>/', VenueByCityView.as_view(), name='venue-list-by-city'),
    path("cities/venues/", CityVenuesAPIView.as_view(), name="city-venues"),
    path("nearest-venues/", NearestVenueView.as_view(), name="nearest-venues"),
    path("nearest-venues/more/limit/", NearestVenueTenView.as_view(), name="nearest-venues-10"),
    path("scavenger-hunts/", ScavengerHuntViews.as_view(), name="scavenger-hunt-list"),
    path("user-scavenger-hunts/<int:pk>/", UserScavengerHuntUpdateView.as_view(), name="user-scavenger-hunt-update"),
    # GeoFencedViews
    path('geofences/', GeoFencedViews.as_view(), name='geofence-list'),
    path('geofences/<int:pk>/', GeoFencedDetailView.as_view(), name='geofence-detail'),
    # for venue messages
    path('venues/message/create/', CreateVenueMessageView.as_view(), name='create-venue-message'),
    path('venues/message/<int:venue_id>/', VenueMessageDetailView.as_view(), name='message-list'),
    
    # for stops
    path('stops/create/', CreateStopView.as_view(), name='create-stop'),
    path('stops/list/', ListStopView.as_view(), name='stop-list'),
    
    # for nearby attractions
    path('nearby-attractions/', NearByAttractionView.as_view(), name='nearby-attraction'),
    path('nearby-attractions/<int:pk>/', NearByAttractionDetailView.as_view(), name='nearby-attraction-detail'),
]
