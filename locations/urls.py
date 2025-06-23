from django.urls import path
from . import views

urlpatterns = [
    path('select/', views.location_select_view, name='select_location'),
    path('ajax/load-counties/', views.load_counties, name='ajax_load_counties'),
    path('ajax/load-zips/', views.load_zipcodes, name='ajax_load_zips'),
]
