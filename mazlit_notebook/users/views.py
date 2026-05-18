from django.shortcuts import render
from .forms import LoginForm

# Create your views here.
def index(request):
    pass

def login_view(request):
    form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    pass