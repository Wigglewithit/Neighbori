from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('skills/', include('skills.urls')),
    path('messages/', include('messaging.urls')),
    path('trades/', include('trades.urls')),
    path('', lambda request: redirect('messages:inbox'), name='home'),
    path('users/', include('users.urls')),
    path('accounts/', include('users.urls')),
    path('locations/', include('locations.urls')),
    path('profile/', include('profiles.urls')),
    path('api/profile/', include('profiles.urls')),


]
