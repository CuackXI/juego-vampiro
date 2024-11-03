"""Module for the ExperienceGem class."""

from business.entities.entity import Entity
from business.entities.interfaces import IExperienceGem, IHasPosition
from business.world.interfaces import IGameWorld
from presentation.sprite import ExperienceGemSprite


class ExperienceGem(Entity, IExperienceGem):
    """Represents an experience gem in the game world."""

    def __init__(self, pos_x: float, pos_y: float, amount: int):
        super().__init__(pos_x, pos_y, ExperienceGemSprite(pos_x, pos_y))
        self.__amount = amount

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y
        }

    @property
    def amount(self) -> int:
        return self.__amount

    def __str__(self):
        return f"ExperienceGem(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
    
    def in_player_range(self, player):
        return self._get_distance_to(player) <= player.pick_range