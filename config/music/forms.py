from django import forms
from .models import Music

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = '__all__'

class MusicSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')