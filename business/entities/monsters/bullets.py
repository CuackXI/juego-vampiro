"""Module for a bullet entity that moves towards a target direction for a monster."""

import math

from business.entities.monsters.interfaces import IMonsterBullet
from business.world.interfaces import IGameWorld
from presentation.sprite import MonsterBulletSprite

class MonsterBullet(IMonsterBullet):
    """A bullet that moves towards a target direction."""

    def __init__(self, src_x, src_y, dst_x, dst_y, speed, damage, health):
        super().__init__(src_x, src_y, speed, MonsterBulletSprite(src_x, src_y))

        self.__dir_x, self.__dir_y = self.__calculate_direction(dst_x - src_x, dst_y - src_y)
        self.__damage = damage
        self.__max_health = health
        self.__health = self.__max_health 

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'dir_x': self.__dir_x,
            'dir_y': self.__dir_y,
            'damage': self.__damage,
            'health': self.__health,
            'speed': self.speed
        }

    def __calculate_direction(self, dx, dy):
        """Calculates a direction to other position."""
        distance = math.hypot(dx, dy)
        if distance != 0:
            return dx / distance, dy / distance
        return 0, 0

    @property
    def max_health(self) -> float:
        return self.__max_health

    @property
    def health(self) -> float:
        return self.__health

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)

    def update(self, _: IGameWorld):
        self.move(self.__dir_x, self.__dir_y)

    @property
    def damage_amount(self):
        return self.__damage

    def __str__(self):
        return f"Bullet(pos=({self._pos_x, self._pos_y}), dir=({self.__dir_x, self.__dir_y}))"