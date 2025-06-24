from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('skills/', include('skills.urls')),
    path('messages/', include('messaging.urls')),
    path('trades/', include('trades.urls')),
    path('', lambda request: redirect('messages:inbox'), name='home'),
    path('users/', include('users.urls')),
    path('accounts/', include('users.urls')),
    path('locations/', include('locations.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
