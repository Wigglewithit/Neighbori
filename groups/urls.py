from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.group_list, name='list'),
    path('create/', views.create_group, name='create'),
    path('<int:pk>/', views.group_detail, name='detail'),
    path('<int:pk>/join/', views.join_group, name='join'),





]
