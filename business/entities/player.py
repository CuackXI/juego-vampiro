"""Player entity module."""

import pygame

from business.entities.bullet import Bullet
from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
from business.entities.bullet_factory import *
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite

class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. It can move around the game world and shoot at monsters.
    """

    BASE_COOLDOWN_MULTIPLIER = 1.0
    BASE_DAMAGE_MULTIPLIER = 1.0
    BASE_SHOOT_COOLDOWN = 200.0
    BASE_HEALTH = 100.0
    BASE_HEALTH_REGEN = 0.0
    BASE_PICK_RANGE = 35.0
    BASE_SPEED = 5.0
    BASE_LEVELS = {
        2: 100,
        3: 250,
        4: 500,
        5: 850,
        6: 1200,
        7: 1700
    }

    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite):
        super().__init__(pos_x, pos_y, Player.BASE_SPEED, sprite)

        self.__experience = 0
        self.__level = 1
        self.__damage_multiplier = Player.BASE_DAMAGE_MULTIPLIER
        self.__max_health = Player.BASE_HEALTH
        self.__health = self.__max_health
        self.__health_regen = Player.BASE_HEALTH_REGEN
        self.__cooldown_multiplier = Player.BASE_COOLDOWN_MULTIPLIER
        self.__pick_range = Player.BASE_PICK_RANGE

        self.__static_inventory = []
        self.__updatable_inventory = [NormalBulletFactory(self)]
        # EpicBulletFactory(self)

    def __str__(self):
        return f"Player(hp={self.__health}, xp={self.__experience}, lvl={self.__level}, pos=({self._pos_x}, {self._pos_y}))"

    @property
    def experience(self):
        return self.__experience

    @property
    def experience_to_next_level(self):
        next_level = self.__level + 1
        
        experience_to_next_level = 0
        if next_level in self.BASE_LEVELS:
            experience_to_next_level = self.BASE_LEVELS[next_level]
        
        return experience_to_next_level
        
    @property
    def pick_range(self):
        return self.__pick_range

    @property
    def level(self):
        return self.__level

    @property
    def damage_multiplier(self):
        return self.__damage_multiplier

    @property
    def damage_amount(self):
        pass

    @property
    def health(self) -> int:
        return self.__health
    
    @property
    def max_health(self) -> int:
        return self.__max_health

    @property
    def cooldown_multiplier(self) -> float:
        return self.__cooldown_multiplier

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)
        self.sprite.take_damage()

    def pickup_gem(self, gem: ExperienceGem):
        self.__gain_experience(gem.amount)

    def __gain_experience(self, amount: int):
        self.__experience += amount
        while self.__experience >= self.experience_to_next_level:
            self.__experience -= self.experience_to_next_level
            self.__level += 1

    def handle_perk(self):
        return super().handle_perk()

    def update(self, world: IGameWorld):
        self.sprite.update()

        for perk in self.__updatable_inventory:
            perk.update(world)