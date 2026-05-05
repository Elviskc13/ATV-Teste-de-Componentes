class WaitlistRepository:
    def __init__(self):
        self._waitlist = []

    def add_to_waitlist(self, participant_id: int, workshop_id: int) -> None:
        self._waitlist.append({"participant_id": participant_id, "workshop_id": workshop_id})

    def has_waitlist(self, participant_id: int, workshop_id: int) -> bool:
        return any(
            entry["participant_id"] == participant_id and entry["workshop_id"] == workshop_id
            for entry in self._waitlist
        )

    def has_any_waitlist(self, workshop_id: int) -> bool:
        return any(entry["workshop_id"] == workshop_id for entry in self._waitlist)

    def next_participant(self, workshop_id: int):
        for entry in self._waitlist:
            if entry["workshop_id"] == workshop_id:
                return entry["participant_id"]
        return None

    def remove_from_waitlist(self, participant_id: int, workshop_id: int) -> None:
        for entry in list(self._waitlist):
            if entry["participant_id"] == participant_id and entry["workshop_id"] == workshop_id:
                self._waitlist.remove(entry)
                return
        raise ValueError("Waitlist entry not found")
