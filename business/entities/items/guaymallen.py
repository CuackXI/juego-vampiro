"""Module for the Guaymallen class."""

from business.entities.entity import Entity
from business.entities.interfaces import IItem
from business.world.interfaces import IGameWorld
from presentation.sprite import GuaymallenSprite


class Guaymallen(Entity, IItem):
    """Guaymallen alfajor that heals 50% of player's max_health"""

    def __init__(self, pos_x: float, pos_y: float):
        super().__init__(pos_x, pos_y, GuaymallenSprite(pos_x, pos_y))
        self.__amount = 0.5

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'amount': self.__amount
        }

    @property
    def amount(self) -> int:
        return self.__amount

    def __str__(self):
        return f"Guaymallen(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
    
    def in_player_range(self, player):
        return self._get_distance_to(player) <= player.pick_range