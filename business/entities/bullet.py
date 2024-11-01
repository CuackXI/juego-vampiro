"""Module for a bullet entity that moves towards a target direction."""

import math

from business.entities.entity import MovableEntity
from business.entities.interfaces import IBullet
from business.world.interfaces import IGameWorld
from presentation.sprite import BulletSprite, TurretBulletSprite

class Bullet(MovableEntity, IBullet):
    """A bullet that moves towards a target direction."""

    def __init__(self, src_x, src_y, dst_x, dst_y, speed, damage, health):
        super().__init__(src_x, src_y, speed, BulletSprite(src_x, src_y))
        self.__dir_x, self.__dir_y = self.__calculate_direction(dst_x - src_x, dst_y - src_y)

        self.__damage = damage
        self.__health = health

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
        return self.__damage

    def __str__(self):
        return f"Bullet(pos=({self._pos_x, self._pos_y}), dir=({self.__dir_x, self.__dir_y}))"
    
class TurretBullet(MovableEntity, IBullet):
    """A bullet that moves towards a target direction."""

    def __init__(self, src_x, src_y, dst_x, dst_y, speed, damage, health, world):
        super().__init__(src_x, src_y, speed, TurretBulletSprite(src_x, src_y))
        self.__dir_x, self.__dir_y = self.__calculate_direction(dst_x - src_x, dst_y - src_y)

        self.__damage = damage
        self.__health = health
        self.__world = world

    def __get_nearest_monster(self):  
        if not self.__world.monsters:
            return  # No monsters to shoot at

        # Find the nearest monster
        monster = min(
            self.__world.monsters,
            key=lambda monster: (
                (monster.pos_x - self.__world.player.pos_x) ** 2 + (monster.pos_y - self.__world.player.pos_y) ** 2
            ),)

        

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
        return self.__damage

    def __str__(self):
        return f"Bullet(pos=({self._pos_x, self._pos_y}), dir=({self.__dir_x, self.__dir_y}))"
    
class FollowingBullet(MovableEntity, IBullet):
    def __init__(self, src_x, src_y, dst_x, dst_y, speed, damage, health):
        super().__init__(src_x, src_y, speed, TurretBulletSprite(src_x, src_y))
        self.__dir_x, self.__dir_y = self.__calculate_direction(dst_x - src_x, dst_y - src_y)

        self.__damage = damage
        self.__health = health

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
        self.__calculate_direction()
        self.move(self.__dir_x, self.__dir_y)

    @property
    def damage_amount(self):
        return self.__damage