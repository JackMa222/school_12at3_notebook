from django import forms
from .models import Organiser, PaymentBody, Payment, Event, Match
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
        
class PaymentBodyForm(forms.ModelForm):
    name = forms.CharField(
        label="Payment Body Name",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter payment body name'
        })
    )
    
    class Meta:
        model = PaymentBody
        fields = ['name']
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        
        fields = ['name', 'amount', 'payment_status', 'payment_body', 'matches', 'events']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. HNSW26-01'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full pl-6',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'payment_body': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'matches': forms.CheckboxSelectMultiple(),
            'events': forms.CheckboxSelectMultiple()
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['payment_body'].queryset = PaymentBody.objects.filter(user=user)
            self.fields['payment_body'].empty_label = "Select Payment Body"
            
            self.fields['matches'].queryset = Match.objects.filter(user=user)
            self.fields['events'].queryset = Event.objects.filter(user=user)
            
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        
        fields = ['name', 'starting_date', 'ending_date', 'location', 'roles', 'organiser']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. 2026 HNSW U16 FSC'
            }),
            'starting_date': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
            'ending_date': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. Hobart, Tasmania'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full pl-6',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'organiser': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'roles': forms.SelectMultiple(attrs={
                'class': 'select select-bordered w-full'
            })
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['organiser'].queryset = Organiser.objects.filter(user=user)
            self.fields['organiser'].empty_label = "Select Organiser"
            
class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        
        fields = ['title', 'date_time', 'venue', 'grade', 'roles', 'payment_fee', 'competition']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. Belgium vs Germany (Final)'
            }),
            'date_time': forms.DateTimeInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'type': 'datetime-local'
            }),
            'venue': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. Sydney Olympic Park OP1'
            }),
            'grade': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'e.g. PL1'
            }),
            'roles': forms.SelectMultiple(attrs={
                'class': 'select select-bordered w-full'
            }),
            'payment_fee': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full pl-6',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'competition': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            })            
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['roles'].empty_label = "Select Role"
        
        if user:
            self.fields['competition'].queryset = Event.objects.filter(user=user)
            self.fields['competition'].empty_label = "Select Competition"