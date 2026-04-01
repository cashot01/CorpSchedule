from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    """
    Modelo base de usuário.
    """
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Client(User):
    """
    Perfil de Cliente. Herda de User.
    """
    # Pode adicionar campos específicos se necessário
    pass

class Professional(User):
    """
    Perfil de Profissional. Herda de User.
    """
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_full_name()} ({'Verificado' if self.is_verified else 'Pendente'})"