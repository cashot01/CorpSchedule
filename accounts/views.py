# accounts/views.py
from django.contrib.auth.views import LoginView
from django.contrib import messages

class CustomLoginView(LoginView):
    """
    View personalizada de login com mensagem de boas-vindas.
    """
    def form_valid(self, form):
        # 👉 CORREÇÃO: Pegar o usuário do formulário, não do request
        # O form.get_user() retorna o usuário autenticado
        user = form.get_user()
        
        # Criar mensagem de boas-vindas
        user_name = user.first_name or user.username
        messages.success(self.request, f'Bem-vindo, {user_name}! 🎉')
        
        # Chamar o método pai para concluir o login e redirecionar
        return super().form_valid(form)