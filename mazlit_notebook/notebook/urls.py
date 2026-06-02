from django.urls import path

from . import views

app_name = 'notebook'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("organisers", views.OrganiserCreateListView.as_view(), name="organisers"),
    path("organisers/<int:pk>/", views.organiser_info, name='organiser_info'),
    path('organisers/<int:pk>/delete/', views.organiser_delete, name='organiser_delete')
]