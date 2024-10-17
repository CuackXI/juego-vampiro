"""Module for the ExperienceGem class."""

from business.entities.entity import Entity
from business.entities.interfaces import IExperienceGem, IHasPosition
from business.world.interfaces import IGameWorld
from presentation.sprite import ExperienceGemSprite


class ExperienceGem(Entity, IExperienceGem):
    """Represents an experience gem in the game world."""

    def __init__(self, pos_x: float, pos_y: float, amount: int):
        super().__init__(pos_x, pos_y, ExperienceGemSprite(pos_x, pos_y))
        self._logger.debug("Created %s", self)

    @property
    def amount(self) -> int:
        pass

    def __str__(self):
        return f"ExperienceGem(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
    
    def in_player_range(self, player):
        return self._get_distance_to(player) <= player.pick_range

    def update(self, world: IGameWorld):
        super().update(world)
        
        if self._get_distance_to(world.player) <= world.player.pick_range:
            world.remove_experience_gem(self)
