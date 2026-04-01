# scheduling/urls.py
from django.urls import path
from . import views

app_name = 'scheduling'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
    path('agendar/', views.AppointmentCreateView.as_view(), name='appointment_create'),
]