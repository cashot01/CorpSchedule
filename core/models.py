from django.db import models

class TimeStampedModel(models.Model):
    """
    Classe Abstrata para adicionar created_at e updated_at automaticamente.
    Demonstra o conceito de Herança e Abstração.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Importante: Não cria tabela no banco