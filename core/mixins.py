from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(LoginRequiredMixin):
    """
    Mixin genérico para verificar tipo de usuário.
    """
    required_role = None  # Deve ser sobrescrito ('client' ou 'professional')

    def dispatch(self, request, *args, **kwargs):
        if self.required_role == 'professional':
            if not hasattr(request.user, 'professional'):
                raise PermissionDenied("Acesso restrito a profissionais.")
        elif self.required_role == 'client':
            if not hasattr(request.user, 'client'):
                raise PermissionDenied("Acesso restrito a clientes.")
        return super().dispatch(request, *args, **kwargs)