from django.urls import path
from .views import profile_detail_view
from .views import SkillProfileUpdateView
from .views import edit_profile_view


urlpatterns = [
    path('<str:username>/', profile_detail_view, name='profile_detail'),
    path('me/', SkillProfileUpdateView.as_view(), name='my-profile'),
    path('edit/', edit_profile_view, name='edit-profile'),

]
