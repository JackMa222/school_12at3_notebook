from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrganiserForm
from .models import Organiser

# Create your views here.
@login_required
def index(request):
    return render(request, 'notebook/index.html')

@login_required
def organisers(request):
    if request.method == "POST":
        form = OrganiserForm(request.POST)
        
        if form.is_valid():
            organiser_name = form.cleaned_data.get('organiser_name')
            
            new_organiser = Organiser.objects.create(
                name=organiser_name,
                user=request.user
            )
            
            messages.success(request, f"Organiser '{organiser_name}' created successfully")
            return redirect("notebook:organisers")
    
    form = OrganiserForm()
    
    return render(request, 'notebook/organisers.html', {'form': form})