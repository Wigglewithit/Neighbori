from django import forms
from .models import SkillProfile
from locations.models import County, State, ZipCode

class ProfileForm(forms.ModelForm):
    class Meta:
        model = SkillProfile
        fields = [
            'bio', 'skills_offered', 'skills_wanted',
            'state', 'counties', 'city', 'zipcode', 'search_radius'
        ]
        widgets = {
            'counties': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['counties'].queryset = County.objects.all()
        self.fields['counties'].help_text = "Hold Ctrl or Cmd to select multiple."
