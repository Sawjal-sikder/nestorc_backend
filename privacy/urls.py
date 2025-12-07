from .views import accountdeleteView, privacy_policy, supportView
from django.urls import path

urlpatterns = [
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('account-delete/', accountdeleteView, name='account_delete'),
    path('support/', supportView, name='support'),
]