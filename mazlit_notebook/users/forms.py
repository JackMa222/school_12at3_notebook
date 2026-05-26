from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': '••••••••'
    }))
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': 'name@example.com'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Choose a username'
        })
        
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Chris'
        })
        
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Kof'
        })
        
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '••••••••'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Confirm your password'
        })
        
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"