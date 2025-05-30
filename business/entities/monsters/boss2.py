"""This module contains the Monster class, which represents a monster entity in the game."""

from business.entities.entity import MovableEntity
from business.entities.interfaces import IDamageable, IHasPosition, IMonster
from business.handlers.cooldown_handler import CooldownHandler
from business.world.interfaces import IGameWorld
from presentation.sprite import BigBossMonsterSprite
import math

class BigBossMonster(MovableEntity, IMonster):
    """A monster entity in the game."""

    BASE_SPEED = 4
    BASE_HEALTH = 10000
    BASE_DAMAGE = 10000
    BASE_ATTACK_RANGE = 50
    BASE_ATTACK_COOLDOWN = 0

    def __init__(self, src_x: int, src_y: int, saved_data: dict | None = None):
        super().__init__(src_x, src_y, BigBossMonster.BASE_SPEED, BigBossMonsterSprite(0, 0, 0.5))

        self.__speed = BigBossMonster.BASE_SPEED
        self.__max_health = BigBossMonster.BASE_HEALTH
        self.__health = self.max_health
        self.__damage = BigBossMonster.BASE_DAMAGE
        self.__attack_range = BigBossMonster.BASE_ATTACK_RANGE
        self.__attack_cooldown = CooldownHandler(BigBossMonster.BASE_ATTACK_COOLDOWN)

        if saved_data:
            self.__load_saved_data(saved_data)

    def __load_saved_data(self, saved_data: dict):
        self._pos_x = saved_data['pos_x']
        self._pos_y = saved_data['pos_y']
        self.__health = saved_data['health']
        self.__attack_cooldown.last_action_time = saved_data['attack_cooldown']

    def to_json(self):
        return {
            'pos_x': self._pos_x,
            'pos_y': self._pos_y,
            'health': self.__health,
            'attack_cooldown': self.__attack_cooldown.last_action_time
        }

    def attack(self, target: IDamageable):
        """Attacks the target."""
        if not self.__attack_cooldown.is_action_ready():
            return

        if self._get_distance_to(target) < self.__attack_range:
            target.take_damage(self.damage_amount)
            self.__attack_cooldown.put_on_cooldown()

    @property
    def damage_amount(self):
        return self.__damage

    @property
    def max_health(self):
        return self.__max_health

    def __get_normalized_direction(self, entity: "IHasPosition"):
        """Calculates a direction to other position."""
        x1, y1 = self.pos_x, self.pos_y
        x2, y2 = entity.pos_x, entity.pos_y
        vector_x = x2 - x1
        vector_y = y2 - y1

        magnitud = math.sqrt(vector_x**2 + vector_y**2)

        if magnitud == 0:
            magnitud = 0.00000001 # ZERO DIVISION ERROR

        direccion_x = vector_x / magnitud
        direccion_y = vector_y / magnitud
        return direccion_x, direccion_y

    def __get_direction_towards_the_player(self, world: IGameWorld):
        """Gets direction towards the player."""
        dir_x, dir_y = self.__get_normalized_direction(world.player)

        return dir_x, dir_y

    def update(self, world: IGameWorld):
        direction_x, direction_y = self.__get_direction_towards_the_player(world)
        if (direction_x, direction_y) == (0, 0):
            return

        self.move(direction_x, direction_y)

        self.attack(world.player)

        self.sprite.update()

    def __str__(self):
        return f"Monster(hp={self.health}, pos={self.pos_x, self.pos_y})"

    @property
    def health(self) -> float:
        return self.__health
    
    @health.setter
    def health(self, value):
        self.__health = value
            
    @property
    def speed(self) -> float:
        self.__speed

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()
