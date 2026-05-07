import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.conference_service import ConferenceService
from src.workshop_repository import WorkshopRepository
from src.participant_repository import ParticipantRepository
from src.enrollment_repository import EnrollmentRepository
from src.waitlist_repository import WaitlistRepository

def criar_sistema():
    workshop_repo = WorkshopRepository()
    participant_repo = ParticipantRepository()
    enrollment_repo = EnrollmentRepository()
    waitlist_repo = WaitlistRepository()

    service = ConferenceService(
        workshop_repo,
        participant_repo,
        enrollment_repo,
        waitlist_repo
    )

    return (
        service,
        workshop_repo,
        participant_repo,
        enrollment_repo,
        waitlist_repo
    )


def test_inscricao_com_sucesso():

    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(10, 1)

    assert result is True
    assert enrollment_repo.is_workshop_with_participant(10, 1)


def test_participante_bloqueado():

    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(20, 1)

    assert result is False


def test_participante_nao_pagou():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(30, 1)

    assert result is False

def test_entrada_na_fila():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.join_waitlist(10, 3)

    assert result is True


def test_nao_entra_na_fila_se_disponivel():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.join_waitlist(10, 1)

    assert result is False


def test_respeita_ordem_da_fila():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.join_waitlist(10, 3)  
    service.join_waitlist(40, 3)  

    result = service.enroll_in_workshop(40, 3)

    assert result is False

def test_primeiro_da_fila_consegue_entrar():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.join_waitlist(10, 3)

    workshop_repo.mark_available(3)

    result = service.enroll_in_workshop(10, 3)

    assert result is True


def test_cancelamento_com_fila_nao_libera_vaga():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.enroll_in_workshop(10, 1)

    service.join_waitlist(40, 1)

    service.cancel_workshop_enrollment(10, 1)

    assert not workshop_repo.is_available(1)


def test_cancelamento_sem_fila_libera_vaga():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.enroll_in_workshop(10, 1)

    service.cancel_workshop_enrollment(10, 1)

    assert workshop_repo.is_available(1)


def test_limite_de_inscricoes():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.enroll_in_workshop(10, 1)
    service.enroll_in_workshop(10, 2)

    workshop_repo.mark_available(3)

    result = service.enroll_in_workshop(10, 3)

    assert result is False


def test_workshop_inexistente():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(10, 999)

    assert result is False


def test_participante_inexistente():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    result = service.enroll_in_workshop(999, 1)

    assert result is False


def test_fila_duplicada():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.join_waitlist(10, 3)

    result = service.join_waitlist(10, 3)

    assert result is False
    

def test_inscricao_remove_participante_da_fila():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.join_waitlist(10, 3)

    workshop_repo.mark_available(3)

    result = service.enroll_in_workshop(10, 3)

    assert result is True
    assert not waitlist_repo.has_waitlist(10, 3)

def test_fluxo_completo_inscricao_fila_cancelamento():
    
    service, workshop_repo, participant_repo, enrollment_repo, waitlist_repo = criar_sistema()

    service.enroll_in_workshop(10, 1)

    service.join_waitlist(40, 1)

    service.cancel_workshop_enrollment(10, 1)

    workshop_repo.mark_available(1)

    result = service.enroll_in_workshop(40, 1)

    assert result is True