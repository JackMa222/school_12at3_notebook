from django.urls import path

from . import views

app_name = 'notebook'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("organisers/", views.OrganiserCreateListView.as_view(), name="organisers"),
    path("organisers/<int:pk>/", views.OrganiserUpdateView.as_view(), name='organiser_info'),
    path('organisers/<int:pk>/delete/', views.OrganiserDeleteView.as_view(), name='organiser_delete'),
    path("payment_bodies/", views.PaymentBodyCreateListView.as_view(), name='pymt_bodies'),
    path("payment_bodies/<int:pk>/", views.PaymentBodyUpdateView.as_view(), name='pymt_bodies_info'),
    path("payment_bodies/<int:pk>/delete/", views.PaymentBodyDeleteView.as_view(), name='pymt_bodies_delete'),
    path("payments/", views.PaymentListView.as_view(), name="payments"),
    path("payments/new/", views.PaymentCreateView.as_view(), name="payment_create"),
    path("payments/<int:pk>/", views.PaymentUpdateView.as_view(), name="payment_edit"),
    path("payments/<int:pk>/delete", views.PaymentDeleteView.as_view(), name="payment_delete"),
    path("events/", views.EventListView.as_view(), name="events"),
    path("events/new/", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/", views.EventUpdateView.as_view(), name="event_edit"),
    path("events/<int:pk>/delete", views.EventDeleteView.as_view(), name="event_delete"),
    path("matches/", views.IndexView.as_view(), name="matches"),
    path("matches/new/", views.MatchCreateView.as_view(), name="match_create"),
]