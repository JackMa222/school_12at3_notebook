from django.contrib import admin
from .models import PaymentBody, Organiser, Event, Match, MatchOfficial, Payment, Role

# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'starting_date', 'ending_date', 'location', 'organiser']
    filter_horizontal = ['roles']
    search_fields = ['names', 'location']
    
@admin.register(Match)
class MatchAdmin(admin.modelAdmin):
    list_display = ['title', 'date_time', 'venue', 'grade', 'payment_fee']
    filter_horizontal = ['roles']
    search_fields = ['title', 'venue', 'grade']
    
@admin.register(MatchOfficial)
class MatchOfficialAdmin(admin.ModelAdmin):
    list_display = ['name', 'match']
    filter_horizontal = ['roles']
    search_fields = ['name']
    
admin.site.register(PaymentBody)
admin.site.register(Organiser)
admin.site.register(Payment)