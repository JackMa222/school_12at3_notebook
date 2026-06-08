from django import forms
from .models import Organiser, PaymentBody, Payment
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
        
        fields = ['name', 'amount', 'payment_status', 'payment_body']
        
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
            })
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['payment_body'].queryset = PaymentBody.objects.filter(user=user)
            self.fields['payment_body'].empty_label = "Select Payment Body"