import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.conference_service import ConferenceService
from src.workshop_repository import WorkshopRepository
from src.participant_repository import ParticipantRepository
from src.enrollment_repository import EnrollmentRepository
from src.waitlist_repository import WaitlistRepository


def test_inscricao_com_sucesso():
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

    result = service.enroll_in_workshop(10, 1)

    assert result is True
    assert enrollment_repo.is_workshop_with_participant(10, 1)

def test_participante_bloqueado():
    service = ConferenceService(
        WorkshopRepository(),
        ParticipantRepository(),
        EnrollmentRepository(),
        WaitlistRepository()
    )

    result = service.enroll_in_workshop(20, 1)

    assert result is False


def test_participante_nao_pagou():
    service = ConferenceService(
        WorkshopRepository(),
        ParticipantRepository(),
        EnrollmentRepository(),
        WaitlistRepository()
    )

    result = service.enroll_in_workshop(30, 1)

    assert result is False

def test_entrada_na_fila():
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

    result = service.join_waitlist(10, 3)

    assert result is True


def test_nao_entra_na_fila_se_disponivel():
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

    result = service.join_waitlist(10, 1)

    assert result is False

def test_entrada_na_fila():
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

    result = service.join_waitlist(10, 3)

    assert result is True


def test_nao_entra_na_fila_se_disponivel():
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

    result = service.join_waitlist(10, 1)

def test_respeita_ordem_da_fila():
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

    service.join_waitlist(10, 3)  
    service.join_waitlist(40, 3)  

    result = service.enroll_in_workshop(40, 3)

    assert result is False

def test_primeiro_da_fila_consegue_entrar():
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

    service.join_waitlist(10, 3)

    workshop_repo.mark_available(3)

    result = service.enroll_in_workshop(10, 3)

    assert result is True