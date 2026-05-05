from src.participant_repository import ParticipantRepository


def test_exists_returns_true_for_known_participant():
    repo = ParticipantRepository()
    assert repo.exists(10) is True


def test_exists_returns_false_for_unknown_participant():
    repo = ParticipantRepository()
    assert repo.exists(999) is False


def test_is_blocked_returns_true_when_participant_is_blocked():
    repo = ParticipantRepository()
    assert repo.is_blocked(20) is True


def test_has_paid_fee_returns_false_when_fee_is_not_paid():
    repo = ParticipantRepository()
    assert repo.has_paid_fee(30) is False
