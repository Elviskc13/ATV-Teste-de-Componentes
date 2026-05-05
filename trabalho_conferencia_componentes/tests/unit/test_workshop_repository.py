import pytest
from src.workshop_repository import WorkshopRepository


def test_exists_returns_true_for_existing_workshop():
    repo = WorkshopRepository()
    assert repo.exists(1) is True


def test_is_available_returns_true_for_available_workshop():
    repo = WorkshopRepository()
    assert repo.is_available(1) is True


def test_is_available_returns_false_for_unavailable_workshop():
    repo = WorkshopRepository()
    assert repo.is_available(3) is False


def test_mark_unavailable_changes_workshop_state():
    repo = WorkshopRepository()
    repo.mark_unavailable(1)
    assert repo.is_available(1) is False


def test_mark_available_changes_workshop_state():
    repo = WorkshopRepository()
    repo.mark_available(3)
    assert repo.is_available(3) is True


def test_mark_unavailable_raises_for_unknown_workshop():
    repo = WorkshopRepository()
    with pytest.raises(ValueError, match="Workshop not found"):
        repo.mark_unavailable(999)
