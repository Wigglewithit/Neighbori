from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'visibility']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded px-4 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-4 py-2'}),
            'visibility': forms.Select(attrs={'class': 'w-full border rounded px-4 py-2'}),
        }
