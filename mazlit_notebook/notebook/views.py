from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.utils import timezone, formats
from django.template import Template, Context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from .forms import OrganiserForm, PaymentBodyForm, PaymentForm, EventForm, MatchForm
from .models import Organiser, PaymentBody, Payment, Event, Match

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'notebook/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['matches'] = (Match.objects.filter(user=user)
                              .select_related('competition')
                              .prefetch_related('roles')
                              .order_by('-date_time'))
        
        context['events'] = (Event.objects.filter(user=user, ending_date__gte=timezone.now().date())
                             .order_by('starting_date')[:3])
        
        context['latest_payments'] = (Payment.objects.filter(user=user, payment_status='PAID')[:3])
        
        outstanding = (Payment.objects.filter(user=user, payment_status='OUTSTANDING')
                       .aggregate(total=Sum('amount'))['total'])
        
        context['outstanding_balance'] = outstanding or 0.00
        
        return context

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
            
            status_badge = status_mapping.get(payment.payment_status, f'<span class="badge">{payment.payment_status}</span>')
            linked_ref = escape(payment.linked_item) if payment.linked_item else '<span class="text-base-content/30">-</span>'
            payment_body = escape(payment.payment_body.name) if payment.payment_body else '<span class="text-base-content/30">-</span>'
            
            rows.append([
                name_link,
                linked_ref,
                payment_body,
                f"${payment.amount}",
                status_badge
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
    
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'notebook/events.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        return (Event.objects.filter(user=self.request.user)
                .select_related('organiser')
                .prefetch_related('roles'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_events = self.get_queryset()
            
        upcoming_count = user_events.filter(ending_date__gte=timezone.now().date()).count()
        
        context['stats'] = {
            'total_count': user_events.count(),
            'upcoming_count': upcoming_count
        }
        rows = []
        
        for event in user_events:
            detail_url = reverse("notebook:event_edit", kwargs={'pk': event.pk})
            escaped_name = escape(event)
            name_link = f'<a href="{detail_url}" class="link link-primary font-medium hover:underline">{escaped_name}</a>'
            escaped_start = escape(event.starting_date) if event.starting_date else ""
            escaped_end = escape(event.ending_date) if event.ending_date else ""
            escaped_location = escape(event.location) if event.location else ""
            escaped_organiser = escape(event.organiser.name) if event.organiser else ""
            
            role_badges = []
            for role in event.roles.all():
                escaped_role_name = escape(role.name)
                css_class = role.badge_class if role.badge_class else "badge-ghost"
                
                badge_html = f'<span class="badge {css_class} text-xs font-semibold mr-1">{escaped_role_name}</span>'
                role_badges.append(badge_html)
                
            role_badges = "".join(role_badges) if role_badges else '-'
            
            rows.append([
                name_link,
                escaped_start,
                escaped_end,
                escaped_location,
                role_badges,
                escaped_organiser
            ])
            
        context['table_headers'] = ["Name", "Start", "End", "Location", "Roles", "Organiser"]
        context['table_rows'] = rows
        return context
    
class MatchCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'notebook/match_form.html'
    success_url = reverse_lazy('notebook:matches')
    success_message = "Match successfully recorded!"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class MatchUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Match
    form_class = MatchForm
    template_name = 'notebook/match_form.html'
    success_url = reverse_lazy('notebook:matches')
    success_message = "Match successfully updated!"
    
    def get_queryset(self):
        return Match.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MatchDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Match
    success_url = reverse_lazy('notebook:matches')
    
    def get_queryset(self):
        return Match.objects.filter(user=self.request.user)
    
    def get_success_message(self, cleaned_data):
        return f"Match '{self.object.title}' was successfully deleted."

class MatchListView(LoginRequiredMixin, ListView):
    model = Match
    template_name = 'notebook/matches.html'
    context_object_name = 'matches'
    
    def get_queryset(self):
        return (Match.objects.filter(user=self.request.user)
                .select_related('competition')
                .prefetch_related('roles'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_matches = self.get_queryset()
            
        upcoming_count = user_matches.filter(date_time__gte=timezone.now().date()).count()
        
        context['stats'] = {
            'total_count': user_matches.count(),
            'upcoming_count': upcoming_count
        }
        rows = []
        
        for match in user_matches:
            detail_url = reverse("notebook:match_edit", kwargs={'pk': match.pk})
            escaped_name = escape(match.title)
            name_link = f'<a href="{detail_url}" class="link link-primary font-medium hover:underline">{escaped_name}</a>'
            t = Template('{% load tz %}{{ dt|localtime|date:"SHORT_DATETIME_FORMAT" }}')
            clean_date = t.render(Context({'dt': match.date_time}))
            date_html = f'<span class="whitespace-nowrap">{clean_date}</span>'
            escaped_venue = escape(match.venue) if match.venue else ""
            escaped_grade = escape(match.grade) if match.grade else ""
            escaped_fee = f"${escape(match.payment_fee)}" if match.payment_fee else ""
            escaped_competition = escape(match.competition) if match.competition else ""
            
            role_badges = []
            for role in match.roles.all():
                escaped_role_name = escape(role.name)
                css_class = role.badge_class if role.badge_class else "badge-ghost"
                
                badge_html = f'<span class="badge {css_class} text-xs font-semibold mr-1">{escaped_role_name}</span>'
                role_badges.append(badge_html)
                
            role_badges = "".join(role_badges) if role_badges else '-'
            
            rows.append([
                name_link,
                date_html,
                escaped_venue,
                escaped_grade,
                escaped_fee,
                role_badges,
                escaped_competition
            ])
            
        context['table_headers'] = ["Name", "Date / Time", "Venue", "Grade", "Fee", "Roles", "Competition"]
        context['table_rows'] = rows
        return context