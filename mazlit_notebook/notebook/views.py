from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
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
            organiser_name = form.cleaned_data.get('name')
            
            new_organiser = Organiser.objects.create(
                name=organiser_name,
                user=request.user
            )
            
            messages.success(request, f"Organiser '{organiser_name}' created successfully")
            return redirect("notebook:organisers")
    
    form = OrganiserForm()
    organisers = Organiser.objects.all()
    
    headers = ["Name"]
    
    rows = []
    
    for organiser in organisers:
        detail_url = reverse("notebook:organiser_info", kwargs={'pk': organiser.pk})
        
        escaped_name = escape(organiser.name)
        
        name_link = f'<a href="{detail_url}" class="link link-primary font-medium hover:underline">{escaped_name}</a>'
        
        rows.append([name_link])
    
    print(rows)
    
    context = {
        'form': form,
        'table_headers': headers,
        'table_rows': rows
    }
    
    return render(request, 'notebook/organisers.html', context)

@login_required
def organiser_info(request, pk):
    organiser = get_object_or_404(Organiser, pk=pk)
    
    if request.method == "POST":
        form = OrganiserForm(request.POST, instance=organiser)
        if form.is_valid():
            form.save()
            messages.success(request, f"Organiser '{organiser.name} updated successfully")
            return redirect("notebook:organiser_info", pk=organiser.pk)
    else:
        form = OrganiserForm(instance=organiser) 
    
    context = {
        'organiser': organiser,
        'form': form
    }
    
    return render(request, 'notebook/organiser_info.html', context)

@login_required
def organiser_delete(request, pk):
    if request.method == 'POST':
        organiser = get_object_or_404(Organiser, pk=pk)
        deleted_name = organiser.name
        
        organiser.delete()
        
        messages.success(request, f"Organiser '{deleted_name} was successfully deleted.")

    return redirect("notebook:organisers")