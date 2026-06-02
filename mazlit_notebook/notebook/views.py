from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from .forms import OrganiserForm
from .models import Organiser

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'notebook/index.html'

class OrganiserCreateListView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Organiser
    form_class = OrganiserForm
    template_name = 'notebook/organisers.html'
    success_url = reverse_lazy('notebook:organisers')
    success_message = f"Organiser '%(name)s' created successfully"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        organisers = Organiser.objects.filter(user=self.request.user)
        
        rows = []
        for organiser in organisers:
            detail_url = reverse("notebook:organiser_info", kwargs={'pk': organiser.pk})
            escaped_name = escape(organiser.name)
            name_link = f'<a href="{detail_url}" class="link link-primary font-medium hover:underline">{escaped_name}</a>'
            rows.append([name_link])
            
        context['table_headers'] = ["Name"]
        context['table_rows'] = rows
        return context

@login_required
def organiser_info(request, pk):
    organiser = get_object_or_404(Organiser, pk=pk, user=request.user)
    
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
        organiser = get_object_or_404(Organiser, pk=pk, user=request.user)
        deleted_name = organiser.name
        
        organiser.delete()
        
        messages.success(request, f"Organiser '{deleted_name} was successfully deleted.")

    return redirect("notebook:organisers")