from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from core.mixins import RoleRequiredMixin
from services.appointment_service import AppointmentService
from .models import Appointment, Service

User = get_user_model()

class AppointmentCreateView(RoleRequiredMixin, CreateView):
    model = Appointment
    template_name = 'scheduling/appointment_form.html'
    fields = ['service', 'scheduled_at']
    success_url = reverse_lazy('scheduling:appointment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

    def form_valid(self, form):
        # Instancia o Serviço de Negócio
        service_layer = AppointmentService(
            professional=self.request.user.professional, # Ou lógica para escolher profissional
            client=self.request.user.client,
            service=form.instance.service,
            scheduled_at=form.instance.scheduled_at
        )
        
        try:
            service_layer.create_appointment()
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

class AppointmentListView(RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'scheduling/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Polimorfismo: Client vê os seus, Professional vê os dele
        if hasattr(self.request.user, 'client'):
            return Appointment.objects.filter(client=self.request.user.client)
        elif hasattr(self.request.user, 'professional'):
            return Appointment.objects.filter(professional=self.request.user.professional)
        return Appointment.objects.none()