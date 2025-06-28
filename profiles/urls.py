from django.urls import path
import profiles.views as views

app_name = 'profiles'

urlpatterns = [
    path('directory/', views.user_directory, name='directory'),  # 🟢 Put this FIRST
    path('edit/', views.edit_profile_view, name='edit-profile'),
    path('me/', views.my_profile, name='my-profile'),
    path('<str:username>/', views.profile_detail, name='profile_detail'),  # 🟡 LAST
]
