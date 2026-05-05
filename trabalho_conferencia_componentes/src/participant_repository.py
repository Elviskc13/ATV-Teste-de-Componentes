class ParticipantRepository:
    def __init__(self):
        self._participants = {
            10: {"name": "Ana", "blocked": False, "fee_paid": True},
            20: {"name": "Bruno", "blocked": True, "fee_paid": True},
            30: {"name": "Carla", "blocked": False, "fee_paid": False},
            40: {"name": "Diego", "blocked": False, "fee_paid": True},
        }

    def exists(self, participant_id: int) -> bool:
        return participant_id in self._participants

    def is_blocked(self, participant_id: int) -> bool:
        if participant_id not in self._participants:
            return False
        return self._participants[participant_id]["blocked"]

    def has_paid_fee(self, participant_id: int) -> bool:
        if participant_id not in self._participants:
            return False
        return self._participants[participant_id]["fee_paid"]
