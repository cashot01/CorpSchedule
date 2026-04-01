# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client, Professional

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuração do Admin para o modelo base User.
    Estende o UserAdmin padrão do Django.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissões', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Admin específico para Clientes.
    """
    list_display = ('username', 'email', 'get_appointments_count', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('created_at',)
    
    def get_appointments_count(self, obj):
        return obj.appointments.count()
    get_appointments_count.short_description = 'Agendamentos'

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    """
    Admin específico para Profissionais.
    """
    list_display = ('username', 'email', 'is_verified', 'get_appointments_count', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('username', 'email', 'bio')
    
    def get_appointments_count(self, obj):
        return obj.appointments.count()
    get_appointments_count.short_description = 'Agendamentos'