from django.urls import path

from . import views

app_name = 'notebook'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("organisers", views.OrganiserCreateListView.as_view(), name="organisers"),
    path("organisers/<int:pk>/", views.OrganiserUpdateView.as_view(), name='organiser_info'),
    path('organisers/<int:pk>/delete/', views.OrganiserDeleteView.as_view(), name='organiser_delete'),
    path("payment_bodies/", views.PaymentBodyCreateListView.as_view(), name='pymt_bodies')
]