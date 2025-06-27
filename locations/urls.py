from django.urls import path
from . import views
from .views import load_cities

urlpatterns = [
    path('select/', views.location_select_view, name='select_location'),
    path('ajax/load-counties/', views.load_counties, name='ajax_load_counties'),
    path('load-cities/', load_cities, name='load_cities'),
    path('locations/load-cities/', load_cities, name='load_cities'),

]
