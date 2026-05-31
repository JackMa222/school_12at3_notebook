from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm

# Create your views here.
@login_required
def index(request):
    return render(request, 'users/index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:index')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}")
                return redirect("users:index")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
 
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:index')
    
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            messages.success(request, f"Account created successfully.")
            return redirect('users:index')
        else:
            messages.error(request, "Please correct the following errors.")
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    
    return redirect('users:login')