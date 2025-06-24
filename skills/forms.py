from django import forms
from .models import SkillPost

class SkillPostForm(forms.ModelForm):
    class Meta:
        model = SkillPost
        fields = ['post_type', 'skill', 'description', 'tags', 'image', 'visibility']
        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. coding, design, carpentry'}),
        }
