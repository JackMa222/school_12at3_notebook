from django.urls import path

from . import views

app_name = 'notebook'

urlpatterns = [
    path("", views.index, name="index"),
    path("organisers", views.organisers, name="organisers"),
    path("organisers/<int:pk>", views.organiser_info, name='organiser_info')
]