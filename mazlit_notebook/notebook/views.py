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

class OrganiserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Organiser
    form_class = OrganiserForm
    template_name = 'notebook/organiser_info.html'
    success_message = "Organiser '%(name)s' updated successfully"
    
    def get_queryset(self):
        return Organiser.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse("notebook:organiser_info", kwargs={'pk': self.object.pk})

class OrganiserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Organiser
    success_url = reverse_lazy('notebook:organisers')
    
    def get_queryset(self):
        return Organiser.objects.filter(user=self.request.user)
    
    def get_success_message(self, cleaned_data):
        return f"Organisers '{self.object.name}' was successfully deleted."

@login_required
def organiser_delete(request, pk):
    if request.method == 'POST':
        organiser = get_object_or_404(Organiser, pk=pk, user=request.user)
        deleted_name = organiser.name
        
        organiser.delete()
        
        messages.success(request, f"Organiser '{deleted_name} was successfully deleted.")

    return redirect("notebook:organisers")