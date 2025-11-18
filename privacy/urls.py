from .views import privacy_policy
from django.urls import path
urlpatterns = [
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
]