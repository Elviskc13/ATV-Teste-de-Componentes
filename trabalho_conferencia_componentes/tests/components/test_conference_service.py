import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Importação das classes do sistema
from src.conference_service import ConferenceService
from src.workshop_repository import WorkshopRepository
from src.participant_repository import ParticipantRepository
from src.enrollment_repository import EnrollmentRepository
from src.waitlist_repository import WaitlistRepository

# Função auxiliar responsável por criar o sistema necessário para os testes
def criar_sistema():

    # Cria os repositórios utilizados pelo serviço
    workshop_repo = WorkshopRepository()
    participant_repo = ParticipantRepository()
    enrollment_repo = EnrollmentRepository()
    waitlist_repo = WaitlistRepository()

    # Cria o serviço principal do sistema
    service = ConferenceService(
        workshop_repo,
        participant_repo,
        enrollment_repo,
        waitlist_repo
    )

    # Retorna o serviço e os repositórios para uso
    return (
        service,
        workshop_repo,
        participant_repo,
        enrollment_repo,
        waitlist_repo
    )

# Testes de inscrição

# Verifica se um participante válido consegue se inscrever
def test_inscricao_com_sucesso():

    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Realiza a inscrição
    result = service.enroll_in_workshop(10, 1)

    # Verifica se a operação retornou sucesso
    assert result is True

    # Verifica se a inscrição foi realmente registrada
    assert enrollment_repo.is_workshop_with_participant(10, 1)

# Verifica se participante bloqueado não consegue se inscrever
def test_participante_bloqueado():

    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(20, 1)

    assert result is False

# Verifica se participante inadimplente não consegue se inscrever
def test_participante_nao_pagou():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(30, 1)

    assert result is False

# Verifica se o sistema impede inscrição em workshop inexistente
def test_workshop_inexistente():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(10, 999)

    assert result is False

# Verifica se participante inexistente não consegue se inscrever
def test_participante_inexistente():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(999, 1)

    assert result is False

# Verifica se o limite máximo de 2 inscrições ativas é respeitado
def test_limite_de_inscricoes():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Realiza duas inscrições válidas
    service.enroll_in_workshop(10, 1)
    service.enroll_in_workshop(10, 2)

    # Libera manualmente o workshop 3
    workshop_repo.mark_available(3)

     # Tenta realizar uma terceira inscrição
    result = service.enroll_in_workshop(10, 3)

    assert result is False

# Testes de fila de espera

# Verifica se participante consegue entrar na fila de espera
def test_entrada_na_fila():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.join_waitlist(10, 3)

    assert result is True

# Verifica se não é possível entrar na fila quando workshop está disponível
def test_nao_entra_na_fila_se_disponivel():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.join_waitlist(10, 1)

    assert result is False

# Verifica se o sistema impede fila duplicada
def test_fila_duplicada():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Primeira entrada na fila
    service.join_waitlist(10, 3)

    # Segunda tentativa da mesma pessoa
    result = service.join_waitlist(10, 3)

    assert result is False

# Verifica se o sistema respeita a ordem da fila de espera
def test_respeita_ordem_da_fila():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Participante 10 entra primeiro
    service.join_waitlist(10, 3)
    # Participante 40 entra depois  
    service.join_waitlist(40, 3)  

    # Participante 40 tenta furar a fila
    result = service.enroll_in_workshop(40, 3)

    assert result is False

# Verifica se o primeiro da fila consegue realizar inscrição
def test_primeiro_da_fila_consegue_entrar():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Participante entra na fila
    service.join_waitlist(10, 3)

    # Workshop é liberado
    workshop_repo.mark_available(3)

    # Participante tenta se inscrever
    result = service.enroll_in_workshop(10, 3)

    assert result is True

# Verifica se a inscrição remove automaticamente o participante da fila
def test_inscricao_remove_participante_da_fila():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Participante entra na fila
    service.join_waitlist(10, 3)

    # Workshop é liberado
    workshop_repo.mark_available(3)

    # Participante realiza inscrição
    result = service.enroll_in_workshop(10, 3)

    assert result is True

    # Verifica se saiu da fila
    assert not waitlist_repo.has_waitlist(10, 3)

# Testes de cancelamento

# Verifica se cancelamento sem fila libera a vaga
def test_cancelamento_sem_fila_libera_vaga():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Participante realiza inscrição
    service.enroll_in_workshop(10, 1)

    # Cancela inscrição
    service.cancel_workshop_enrollment(10, 1)

    # Workshop deve voltar a ficar disponível
    assert workshop_repo.is_available(1)


# Verifica se cancelamento com fila mantém workshop indisponível
def test_cancelamento_com_fila_nao_libera_vaga():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Participante realiza inscrição
    service.enroll_in_workshop(10, 1)

    # Outro participante entra na fila
    service.join_waitlist(40, 1)

     # Cancela inscrição
    service.cancel_workshop_enrollment(10, 1)

    # Workshop deve continuar indisponível
    assert not workshop_repo.is_available(1)

# Teste de fluxo completo

# Verifica fluxo completo envolvendo inscrição, fila e cancelamento
def test_fluxo_completo_inscricao_fila_cancelamento():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    # Participante 10 realiza inscrição
    service.enroll_in_workshop(10, 1)

    # Participante 40 entra na fila
    service.join_waitlist(40, 1)

    # Participante 10 cancela inscrição
    service.cancel_workshop_enrollment(10, 1)

    # Workshop é liberado manualmente
    workshop_repo.mark_available(1)

    # Participante 40 tenta se inscrever
    result = service.enroll_in_workshop(40, 1)

    assert result is True