from django.urls import path
from .views import feed, discover_api

urlpatterns = [
    path('', feed, name='discover_feed'),
    path('api/', discover_api, name='discover_api'),
]
