from django.contrib import admin
from .models import SkillProfile
from locations.models import County

@admin.register(SkillProfile)
class SkillProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('counties',)
    search_fields = ('user__username', 'skills_offered', 'skills_wanted')
    list_filter = ('trade_preferences', 'state', 'allow_lurkers', 'open_to_connections')

