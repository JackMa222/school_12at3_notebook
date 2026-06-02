from django import forms
from .models import Organiser
#from django.contrib.auth import get_user_model

#User = get_user_model()

class OrganiserForm(forms.ModelForm):
    name = forms.CharField(
        label="Organiser Name",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter organisation name'
        })
    )
    
    class Meta:
        model = Organiser
        fields = ['name']