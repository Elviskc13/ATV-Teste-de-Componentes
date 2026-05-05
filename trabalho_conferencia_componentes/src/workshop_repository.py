class WorkshopRepository:
    def __init__(self):
        self._workshops = {
            1: {"title": "Pytest Avançado", "available": True},
            2: {"title": "Arquitetura de Software", "available": True},
            3: {"title": "DevOps na Prática", "available": False},
        }

    def exists(self, workshop_id: int) -> bool:
        return workshop_id in self._workshops

    def is_available(self, workshop_id: int) -> bool:
        if workshop_id not in self._workshops:
            return False
        return self._workshops[workshop_id]["available"]

    def mark_unavailable(self, workshop_id: int) -> None:
        if workshop_id not in self._workshops:
            raise ValueError("Workshop not found")
        self._workshops[workshop_id]["available"] = False

    def mark_available(self, workshop_id: int) -> None:
        if workshop_id not in self._workshops:
            raise ValueError("Workshop not found")
        self._workshops[workshop_id]["available"] = True
