from django.contrib import admin
from .models import CommunityProfile
from locations.models import County

@admin.register(CommunityProfile)
class CommunityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'location_scope', 'connection_status', 'is_mentor')
    list_filter = ('region', 'location_scope', 'connection_status', 'is_mentor')

