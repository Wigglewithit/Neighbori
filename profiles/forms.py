from django import forms
from .models import CommunityProfile
from locations.models import County, State, City

class ProfileForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'id': 'id_state',
            'class': 'w-full p-2 border border-blue-200 rounded bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-300'
        })
    )

    class Meta:
        model = CommunityProfile
        fields = [
            'bio',
            'skills_offered',
            'skills_wanted',
            'interests',
            'gender',
            'age',
            'connection_status',
            'location_scope',
            'city',            # ← Will be updated by HTMX
            'available_for',
            'is_mentor',
            'allow_lurkers',
            'profile_picture',
        ]
        widgets = {
            'city': forms.Select(attrs={
                'id': 'id_city',
                'hx-get': '/locations/load-cities/',
                'hx-target': '#id_city',
                'hx-trigger': 'change from:#id_state',
                'class': 'w-full p-2 border border-blue-200 rounded bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-300'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs.update({
                    'class': 'w-full p-2 border border-blue-200 rounded bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-300'
                })

        self.fields['city'].queryset = City.objects.none()

        # If editing an existing profile with a city, load related cities
        if self.instance.pk and self.instance.city:
            self.fields['city'].queryset = City.objects.filter(state=self.instance.city.state).order_by('name')
            self.initial['state'] = self.instance.city.state

        # If coming from POST with state ID
        elif 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
