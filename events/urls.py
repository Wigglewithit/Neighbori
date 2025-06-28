from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='list'),
    path('create/', views.create_event, name='create'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('<int:pk>/rsvp/', views.rsvp_event, name='rsvp'),





]
