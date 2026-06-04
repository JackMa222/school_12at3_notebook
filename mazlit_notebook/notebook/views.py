from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from .forms import OrganiserForm, PaymentBodyForm, PaymentForm
from .models import Organiser, PaymentBody, Payment

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
    
class PaymentBodyCreateListView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PaymentBody
    form_class = PaymentBodyForm
    template_name = 'notebook/pymt_body.html'
    success_url = reverse_lazy('notebook:pymt_bodies')
    success_message = f"Payment body '%(name)s' created successfully"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        payment_bodies = PaymentBody.objects.filter(user=self.request.user)
        
        rows = []
        for payment_body in payment_bodies:
            detail_url = reverse("notebook:pymt_bodies_info", kwargs={'pk': payment_body.pk})
            escaped_name = escape(payment_body.name)
            name_link = f'<a href="{detail_url}" class="link link-primary font-medium hover:underline">{escaped_name}</a>'
            rows.append([name_link])
            
        context['table_headers'] = ["Name"]
        context['table_rows'] = rows
        return context
    
class PaymentBodyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PaymentBody
    form_class = PaymentBodyForm
    template_name = 'notebook/pymt_body_info.html'
    success_message = "Payment Body '%(name)s' updated successfully"
    
    def get_queryset(self):
        return PaymentBody.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse("notebook:pymt_bodies_info", kwargs={'pk': self.object.pk})
    
class PaymentBodyDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PaymentBody
    success_url = reverse_lazy('notebook:pymt_bodies')
    
    def get_queryset(self):
        return PaymentBody.objects.filter(user=self.request.user)
    
    def get_success_message(self, cleaned_data):
        return f"Payment Body '{self.object.name}' was successfully deleted."
    
class PaymentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'notebook/payment_form.html'
    success_url = reverse_lazy('notebook:payments')
    success_message = "Payment entry successfully recorded!"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)