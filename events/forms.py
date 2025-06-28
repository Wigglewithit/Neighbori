from django import forms
from .models import Event, Comment

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'visibility']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-4 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-4 py-2'}),
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full border rounded px-4 py-2'
            }),
            'location': forms.TextInput(attrs={'class': 'w-full border rounded px-4 py-2'}),
            'visibility': forms.Select(attrs={'class': 'w-full border rounded px-4 py-2'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'w-full border rounded px-4 py-2'
            }),
        }