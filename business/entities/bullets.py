"""Module for a bullet entity that moves towards a target direction."""

import math

from business.entities.entity import MovableEntity
from business.entities.interfaces import IBullet, IMonster, IDespawnable
from business.world.interfaces import IGameWorld
from presentation.sprite import BulletSprite, TurretBulletSprite, FollowingBulletSprite
from business.handlers.cooldown_handler import CooldownHandler

class NormalBullet(MovableEntity, IBullet):
    """A bullet that moves towards a target direction."""

    def __init__(self, src_x, src_y, dst_x, dst_y, speed, damage, health):
        super().__init__(src_x, src_y, speed, BulletSprite(src_x, src_y))

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
    
class TurretBullet(MovableEntity, IBullet):
    """A bullet that moves towards a target direction."""

    def __init__(self, src_x, src_y, dst_x, dst_y, speed, damage, health):
        super().__init__(src_x, src_y, speed, TurretBulletSprite(src_x, src_y))
        
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
    
class FollowingBullet(MovableEntity, IBullet, IDespawnable):
    BASE_DESPAWN_COOLDOWN = 2500

    def __init__(self, src_x, src_y, target_monster: IMonster, speed, damage, health, saved_cooldown: float | None = None):
        super().__init__(src_x, src_y, speed, FollowingBulletSprite(src_x, src_y))

        self.__target_monster = target_monster
        self.__damage = damage
        self.__max_health = health
        self.__health = self.__max_health
        self.__despawn_cooldown = CooldownHandler(self.BASE_DESPAWN_COOLDOWN)

        self.__despawn_cooldown.put_on_cooldown()
        if saved_cooldown:
            self.__despawn_cooldown.last_action_time = saved_cooldown

        if target_monster:
            self.__dir_x, self.__dir_y = self.__calculate_direction(self.__target_monster.pos_x - src_x, self.__target_monster.pos_y - src_y)

    def to_json(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'damage': self.__damage,
            'health': self.__health,
            'speed': self.speed,
            'despawn_cooldown': self.__despawn_cooldown.last_action_time
        }

    def __calculate_direction(self, dx, dy):
        """
        Calculate normalized direction vector based on the distance to the target.
        """
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

    @property
    def can_despawn(self) -> bool:
        return self.__despawn_cooldown.is_action_ready()

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)

    def __get_nearest_monster(self, world: IGameWorld) -> IMonster:
        if not world.monsters:
            return None

        monster = min(
            world.monsters,
            key=lambda monster: (
                (monster.pos_x - self.pos_x) ** 2 + (monster.pos_y - self.pos_y) ** 2
            ),
        )

        return monster

    def update(self, world: IGameWorld):
        """Update the bullet's position and movement direction, making it follow the target monster."""
        monster = self.__get_nearest_monster(world)

        if monster is not None:
            self.__target_monster = monster

            dx = self.__target_monster.pos_x - self.pos_x
            dy = self.__target_monster.pos_y - self.pos_y
            self.__dir_x, self.__dir_y = self.__calculate_direction(dx, dy)

            self.move(self.__dir_x, self.__dir_y)
            self.sprite.update()

    @property
    def damage_amount(self):
        return self.__damage
    
    def __str__(self):
        return f"Bullet(pos=({self._pos_x, self._pos_y}), dir=({self.__dir_x, self.__dir_y}))"
