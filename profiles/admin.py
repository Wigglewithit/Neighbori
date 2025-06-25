from django.contrib import admin
from .models import CommunityProfile
from locations.models import County


@admin.register(CommunityProfile)
class CommunityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_state', 'connection_status', 'location_scope')
    list_filter = ('state', 'connection_status', 'location_scope')

    def get_state(self, obj):
        return obj.state.name if obj.state else "—"
    get_state.short_description = 'State'