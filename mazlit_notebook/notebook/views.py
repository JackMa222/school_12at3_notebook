from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from .forms import OrganiserForm, PaymentBodyForm, PaymentForm, EventForm
from .models import Organiser, PaymentBody, Payment, Event

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
    
class PaymentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'notebook/payment_form.html'
    success_url = reverse_lazy('notebook:payments')
    success_message = "Payment entry successfully updated!"
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class PaymentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Payment
    success_url = reverse_lazy('notebook:payments')
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def get_success_message(self, cleaned_data):
        return f"Payment '{self.object.name}' was successfully deleted."
    
class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'notebook/payments.html'
    context_object_name = 'payments'
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_payments = self.get_queryset()
        
        outstanding = user_payments.filter(payment_status='OUTSTANDING').aggregate(total=Sum('amount'))['total'] or 0.00
        reimb_outstanding = user_payments.filter(payment_status='OUTSTANDING_REIMB').aggregate(total=Sum('amount'))['total'] or 0.00
        paid = user_payments.filter(payment_status__in=['PAID', 'PAID_REIMB']).aggregate(total=Sum('amount'))['total'] or 0.00
        
        context['stats'] = {
            'outstanding': outstanding,
            'reimb_outstanding': reimb_outstanding,
            'paid': paid,
            'total_count': user_payments.count()
        }
        rows = []
        
        for payment in user_payments:
            detail_url = reverse("notebook:payment_edit", kwargs={'pk': payment.pk})
            escaped_name = escape(payment.name)
            name_link = f'<a href="{detail_url}" class="link link-primary font-medium hover:underline">{escaped_name}</a>'
            
            status_mapping = {
                'PAID': '<span class="badge badge-success text-white">Paid</span>',
                'PAID_REIMB': '<span class="badge badge-success text-white">Reimbursement Paid</span>',
                'OUTSTANDING': '<span class="badge badge-error text-white">Outstanding</span>',
                'OUTSTANDING_REIMB': '<span class="badge badge-warning text-warning-content">Reimbursement Outstanding</span>',
                'PYMT_INDIV': '<span class="badge badge-info text-white">Individual Payments</span>',
                'PYMT_NONE': '<span class="badge badge-ghost">No Payment</span>'
            }
            
            stauts_badge = status_mapping.get(payment.payment_status, f'<span class="badge">{payment.payment_status}</span>')
            linked_ref = escape(payment.linked_item) if payment.linked_item else '<span class="text-base-content/30">-</span>'
            payment_body = escape(payment.payment_body.name) if payment.payment_body else '<span class="text-base-content/30">-</span>'
            
            rows.append([
                name_link,
                linked_ref,
                payment_body,
                f"${payment.amount}",
                stauts_badge
            ])
            
        context['table_headers'] = ["Description", "Linked To", "Payer", "Amount", "Status"]
        context['table_rows'] = rows
        return context
    
class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'notebook/event_form.html'
    success_url = reverse_lazy('notebook:events')
    success_message = "Event successfully recorded!"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EventUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'notebook/event_form.html'
    success_url = reverse_lazy('notebook:events')
    success_message = "Event successfully updated!"
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('notebook:events')
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
    
    def get_success_message(self, cleaned_data):
        return f"Event '{self.object.name}' was successfully deleted."