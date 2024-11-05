"""Module that contains the monster bullet factory."""

from business.entities.monsters.interfaces import IMonsterGun
from business.upgrades.interfaces import IBulletFactory
from business.entities.bullets import *
from business.handlers.cooldown_handler import CooldownHandler
from presentation.sprite import *
from business.entities.monsters.bullets import MonsterBullet

class MonsterBulletFactory(IBulletFactory):
    """Monster bullet factory implementation."""

    BASE_LEVEL_STATS = {
        1: {
            'COOLDOWN': 5000,
            'DAMAGE': 1,
            'SPEED': 5,
            'HEALTH': 1
        }
    }

    def __init__(self, monster: IMonsterGun = None):
        self.__level = 1

        if monster:
            self.__monster = monster
            self.__sprite = MonsterBulletSprite(0, 0)

            self.__cooldown_handler = CooldownHandler(self.cooldown)

    def load_cooldown(self, amount):
        """Loads the cooldown from the data."""
        self.__cooldown_handler.last_action_time = amount

    def to_json(self):
        return {
            'level': self.__level,
            'attack_cooldown': self.__cooldown_handler.last_action_time
        }

    @staticmethod
    def load_bullets(data, world: IGameWorld):
        """Loads the bullets from the data"""
        for bullet_data in data:
            pos_x = bullet_data['pos_x']
            pos_y = bullet_data['pos_y']
            dir_x = bullet_data['dir_x']
            dir_y = bullet_data['dir_y']
            damage = bullet_data['damage']
            health = bullet_data['health']
            speed = bullet_data['speed']

            dst_x = pos_x + dir_x
            dst_y = pos_y + dir_y

            bullet = MonsterBullet(pos_x,pos_y,dst_x,dst_y,speed,damage,health)
            world.add_bullet(bullet)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_player(world)
    
    def __shoot_at_player(self, world: IGameWorld):
        """Shoots at player."""
        player = world.player

        bullet = MonsterBullet(self.__monster.pos_x, self.__monster.pos_y, player.pos_x, player.pos_y, 
        self.speed, self.damage, self.health)
        world.add_bullet(bullet)

    def upgrade(self):
        if self.__level + 1 in MonsterBulletFactory.BASE_LEVEL_STATS.keys():
            self.__level += 1
    
    @property
    def sprite(self):
        return self.__sprite

    @property
    def upgradable(self):
        return self.__level != max(MonsterBulletFactory.BASE_LEVEL_STATS.keys())

    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__cooldown_handler.put_on_cooldown()
            self.create_bullet(world)

    @property
    def level(self):
        return self.__level

    @property
    def cooldown(self):
        return MonsterBulletFactory.BASE_LEVEL_STATS[self.__level]['COOLDOWN'] / (self.__monster.multiplier * 2)

    @property
    def damage(self):
        return MonsterBulletFactory.BASE_LEVEL_STATS[self.__level]['DAMAGE'] * self.__monster.multiplier * 4

    @property
    def speed(self):
        return MonsterBulletFactory.BASE_LEVEL_STATS[self.__level]['SPEED'] * self.__monster.multiplier
    
    @property
    def health(self):
        return MonsterBulletFactory.BASE_LEVEL_STATS[self.__level]['HEALTH']

    def __str__(self) -> str:
        pass

    def upgrade_amount(self):
        pass