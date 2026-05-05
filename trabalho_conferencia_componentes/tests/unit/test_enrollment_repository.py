import pytest
from src.enrollment_repository import EnrollmentRepository


def test_create_enrollment_registers_active_enrollment():
    repo = EnrollmentRepository()
    repo.create_enrollment(10, 1)
    assert repo.has_active_enrollment(1) is True


def test_count_active_enrollments_counts_only_participant_enrollments():
    repo = EnrollmentRepository()
    repo.create_enrollment(10, 1)
    repo.create_enrollment(10, 2)
    repo.create_enrollment(40, 3)
    assert repo.count_active_enrollments(10) == 2


def test_is_workshop_with_participant_returns_true_for_matching_enrollment():
    repo = EnrollmentRepository()
    repo.create_enrollment(10, 1)
    assert repo.is_workshop_with_participant(10, 1) is True


def test_cancel_enrollment_removes_active_enrollment():
    repo = EnrollmentRepository()
    repo.create_enrollment(10, 1)
    repo.cancel_enrollment(10, 1)
    assert repo.has_active_enrollment(1) is False


def test_cancel_enrollment_raises_for_unknown_enrollment():
    repo = EnrollmentRepository()
    with pytest.raises(ValueError, match="Active enrollment not found"):
        repo.cancel_enrollment(10, 1)
