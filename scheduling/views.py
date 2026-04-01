# scheduling/views.py
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from services.appointment_service import AppointmentService
from .models import Appointment, Service
from accounts.models import Client, Professional

class RoleRequiredMixin(LoginRequiredMixin):
    """Mixin para verificar tipo de usuário"""
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if self.required_role == 'professional':
            if not hasattr(request.user, 'professional'):
                raise PermissionDenied("Acesso restrito a profissionais.")
        elif self.required_role == 'client':
            if not hasattr(request.user, 'client'):
                raise PermissionDenied("Acesso restrito a clientes.")
        return super().dispatch(request, *args, **kwargs)

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
        # Determinar profissional e cliente
        if hasattr(self.request.user, 'client'):
            client = self.request.user.client
            professional = Professional.objects.first()  # Simplificado para demo
        elif hasattr(self.request.user, 'professional'):
            professional = self.request.user.professional
            client = Client.objects.first()  # Simplificado para demo
        else:
            form.add_error(None, "Usuário sem perfil válido")
            return self.form_invalid(form)

        service_layer = AppointmentService(
            professional=professional,
            client=client,
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
        if hasattr(self.request.user, 'client'):
            return Appointment.objects.filter(client=self.request.user.client)
        elif hasattr(self.request.user, 'professional'):
            return Appointment.objects.filter(professional=self.request.user.professional)
        return Appointment.objects.none()