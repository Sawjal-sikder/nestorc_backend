from django.urls import path
from .views import *

urlpatterns = [
    path('cities/', CityView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDeleteUpdateView.as_view(), name='city-detail'),
#     for venues
    path('venues/', VenueCreateListView.as_view(), name='venue-list'),
    path('venues/city/<int:city_id>/', VenueByCityView.as_view(), name='venue-list-by-city'),
    # GeoFencedViews
    path('geofences/', GeoFencedViews.as_view(), name='geofence-list'),
]
