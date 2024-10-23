from business.entities.interfaces import IPerk

class RegenerationPerk(IPerk):

    BASE_LEVELS = {
        2: 2,
        3: 5,
        4: 8,
        5: 12
    }

    def __init__(self) -> None:
        self.__regen = 1

    @property
    def upgrade_amount(self):
        return self.__regen

    def upgrade(self):
        return super().upgrade()

class MaxHealthPerk(IPerk):
    BASE_LEVELS = {
        2: 40,
        3: 75,
        4: 150,
        5: 250
    }

    def __init__(self) -> None:
        self.__health = 25

    @property
    def upgrade_amount(self):
        return self.__health

    def upgrade(self):
        return super().upgrade()

class DamageMultiplierPerk(IPerk):
    BASE_LEVELS = {
        2: 1.5,
        3: 2,
        4: 3,
        5: 5
    }

    def __init__(self) -> None:
        self.__damage_multiplier: 1.2

    @property
    def upgrade_amount(self):
        return self.__damage_multiplier

    def upgrade(self):
        return super().upgrade()