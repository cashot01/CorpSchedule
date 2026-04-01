from django.urls import path
from . import views

app_name = 'scheduling'

urlpatterns = [
    path('agendar/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('meus-agendamentos/', views.AppointmentListView.as_view(), name='appointment_list'),
]