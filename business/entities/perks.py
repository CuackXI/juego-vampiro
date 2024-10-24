from business.entities.interfaces import IPerk

class RegenerationPerk(IPerk):

    BASE_LEVEL_STATS = {
        1: 1,
        2: 2,
        3: 5,
        4: 8,
        5: 12
    }

    def __init__(self) -> None:
        self.__level = 1

    @property
    def upgrade_amount(self):
        return RegenerationPerk.BASE_LEVEL_STATS[self.__level]

    @property
    def upgradable(self):
        return self.__level != 5

    def upgrade(self):
        if self.__level + 1 in RegenerationPerk.BASE_LEVEL_STATS.keys():
            self.__level += 1
        
    def __str__(self):
        return f'AUMENTO DE REGENERACIÓN: {self.upgrade_amount}'

class MaxHealthPerk(IPerk):
    BASE_LEVEL_STATS = {
        1: 25,
        2: 40,
        3: 75,
        4: 150,
        5: 250
    }

    def __init__(self) -> None:
        self.__level = 1

    @property
    def upgrade_amount(self):
        return MaxHealthPerk.BASE_LEVEL_STATS[self.__level]

    @property
    def upgradable(self):
        return self.__level != 5

    def upgrade(self):
        if self.__level + 1 in MaxHealthPerk.BASE_LEVEL_STATS.keys():
            self.__level += 1

    def __str__(self):
        return f'AUMENTO DE VIDA MÁXIMA: {self.upgrade_amount}'

class DamageMultiplierPerk(IPerk):
    BASE_LEVEL_STATS = { #All + 1 from player
        1: 0.1,
        2: 0.5,
        3: 1,
        4: 2,
        5: 4
    }

    def __init__(self) -> None:
        self.__level = 1

    @property
    def upgrade_amount(self):
        return DamageMultiplierPerk.BASE_LEVEL_STATS[self.__level]

    @property
    def upgradable(self):
        return self.__level != 5

    def upgrade(self):
        if self.__level + 1 in DamageMultiplierPerk.BASE_LEVEL_STATS.keys():
            self.__level += 1

    def __str__(self):
        return f'MULTIPLICACION DE DAÑO: {1 + self.upgrade_amount}'