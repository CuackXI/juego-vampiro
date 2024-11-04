"""Player entity module."""

import pygame

from business.entities.entity import MovableEntity
from business.entities.items.experience_gem import IExperienceGem
from business.entities.items.guaymallen import Guaymallen
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer, IItem
from business.upgrades.interfaces import IBulletFactory
from business.handlers.cooldown_handler import CooldownHandler
from business.upgrades.perks import *
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
    BASE_SPEED_MULTIPLIER = 1.0
    BASE_LEVELS_EXP = {
        2: 5,
        3: 10,
        4: 20,
        5: 30,
        6: 50,
        7: 70,
        8: 100,
        9: 100,
        10: 100
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
        self.__speed_multiplier = Player.BASE_SPEED_MULTIPLIER

        self.__static_inventory: list[IPerk] = []
        self.__updatable_inventory: list[IBulletFactory] = []

        if saved_data:
            self.__load_saved_data(saved_data)

    def __load_saved_data(self, saved_data: dict):
        self._pos_x = saved_data['pos_x']
        self._pos_y = saved_data['pos_y']
        self.__experience = saved_data['experience']
        self.__level = saved_data['level']
        self.__health = saved_data['health']
        self.__health_regen_cooldown.last_action_time = saved_data['health_regen_cooldown']

    def __str__(self):
        return f"Player(hp={self.__health}, xp={self.__experience}, lvl={self.__level}, pos=({self._pos_x}, {self._pos_y}))"

    def to_json(self):
        return {
            'pos_x': self._pos_x,
            'pos_y': self._pos_y,
            'experience': self.__experience,
            'level': self.__level,
            'health': self.__health,
            'health_regen_cooldown': self.__health_regen_cooldown.last_action_time,
            'static':{str(type(perk)): perk.to_json() for perk in self.__static_inventory},
            'updatable':{str(type(perk)): perk.to_json() for perk in self.__updatable_inventory}
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
    def speed_multiplier(self):
        for perk in self.__static_inventory:
            if isinstance(perk, SpeedPerk):
                return self.__speed_multiplier + perk.upgrade_amount() 

        return self.__speed_multiplier

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
                return self.__max_health + perk.upgrade_amount()
        return self.__max_health

    @property
    def cooldown_multiplier(self) -> float:
        return self.__cooldown_multiplier

    @property
    def health_regen(self):
        for perk in self.__static_inventory:
            if isinstance(perk, RegenerationPerk):
                return self.__health_regen + perk.upgrade_amount()
        return self.__health_regen

    @property
    def inventory(self):
        perks = []
        for perk in self.__updatable_inventory:
            perks.append(perk)

        for perk in self.__static_inventory:
            perks.append(perk)

        return perks

    @property
    def experience_progress(self) -> float:
        if self.__level == 1:
            return (self.__experience / self.experience_to_next_level)
        elif self.__level in self.BASE_LEVELS_EXP:
            return (self.__experience / self.experience_to_next_level) if self.experience_to_next_level else 0
        return 0

    def move(self, direction_x: float, direction_y: float):
        self._pos_x += direction_x * self._speed * self.speed_multiplier
        self._pos_y += direction_y * self._speed * self.speed_multiplier

        self.sprite.update_pos(self._pos_x, self._pos_y)


    def take_damage(self, amount):
        self.__health = max(0, self.__health - amount)

        self.sprite.take_damage()

    def heal(self, amount, color = None):
        self.__health += amount
        if self.__health > self.max_health:
            self.__health = self.max_health

        if color:
            self.sprite.heal()

    def pickup_item(self, item: IItem, world: IGameWorld):
        if isinstance(item, IExperienceGem):
            self.__gain_experience(item.amount, world)

        elif isinstance(item, Guaymallen):
            self.heal(self.max_health * 0.2, color = True)

    def __gain_experience(self, amount: int, world: IGameWorld):
        self.__experience += amount

        last_level = self.__level

        while self.__experience >= self.experience_to_next_level:
            self.__experience -= self.experience_to_next_level
            self.__level += 1
            if self.__level not in Player.BASE_LEVELS_EXP.keys():
                self.__level -= 1
                self.__experience = self.BASE_LEVELS_EXP[self.__level]
                break 
            else:
                world.activate_upgrade(self.__level - last_level)

    def handle_perk(self, perk: IPerk):
        if isinstance(perk, IBulletFactory):
            if perk not in self.__updatable_inventory:
                self.__updatable_inventory.append(perk)
            else:
                perk.upgrade()
        elif perk not in self.__static_inventory:
            self.__static_inventory.append(perk)
        else:
            perk.upgrade()

    def update(self, world: IGameWorld):
        self.sprite.update()

        for perk in self.__updatable_inventory:
            perk.update(world)

        if self.__health_regen_cooldown.is_action_ready() and self.__health < self.max_health:
            self.heal(self.health_regen)
            self.__health_regen_cooldown.put_on_cooldown()