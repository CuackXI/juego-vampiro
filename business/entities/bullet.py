"""Module for a bullet entity that moves towards a target direction."""

import math

from business.entities.entity import MovableEntity
from business.entities.interfaces import IBullet
from business.world.interfaces import IGameWorld
from presentation.sprite import BulletSprite

class Bullet(MovableEntity, IBullet):
    """A bullet that moves towards a target direction."""

    BASE_DAMAGE = 200
    BASE_HEALTH = 5

    def __init__(self, src_x, src_y, dst_x, dst_y, speed, damage_multiplier):
        super().__init__(src_x, src_y, speed, BulletSprite(src_x, src_y))
        self.__dir_x, self.__dir_y = self.__calculate_direction(dst_x - src_x, dst_y - src_y)

        self.__health = Bullet.BASE_HEALTH

        self._logger.debug("Created %s", self)

    def __calculate_direction(self, dx, dy):
        distance = math.hypot(dx, dy)
        if distance != 0:
            return dx / distance, dy / distance
        return 0, 0

    @property
    def health(self) -> int:
        return self.__health

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)

    def update(self, _: IGameWorld):
        self.move(self.__dir_x, self.__dir_y)

    @property
    def damage_amount(self):
        return Bullet.BASE_DAMAGE

    def __str__(self):
        return f"Bullet(pos=({self._pos_x, self._pos_y}), dir=({self.__dir_x, self.__dir_y}))"
