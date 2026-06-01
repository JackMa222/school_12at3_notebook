from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


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
        relate_name='events',
        verbose_name="Role(s)"
    )
    
    organiser = models.ForeignKey(
        Organiser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
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
        relate_name='matches',
        verbose_name="Role(s)"
    )
    payment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Base Match Fee")
    
    competitIon = models.ForeignKey(
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

class MatchOfficial(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='officIals'
    )
    
    name = models.CharField(max_length=255, verbose_name="Official Name")
    roles = models.ManyToManyField(
        Role,
        blank=True,
        relate_name='officials',
        verbose_name="Role(s)"
    )
    
    def __str__(self):
        return f"{self.name} ({self.roles})"
    
class Payment(models.Model):
    STATUS_CHOICES = [
        ('OUTSTANDING_REIMB', 'Reimbursement Outstanding'),
        ('OUTSTANDING', 'Outstanding'),
        ('PAID_REIMB', 'Reimbursement Paid'),
        ('PYMT_INDIV', 'Individual Payments'),
        ('PYMT_NONE', 'No Payment'),
        ('PAID', 'Paid')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
        
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
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
        default='PENDING',
        verbose_name='Payment Status'
    )
    
    @property
    def linked_item(self):
        if self.match and self.event:
            return f"{self.match.title} / {self.event.name}"
        if self.match:
            return self.match
        if self.event:
            return self.event
        return None
    
    def __str__(self):
        parts = []
        
        if self.match:
            parts.append(f"Match: {self.match.title}")
            
        if self.event:
            parts.append(f"Event: {self.event.name}")
            
        linked_to = " | ".join(parts) if parts else "Unlinked payment"
        
        return f"${self.amount} ({self.payment_status}) - {linked_to}"
    