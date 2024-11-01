"""Player entity module."""

import pygame

from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
import business.entities.bullet_factory as bf
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.perks import *
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite


class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. It can move around the game world and shoot at monsters."""

    BASE_COOLDOWN_MULTIPLIER = 1.0
    BASE_DAMAGE_MULTIPLIER = 1.0
    BASE_HEALTH_REGEN_COOLDWON = 1000
    BASE_HEALTH = 100.0
    BASE_HEALTH_REGEN = 0.5
    BASE_PICK_RANGE = 35.0
    BASE_SPEED = 5.0
    BASE_LEVELS_EXP = {
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 1
    }

    def __init__(self, pos_x: int, pos_y: int, sprite: Sprite, saved_data: dict | None = None):
        super().__init__(pos_x, pos_y, Player.BASE_SPEED, sprite)

        self.__experience = 0
        self.__level = 1
        self.__damage_multiplier = Player.BASE_DAMAGE_MULTIPLIER
        self.__max_health = Player.BASE_HEALTH
        self.__health = self.__max_health
        self.__health_regen = Player.BASE_HEALTH_REGEN
        self.__cooldown_multiplier = Player.BASE_COOLDOWN_MULTIPLIER
        self.__pick_range = Player.BASE_PICK_RANGE
        self.__health_regen_cooldown = CooldownHandler(Player.BASE_HEALTH_REGEN_COOLDWON)

        self.__static_inventory = []
        self.__updatable_inventory = []

        if saved_data:
            self.__load_saved_data(saved_data)

    def __load_saved_data(self, saved_data: dict):
        self._pos_x = saved_data['pos_x']
        self._pos_y = saved_data['pos_y']
        self.__experience = saved_data['experience']
        self.__level = saved_data['level']
        self.__health = saved_data['health']

    def __str__(self):
        return f"Player(hp={self.__health}, xp={self.__experience}, lvl={self.__level}, pos=({self._pos_x}, {self._pos_y}))"

    def to_json(self):
        return {
            'pos_x': self._pos_x,
            'pos_y': self._pos_y,
            'experience': self.__experience,
            'level': self.__level,
            'health': self.__health
        }

    @property
    def experience(self):
        return self.__experience

    @property
    def experience_to_next_level(self):
        next_level = self.__level + 1
        
        experience_to_next_level = 0
        if next_level in self.BASE_LEVELS_EXP:
            experience_to_next_level = self.BASE_LEVELS_EXP[next_level]
        else:
            experience_to_next_level = self.BASE_LEVELS_EXP[self.__level]
        
        return experience_to_next_level

    @property
    def pick_range(self):
        return self.__pick_range

    @property
    def level(self):
        return self.__level

    @property
    def damage_multiplier(self):
        for perk in self.__static_inventory:
            if isinstance(perk, DamageMultiplierPerk):
                return self.__damage_multiplier + perk.upgrade_amount() 

        return self.__damage_multiplier

    @property
    def damage_amount(self):
        pass

    @property
    def health(self) -> int:
        return self.__health
    
    @property
    def max_health(self) -> int:
        for perk in self.__static_inventory:
            if isinstance(perk, MaxHealthPerk):
                return self.__max_health + perk.upgrade_amount

        return self.__max_health

    @property
    def cooldown_multiplier(self) -> float:
        return self.__cooldown_multiplier

    @property
    def health_regen(self):
        for perk in self.__static_inventory:
            if isinstance(perk, RegenerationPerk):
                return self.__health_regen + perk.upgrade_amount 
        return self.__health_regen

    @property
    def inventory(self):
        perks = []
        for perk in self.__updatable_inventory:
            perks.append(perk)

        for perk in self.__static_inventory:
            perks.append(perk)

        return perks

    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)

        self.sprite.take_damage()

    def heal(self):
        self.__health += self.health_regen
        if self.__health > self.max_health:
            self.__health = self.max_health

    def pickup_gem(self, gem: ExperienceGem, world: IGameWorld):
        self.__gain_experience(gem.amount, world)

    def __gain_experience(self, amount: int, world: IGameWorld):
        self.__experience += amount
        while self.__experience >= self.experience_to_next_level:
            self.__experience -= self.experience_to_next_level
            self.__level += 1
            if self.__level not in Player.BASE_LEVELS_EXP.keys():
                self.__level -= 1
                
            world.activate_upgrade()

    def handle_perk(self, perk):
        if isinstance(perk, bf.IBulletFactory):
            if perk not in self.__updatable_inventory:
                self.__updatable_inventory.append(perk)
            else:
                perk.upgrade()
        elif perk not in self.__static_inventory:
            self.__static_inventory.append(perk)
        else:
            perk.upgrade()

        print(self.__updatable_inventory)
        print(self.__static_inventory)

    def update(self, world: IGameWorld):
        self.sprite.update()

        for perk in self.__updatable_inventory:
            perk.update(world)

        if self.__health_regen_cooldown.is_action_ready() and self.__health < self.max_health:
            self.heal()
            self.__health_regen_cooldown.put_on_cooldown()