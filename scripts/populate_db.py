# scripts/populate_db.py
import os
import sys
import django
from datetime import datetime, timedelta

# =============================================================================
# 👈 IMPORTANTE: Adicionar o projeto ao Python PATH
# =============================================================================
# Isso permite que o script encontre o módulo 'config'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Sobe um nível para a raiz do projeto
sys.path.insert(0, project_root)

# Agora configuramos o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# =============================================================================
# Imports dos modelos (só funcionam após o django.setup())
# =============================================================================
from accounts.models import Client, Professional
from scheduling.models import Service, Appointment

def populate():
    print("🚀 Iniciando população do banco de dados...\n")
    
    # Limpar dados existentes (opcional - cuidado em produção!)
    Appointment.objects.all().delete()
    Service.objects.all().delete()
    Client.objects.all().delete()
    Professional.objects.all().delete()
    print("🧹 Dados antigos limpos.\n")
    
    # Criar profissional
    prof = Professional.objects.create_user(
        username='prof_teste',
        password='senha123',
        first_name='Carlos',
        last_name='Consultor',
        email='carlos@teste.com',
        is_verified=True
    )
    print(f"✅ Professional criado: {prof.username}")
    
    # Criar cliente
    client = Client.objects.create_user(
        username='client_teste',
        password='senha123',
        first_name='Ana',
        last_name='Cliente',
        email='ana@teste.com'
    )
    print(f"✅ Client criado: {client.username}")
    
    # Criar serviços
    service1 = Service.objects.create(
        name='Consultoria Individual',
        duration_minutes=60,
        price=150.00
    )
    print(f"✅ Service criado: {service1.name}")
    
    service2 = Service.objects.create(
        name='Mentoria Executiva',
        duration_minutes=90,
        price=300.00
    )
    print(f"✅ Service criado: {service2.name}")
    
    # Criar agendamento (horário comercial: entre 08h e 18h)
    appointment = Appointment.objects.create(
        client=client,
        professional=prof,
        service=service1,
        scheduled_at=datetime.now() + timedelta(days=1, hours=2),
        status='pending'
    )
    print(f"✅ Appointment criado: ID {appointment.id}")
    
    print("\n" + "="*50)
    print("🎉 Banco de dados populado com sucesso!")
    print("="*50)
    print("\n📋 Dados de teste:")
    print(f"   Professional: {prof.username} / senha: senha123")
    print(f"   Client: {client.username} / senha: senha123")
    print(f"   Services: {Service.objects.count()} cadastrados")
    print(f"   Appointments: {Appointment.objects.count()} agendados")
    print("\n💡 Acesse o admin: http://127.0.0.1:8000/admin/")
    print("   Login com o superusuário que você criou anteriormente.\n")

if __name__ == '__main__':
    try:
        populate()
    except Exception as e:
        print(f"\n❌ Erro ao popular banco de dados: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)