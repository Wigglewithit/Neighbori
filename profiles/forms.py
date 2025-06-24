from django import forms
from .models import CommunityProfile
from locations.models import County, State, ZipCode

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CommunityProfile
        fields = [
            'bio', 'skills_offered', 'skills_wanted', 'interests',
            'connection_status', 'location_scope', 'region', 'counties',
            'zipcode', 'available_for', 'profile_picture', 'is_mentor', 'allow_lurkers', 'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full p-2 border border-blue-200 rounded bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-300'
            })
        self.fields['counties'].help_text = "Hold Ctrl or Cmd to select multiple."
