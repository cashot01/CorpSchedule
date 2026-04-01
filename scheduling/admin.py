# scheduling/admin.py
from django.contrib import admin
from .models import Service, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Admin para Serviços oferecidos.
    """
    list_display = ('name', 'duration_minutes', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin para Agendamentos.
    """
    list_display = ('id', 'client', 'professional', 'service', 'scheduled_at', 'status', 'created_at')
    list_filter = ('status', 'scheduled_at', 'created_at')
    search_fields = ('client__username', 'professional__username', 'service__name')
    ordering = ('-scheduled_at',)
    date_hierarchy = 'scheduled_at'
    
    # Campos que podem ser editados diretamente na lista
    list_editable = ('status',)
    
    # Agrupamento visual no formulário
    fieldsets = (
        ('Informações do Agendamento', {
            'fields': ('client', 'professional', 'service', 'scheduled_at')
        }),
        ('Status', {
            'fields': ('status',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Campos automáticos - somente leitura'
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')