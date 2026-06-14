from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
# Audit log
from auditlog.registry import auditlog


# Create your models here.
class PaymentBody(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_bodies'
    )
    
    name = models.CharField(max_length=255, verbose_name="Payment Body Name")
    
    class Meta:
        verbose_name_plural = "Payment Bodies"
    
    def __str__(self):
        return self.name
    
class Organiser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organisers'
    ) 
    
    name = models.CharField(max_length=255, verbose_name="Organiser Name")
    
    def __str__(self):
        return self.name
 
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    badge_class = models.CharField(
        max_length=50,
        default="badge-ghost",
        help_text="DaisyUI color class: badge-primary, badge-secondary, badge-info, badge-success, etc."
    )
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    
    name = models.CharField(max_length=255, verbose_name="Event Name")
    starting_date = models.DateField(verbose_name="Starting Date", null=True, blank=True)
    ending_date = models.DateField(verbose_name="Ending Date", null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name="Location", null=True, blank=True)
    roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name='events',
        verbose_name="Role(s)"
    )
    
    organiser = models.ForeignKey(
        Organiser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    
    def clean(self):
        if self.starting_date and self.ending_date:
            if self.ending_date < self.starting_date:
                raise ValidationError(
                    "Ending date cannot be before starting date."
                )
    
    def __str__(self):
        return self.name
    
class Match(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    title = models.CharField(max_length=255, verbose_name="Game/Event Title")
    date_time = models.DateTimeField(verbose_name="Date & Time")
    venue = models.CharField(max_length=255, verbose_name="Venue")
    grade = models.CharField(max_length=100, verbose_name="Grade", help_text="e.g. PL1, U18B1")
    roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name='matches',
        verbose_name="Role(s)"
    )
    payment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Base Match Fee", validators=[MinValueValidator(0.00)])
    
    competition = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='matches'
    )
    
    class Meta:
        verbose_name_plural = "Matches"
        ordering = ['-date_time']
        
    def __str__(self):
        return f"{self.title} ({self.date_time.strftime('%d-%m-%Y')})"

class Person(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='people'
    )
    
    name = models.CharField(max_length=255, verbose_name="Person Name")
    # OPTION to add Email and Phone if needed
    
    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_person_name_per_user'
            )
        ]
        
    def __str__(self):
        return self.name

class MatchOfficial(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='officials'
    )
    
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='match_official_entries',
    )
    roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name='officials',
        verbose_name="Role(s)"
    )
    
    def __str__(self):
        assigned_roles = ", ".join([role.name for role in self.roles.all()])
        role_display = f" [{assigned_roles}]" if assigned_roles else ""
        return f"{self.person.name}{role_display} - Match: {self.match.title}"
    
class Payment(models.Model):
    STATUS_CHOICES = [
        ('OUTSTANDING', 'Outstanding'),
        ('OUTSTANDING_REIMB', 'Reimbursement Outstanding'),
        ('PAID_REIMB', 'Reimbursement Paid'),
        ('PYMT_INDIV', 'Individual Payments'),
        ('PYMT_NONE', 'No Payment'),
        ('PAID', 'Paid')
    ]
    
    name = models.CharField(max_length=255, verbose_name="Payment Name/Description")
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
        
    matches = models.ManyToManyField(
        Match,
        related_name='payments',
        blank=True
    )
    
    events = models.ManyToManyField(
        Event,
        blank=True,
        related_name='payments'
    )
    
    payment_body = models.ForeignKey(
        PaymentBody,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Payment Amount")
    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0],
        verbose_name='Payment Status'
    )
    
    @property
    def linked_item(self):
        match_titles = [match.title for match in self.matches.all()]
        event_names = [event.name for event in self.events.all()]
        
        all_links = match_titles + event_names
        return " / ".join(all_links) if all_links else None
    
    def __str__(self):
        parts = []
        
        if self.id and self.matches.exists():
            match_titles = ", ".join([m.title for m in self.matches.all()])
            parts.append(f"Matches: [{match_titles}]")
            
        if self.id and self.events.exists():
            event_names = ", ".join([e.name for e in self.events.all()])
            parts.append(f"Events: [{event_names}]")
            
        linked_to = " | ".join(parts) if parts else "Unlinked payment"
        
        return f"${self.amount} ({self.payment_status}) - {linked_to}"
    
auditlog.register(Match)
auditlog.register(Payment)
auditlog.register(Event)
auditlog.register(Organiser)