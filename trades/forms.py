from django import forms
from .models import Trade

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['user_two', 'skill_given_by_user_one', 'skill_given_by_user_two']
