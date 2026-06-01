from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import OrganiserForm

# Create your views here.
@login_required
def index(request):
    return render(request, 'notebook/index.html')

@login_required
def organisers(request):
    form = OrganiserForm()
    
    return render(request, 'notebook/organisers.html', {'form': form})