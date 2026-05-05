class EnrollmentRepository:
    def __init__(self):
        self._active_enrollments = []

    def create_enrollment(self, participant_id: int, workshop_id: int) -> None:
        self._active_enrollments.append({"participant_id": participant_id, "workshop_id": workshop_id})

    def has_active_enrollment(self, workshop_id: int) -> bool:
        return any(
            enrollment["workshop_id"] == workshop_id
            for enrollment in self._active_enrollments
        )

    def is_workshop_with_participant(self, participant_id: int, workshop_id: int) -> bool:
        return any(
            enrollment["participant_id"] == participant_id and enrollment["workshop_id"] == workshop_id
            for enrollment in self._active_enrollments
        )

    def count_active_enrollments(self, participant_id: int) -> int:
        return sum(
            1 for enrollment in self._active_enrollments
            if enrollment["participant_id"] == participant_id
        )

    def cancel_enrollment(self, participant_id: int, workshop_id: int) -> None:
        for enrollment in list(self._active_enrollments):
            if enrollment["participant_id"] == participant_id and enrollment["workshop_id"] == workshop_id:
                self._active_enrollments.remove(enrollment)
                return
        raise ValueError("Active enrollment not found")
