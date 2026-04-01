from django.db import models
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel
from accounts.models import Professional, Client

class Service(TimeStampedModel):
    name = models.CharField(max_length=100)
    duration_minutes = models.IntegerField(default=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class AppointmentManager(models.Manager):
    """
    Manager Personalizado para encapsular consultas complexas.
    """
    def get_available_slots(self, professional, date):
        # Lógica simplificada para exemplo
        return self.filter(professional=professional, scheduled_at__date=date, status='pending')

class Appointment(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    objects = AppointmentManager()

    def cancel(self):
        """
        Método de instância que encapsula a regra de cancelamento.
        """
        if self.status == 'confirmed':
            raise ValidationError("Agendamentos confirmados não podem ser cancelados por este método.")
        self.status = 'cancelled'
        self.save()

    def __str__(self):
        return f"{self.client.username} com {self.professional.username} às {self.scheduled_at}"