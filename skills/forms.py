from django import forms
from .models import SkillPost

class SkillPostForm(forms.ModelForm):
    class Meta:
        model = SkillPost
        fields = [ 'post_type','title', 'skill', 'description', 'tags', 'image', 'visibility']
        widgets = {
            'post_type': forms.Select(attrs={'class': 'w-full mt-1 p-2 border border-gray-300 rounded-md bg-blue-50'}),
            'title': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border border-gray-300 rounded-md bg-blue-50'}),
            'skill': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border border-gray-300 rounded-md bg-blue-50'}),
            'description': forms.Textarea(attrs={'class': 'w-full mt-1 p-2 border border-gray-300 rounded-md bg-blue-50', 'rows': 5}),
            'tags': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border border-gray-300 rounded-md bg-blue-50', 'placeholder': 'e.g. coding, design, carpentry'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full mt-1 p-2 border border-gray-300 rounded-md bg-blue-50'}),
            'visibility': forms.Select(attrs={'class': 'w-full mt-1 p-2 border border-gray-300 rounded-md bg-blue-50'}),
        }