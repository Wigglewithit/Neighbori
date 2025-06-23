from django import forms
from .models import SkillExchangePost

class SkillExchangePostForm(forms.ModelForm):
    class Meta:
        model = SkillExchangePost
        fields = ['post_type', 'skill', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }