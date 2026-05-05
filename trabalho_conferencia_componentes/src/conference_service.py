class ConferenceService:
    def __init__(self, workshop_repository, participant_repository, enrollment_repository, waitlist_repository):
        self.workshop_repository = workshop_repository
        self.participant_repository = participant_repository
        self.enrollment_repository = enrollment_repository
        self.waitlist_repository = waitlist_repository

    def enroll_in_workshop(self, participant_id: int, workshop_id: int) -> bool:
        if not participant_id or not workshop_id:
            raise ValueError("Participant ID and workshop ID are required")

        if not self.participant_repository.exists(participant_id):
            return False

        if not self.workshop_repository.exists(workshop_id):
            return False

        if self.participant_repository.is_blocked(participant_id):
            return False

        if not self.participant_repository.has_paid_fee(participant_id):
            return False

        if not self.workshop_repository.is_available(workshop_id):
            return False

        if self.enrollment_repository.count_active_enrollments(participant_id) >= 2:
            return False

        next_participant = self.waitlist_repository.next_participant(workshop_id)
        if next_participant is not None and next_participant != participant_id:
            return False

        self.workshop_repository.mark_unavailable(workshop_id)
        self.enrollment_repository.create_enrollment(participant_id, workshop_id)

        if self.waitlist_repository.has_waitlist(participant_id, workshop_id):
            self.waitlist_repository.remove_from_waitlist(participant_id, workshop_id)

        return True

    def cancel_workshop_enrollment(self, participant_id: int, workshop_id: int) -> bool:
        if not participant_id or not workshop_id:
            raise ValueError("Participant ID and workshop ID are required")

        if not self.enrollment_repository.is_workshop_with_participant(participant_id, workshop_id):
            return False

        self.enrollment_repository.cancel_enrollment(participant_id, workshop_id)

        if not self.waitlist_repository.has_any_waitlist(workshop_id):
            self.workshop_repository.mark_available(workshop_id)

        return True

    def join_waitlist(self, participant_id: int, workshop_id: int) -> bool:
        if not participant_id or not workshop_id:
            raise ValueError("Participant ID and workshop ID are required")

        if not self.participant_repository.exists(participant_id):
            return False

        if not self.workshop_repository.exists(workshop_id):
            return False

        if self.participant_repository.is_blocked(participant_id):
            return False

        if not self.participant_repository.has_paid_fee(participant_id):
            return False

        if self.workshop_repository.is_available(workshop_id):
            return False

        if self.waitlist_repository.has_waitlist(participant_id, workshop_id):
            return False

        if self.enrollment_repository.is_workshop_with_participant(participant_id, workshop_id):
            return False

        self.waitlist_repository.add_to_waitlist(participant_id, workshop_id)
        return True
