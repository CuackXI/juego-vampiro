"""This module contains the Monster class, which represents a monster entity in the game."""

from business.entities.interfaces import IDamageable, IHasPosition
from business.entities.monsters.upgrades.bullet_factory import MonsterBulletFactory
from business.world.interfaces import IGameWorld
from presentation.sprite import GunMonsterSprite
from business.handlers.clock import GameClockSingleton
from business.entities.monsters.interfaces import IMonsterGun
import math

class GunMonster(IMonsterGun):
    """A monster entity that shoots bullets."""

    BASE_SPEED = 1
    BASE_HEALTH = 10
    BASE_ATTACK_RANGE = 20000

    def __init__(self, src_x: int, src_y: int, saved_data: dict | None = None):
        if GameClockSingleton().game_clock / 66000 < 1:
            self.__multiplier = 1
        else:
            self.__multiplier = GameClockSingleton().game_clock / 50000

        super().__init__(src_x, src_y, GunMonster.BASE_SPEED * self.__multiplier, GunMonsterSprite(0, 0, self.__multiplier))

        self.__speed = GunMonster.BASE_SPEED
        self.__max_health = GunMonster.BASE_HEALTH
        self.__health = self.max_health
        self.__attack_range = GunMonster.BASE_ATTACK_RANGE

        self.__inventory = [MonsterBulletFactory(self)]

        if saved_data:
            self.__load_saved_data(saved_data)

    def __load_saved_data(self, saved_data: dict):
        """Loads saved data from the data file."""
        self._pos_x = saved_data['pos_x']
        self._pos_y = saved_data['pos_y']
        self.__health = saved_data['health']

        for gun in saved_data['inventory']:
            if 'MonsterBulletFactory' in gun:
                for bullet_factory in self.__inventory:
                    if isinstance(gun, MonsterBulletFactory):
                        bullet_factory.load_cooldown(gun['attack_cooldown'])

    def to_json(self):
        return {
            'pos_x': self._pos_x,
            'pos_y': self._pos_y,
            'health': self.__health,
            'inventory':{str(type(perk)): perk.to_json() for perk in self.__inventory}
        }

    def attack(self, target: IDamageable, world: IGameWorld):
        """Attacks the target."""
        if self._get_distance_to(target) < self.__attack_range:
            for gun in self.__inventory:
                gun.update(world)

    @property
    def damage_amount(self):
        pass

    @property
    def max_health(self):
        return self.__max_health * self.__multiplier

    @property
    def inventory(self):
        return self.__inventory

    def __get_normalized_direction(self, entity: "IHasPosition"):
        """Gets direction to an entity."""
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

        self.attack(world.player, world)
        self.move(direction_x, direction_y)

        self.sprite.update()

    def __str__(self):
        return f"Monster(hp={self.health}, pos={self.pos_x, self.pos_y})"

    @property
    def health(self) -> float:
        return self.__health
    
    @property
    def speed(self) -> float:
        if self.__speed * self.__multiplier > 4:
            return 4
        return self.__speed * self.__multiplier

    @property
    def multiplier(self) -> float:
        return self.__multiplier

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()
