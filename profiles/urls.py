import profiles.views as views
from django.urls import path


app_name = 'profiles'
urlpatterns = [
    path('edit/', views.edit_profile_view, name='edit-profile'),
    path('me/', views.SkillProfileUpdateView.as_view(), name='my-profile'),
    path('<str:username>/', views.profile_detail, name='profile_detail'),
]

