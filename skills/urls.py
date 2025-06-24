from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_feed, name='skill_feed'),
    path('post/', views.create_post_view, name='create_post'),
    path('<int:post_id>/', views.skill_detail, name='skill_detail'),
]
