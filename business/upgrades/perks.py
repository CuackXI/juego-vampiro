from business.upgrades.interfaces import IPerk
from business.entities.interfaces import IPlayer

class RegenerationPerk(IPerk):

    BASE_LEVEL_STATS = {
        1: 1,
        2: 2,
        3: 5,
        4: 8,
        5: 12
    }

    def __init__(self, player: IPlayer) -> None:
        self.__level = 1
        self.__player = player
        
    def upgrade_amount(self, extra = 0):
        return RegenerationPerk.BASE_LEVEL_STATS[self.__level + extra]

    @property
    def upgradable(self):
        return self.__level != 5

    def upgrade(self):
        if self.__level + 1 in RegenerationPerk.BASE_LEVEL_STATS.keys():
            self.__level += 1

    def to_json(self):
        return {
            'level': self.__level
        }

    def __str__(self):
        if self in self.__player.inventory:
            return f'AUMENTO DE REGENERACIÓN: {self.upgrade_amount(extra = 1)} -> NIVEL {self.__level + 1}'
        
        return f'AUMENTO DE REGENERACIÓN: {self.upgrade_amount()}'

class MaxHealthPerk(IPerk):
    BASE_LEVEL_STATS = {
        1: 25,
        2: 40,
        3: 75,
        4: 150,
        5: 250
    }

    def __init__(self, player: IPlayer) -> None:
        self.__level = 1
        self.__player = player

    def upgrade_amount(self, extra = 0):
        return MaxHealthPerk.BASE_LEVEL_STATS[self.__level + extra]

    @property
    def upgradable(self):
        return self.__level != 5

    def upgrade(self):
        if self.__level + 1 in MaxHealthPerk.BASE_LEVEL_STATS.keys():
            self.__level += 1

    def to_json(self):
        return {
            'level': self.__level
        }

    def __str__(self):
        if self in self.__player.inventory:
            return f'AUMENTO DE VIDA MÁXIMA: {self.upgrade_amount(extra = 1)} -> NIVEL {self.__level + 1}'
        
        return f'AUMENTO DE VIDA MÁXIMA: {self.upgrade_amount()}'

class DamageMultiplierPerk(IPerk):
    BASE_LEVEL_STATS = { #All + 1 from player
        1: 0.1,
        2: 0.5,
        3: 1,
        4: 2,
        5: 4
    }

    def __init__(self, player: IPlayer) -> None:
        self.__level = 1
        self.__player = player

    def upgrade_amount(self, extra = 0):
        return DamageMultiplierPerk.BASE_LEVEL_STATS[self.__level + extra]

    @property
    def upgradable(self):
        return self.__level != 5

    def upgrade(self):
        if self.__level + 1 in DamageMultiplierPerk.BASE_LEVEL_STATS.keys():
            self.__level += 1

    def to_json(self):
        return {
            'level': self.__level
        }

    def __str__(self):
        if self in self.__player.inventory:
            return f'MULTIPLICACION DE DAÑO: {1 + self.upgrade_amount(extra = 1)} -> NIVEL {self.__level + 1}'
        
        return f'MULTIPLICACION DE DAÑO: {1 + self.upgrade_amount()}'

class SpeedPerk(IPerk):
    BASE_LEVEL_STATS = { #All + 1 from player
        1: 0.1,
        2: 0.2,
        3: 0.4,
        4: 0.8,
        5: 1
    }

    def __init__(self, player: IPlayer) -> None:
        self.__level = 1
        self.__player = player

    def upgrade_amount(self, extra = 0):
        return SpeedPerk.BASE_LEVEL_STATS[self.__level + extra]

    @property
    def upgradable(self):
        return self.__level != 5

    def upgrade(self):
        if self.__level + 1 in SpeedPerk.BASE_LEVEL_STATS.keys():
            self.__level += 1

    def to_json(self):
        return {
            'level': self.__level
        }

    def __str__(self):
        if self in self.__player.inventory:
            return f'MULTIPLICACION DE VELOCIDAD: {1 + self.upgrade_amount(extra = 1)} -> NIVEL {self.__level + 1}'
        
        return f'MULTIPLICACION DE VELOCIDAD: {1 + self.upgrade_amount()}'
