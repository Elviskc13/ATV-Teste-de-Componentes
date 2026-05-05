import pytest
from unittest.mock import Mock
from src.conference_service import ConferenceService


def make_service():
    workshop_repository = Mock()
    participant_repository = Mock()
    enrollment_repository = Mock()
    waitlist_repository = Mock()
    service = ConferenceService(
        workshop_repository,
        participant_repository,
        enrollment_repository,
        waitlist_repository,
    )
    return service, workshop_repository, participant_repository, enrollment_repository, waitlist_repository


def test_enroll_in_workshop_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Participant ID and workshop ID are required"):
        service.enroll_in_workshop(None, 1)


def test_enroll_in_workshop_returns_false_when_participant_does_not_exist():
    service, _, participant_repository, _, _ = make_service()
    participant_repository.exists.return_value = False
    assert service.enroll_in_workshop(999, 1) is False


def test_enroll_in_workshop_creates_enrollment_when_all_rules_are_satisfied():
    service, workshop_repository, participant_repository, enrollment_repository, waitlist_repository = make_service()

    participant_repository.exists.return_value = True
    workshop_repository.exists.return_value = True
    participant_repository.is_blocked.return_value = False
    participant_repository.has_paid_fee.return_value = True
    workshop_repository.is_available.return_value = True
    enrollment_repository.count_active_enrollments.return_value = 0
    waitlist_repository.next_participant.return_value = None
    waitlist_repository.has_waitlist.return_value = False

    result = service.enroll_in_workshop(10, 1)

    assert result is True
    workshop_repository.mark_unavailable.assert_called_once_with(1)
    enrollment_repository.create_enrollment.assert_called_once_with(10, 1)


def test_cancel_workshop_enrollment_returns_false_when_enrollment_does_not_exist():
    service, _, _, enrollment_repository, _ = make_service()
    enrollment_repository.is_workshop_with_participant.return_value = False
    assert service.cancel_workshop_enrollment(10, 1) is False


def test_join_waitlist_adds_participant_when_rules_are_satisfied():
    service, workshop_repository, participant_repository, enrollment_repository, waitlist_repository = make_service()

    participant_repository.exists.return_value = True
    workshop_repository.exists.return_value = True
    participant_repository.is_blocked.return_value = False
    participant_repository.has_paid_fee.return_value = True
    workshop_repository.is_available.return_value = False
    waitlist_repository.has_waitlist.return_value = False
    enrollment_repository.is_workshop_with_participant.return_value = False

    result = service.join_waitlist(10, 1)

    assert result is True
    waitlist_repository.add_to_waitlist.assert_called_once_with(10, 1)


def test_join_waitlist_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Participant ID and workshop ID are required"):
        service.join_waitlist(None, 1)
