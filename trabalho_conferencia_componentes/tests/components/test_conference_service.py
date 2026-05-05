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