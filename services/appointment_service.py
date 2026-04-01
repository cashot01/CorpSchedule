from django.core.exceptions import ValidationError
from django.utils import timezone
from scheduling.models import Appointment
from accounts.models import Professional
from datetime import timedelta

class AppointmentService:
    """
    Classe de Serviço para gerenciar a lógica de criação de agendamentos.
    Princípio: Single Responsibility (Responsabilidade Única).
    """

    def __init__(self, professional: Professional, client, service, scheduled_at: timezone.datetime):
        self.professional = professional
        self.client = client
        self.service = service
        self.scheduled_at = scheduled_at

    def validate_time_slot(self) -> bool:
        """Verifica se o horário está livre."""
        # Calcula o fim do agendamento baseado na duração do serviço
        end_time = self.scheduled_at + timedelta(minutes=self.service.duration_minutes)
        
        # Verifica sobreposição
        conflict = Appointment.objects.filter(
            professional=self.professional,
            status__in=['pending', 'confirmed'],
            scheduled_at__lt=end_time,
            scheduled_at__gte=self.scheduled_at
        ).exists()
        
        if conflict:
            raise ValidationError("Horário indisponível para este profissional.")
        return True

    def validate_business_hours(self) -> bool:
        """Verifica se é horário comercial (ex: 08h às 18h)."""
        hour = self.scheduled_at.hour
        if hour < 8 or hour >= 18:
            raise ValidationError("Agendamentos apenas entre 08h e 18h.")
        return True

    def create_appointment(self) -> Appointment:
        """Método principal que orquestra a criação."""
        self.validate_business_hours()
        self.validate_time_slot()
        
        appointment = Appointment.objects.create(
            professional=self.professional,
            client=self.client,
            service=self.service,
            scheduled_at=self.scheduled_at,
            status='pending'
        )
        # Aqui poderia disparar um signal para enviar email
        return appointment