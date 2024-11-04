"""Module for the ExperienceGem class."""

from business.entities.entity import Entity
from business.entities.interfaces import IExperienceGem, IPlayer
from presentation.sprite import ExperienceGemSprite, RedExperienceGemSprite, GreenExperienceGemSprite, BlueExperienceGemSprite
from business.handlers.cooldown_handler import CooldownHandler


class ExperienceGem(Entity, IExperienceGem):
    """Represents an experience gem in the game world."""
    
    BASE_DESPAWN_COOLDOWN = 10000

    def __init__(self, pos_x: float, pos_y: float, amount: int, saved_cooldown: float | None = None):
        super().__init__(pos_x, pos_y, ExperienceGemSprite(pos_x, pos_y))
        self.__despawn_cooldown = CooldownHandler(ExperienceGem.BASE_DESPAWN_COOLDOWN)
        self.__amount = amount

        self.__despawn_cooldown.put_on_cooldown()
        if saved_cooldown:
            self.__despawn_cooldown.last_action_time = saved_cooldown

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'amount': self.__amount,
            'despawn_cooldown': self.__despawn_cooldown.last_action_time
        }

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def can_despawn(self) -> bool:
        return self.__despawn_cooldown.is_action_ready()

    def __str__(self):
        return f"ExperienceGem(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
    
    def in_player_range(self, player: IPlayer):
        return self._get_distance_to(player) <= player.pick_range

class RedExperienceGem(Entity, IExperienceGem):
    """Represents a red experience gem in the game world."""
    
    BASE_DESPAWN_COOLDOWN = 30000

    def __init__(self, pos_x: float, pos_y: float, amount: int, saved_cooldown: float | None = None):
        super().__init__(pos_x, pos_y, RedExperienceGemSprite(pos_x, pos_y))
        self.__despawn_cooldown = CooldownHandler(RedExperienceGem.BASE_DESPAWN_COOLDOWN)
        self.__amount = amount

        self.__despawn_cooldown.put_on_cooldown()
        if saved_cooldown:
            self.__despawn_cooldown.last_action_time = saved_cooldown

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'amount': self.__amount,
            'despawn_cooldown': self.__despawn_cooldown.last_action_time
        }

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def can_despawn(self) -> bool:
        return self.__despawn_cooldown.is_action_ready()

    def __str__(self):
        return f"ExperienceGem(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
    
    def in_player_range(self, player: IPlayer):
        return self._get_distance_to(player) <= player.pick_range
    
class GreenExperienceGem(Entity, IExperienceGem):
    """Represents a green experience gem in the game world."""
    
    BASE_DESPAWN_COOLDOWN = 15000

    def __init__(self, pos_x: float, pos_y: float, amount: int, saved_cooldown: float | None = None):
        super().__init__(pos_x, pos_y, GreenExperienceGemSprite(pos_x, pos_y))
        self.__despawn_cooldown = CooldownHandler(GreenExperienceGem.BASE_DESPAWN_COOLDOWN)
        self.__amount = amount

        self.__despawn_cooldown.put_on_cooldown()
        if saved_cooldown:
            self.__despawn_cooldown.last_action_time = saved_cooldown

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'amount': self.__amount,
            'despawn_cooldown': self.__despawn_cooldown.last_action_time
        }

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def can_despawn(self) -> bool:
        return self.__despawn_cooldown.is_action_ready()

    def __str__(self):
        return f"ExperienceGem(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
    
    def in_player_range(self, player: IPlayer):
        return self._get_distance_to(player) <= player.pick_range
    
class BlueExperienceGem(Entity, IExperienceGem):
    """Represents a blue experience gem in the game world."""
    
    BASE_DESPAWN_COOLDOWN = 20000

    def __init__(self, pos_x: float, pos_y: float, amount: int, saved_cooldown: float | None = None):
        super().__init__(pos_x, pos_y, BlueExperienceGemSprite(pos_x, pos_y))
        self.__despawn_cooldown = CooldownHandler(BlueExperienceGem.BASE_DESPAWN_COOLDOWN)
        self.__amount = amount

        self.__despawn_cooldown.put_on_cooldown()
        if saved_cooldown:
            self.__despawn_cooldown.last_action_time = saved_cooldown

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'amount': self.__amount,
            'despawn_cooldown': self.__despawn_cooldown.last_action_time
        }

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def can_despawn(self) -> bool:
        return self.__despawn_cooldown.is_action_ready()

    def __str__(self):
        return f"ExperienceGem(amount={self.__amount}, pos=({self.pos_x}, {self.pos_y}))"
    
    def in_player_range(self, player: IPlayer):
        return self._get_distance_to(player) <= player.pick_range