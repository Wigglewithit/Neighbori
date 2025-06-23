from rest_framework import serializers
from .models import SkillProfile

class SkillProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillProfile
        fields = [
            'bio',
            'skills_offered',
            'skills_wanted',
            'state',
            'counties',
            'city',
            'zipcode',
            'search_radius',
            'trade_preferences',
            'allow_lurkers',
            'open_to_connections',
            'availability',
        ]
        extra_kwargs = {
            'state': {'required': False},
            'counties': {'required': False},
            'city': {'required': False},
            'zipcode': {'required': False},
        }
