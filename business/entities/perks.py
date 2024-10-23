from business.entities.interfaces import IPerk

class RegenerationPerk(IPerk):
    def __init__(self) -> None:
        super().__init__()
    def upgrade(self):
        return super().upgrade()

class MaxHealthPerk(IPerk):
    def __init__(self) -> None:
        super().__init__()
    def upgrade(self):
        return super().upgrade()

class DamageMultiplierPerk(IPerk):
    def __init__(self) -> None:
        super().__init__()
    def upgrade(self):
        return super().upgrade()