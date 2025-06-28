# skills/urls.py

from django.urls import path
from .views import skill_feed, create_post_view, skill_detail

urlpatterns = [
    path('', skill_feed, name='skill_feed'),
    path('create/', create_post_view, name='create_post'),
    path('<int:post_id>/', skill_detail, name='skill_detail'),

]
