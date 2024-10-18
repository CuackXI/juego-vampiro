"""Player entity module."""

import pygame

from business.entities.bullet import Bullet
from business.entities.entity import MovableEntity
from business.entities.experience_gem import ExperienceGem
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.interfaces import ICanDealDamage, IDamageable, IPlayer
from business.world.interfaces import IGameWorld
from presentation.sprite import Sprite

class Player(MovableEntity, IPlayer, IDamageable, ICanDealDamage):
    """Player entity.

    The player is the main character of the game. It can move around the game world and shoot at monsters.
    """

    BASE_DAMAGE_MULTIPLIER = 1.0
    BASE_SHOOT_COOLDOWN = 200.0
    BASE_HEALTH = 100.0
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
        self.__max_health = Player.BASE_HEALTH
        self.__health: int = Player.BASE_HEALTH
        self.__attack_cooldown = CooldownHandler(Player.BASE_SHOOT_COOLDOWN)
        self.__pick_range = Player.BASE_PICK_RANGE
        self._logger.debug("Created %s", self)

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
    def damage_amount(self):
        return Player.BASE_DAMAGE_MULTIPLIER

    @property
    def health(self) -> int:
        return self.__health
    
    @property
    def max_health(self) -> int:
        return self.__max_health

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

    def __shoot_at_nearest_enemy(self, world: IGameWorld):
        if not world.monsters:
            return  # No monsters to shoot at

        # Find the nearest monster
        monster = min(
            world.monsters,
            key=lambda monster: (
                (monster.pos_x - self.pos_x) ** 2 + (monster.pos_y - self.pos_y) ** 2
            ),
        )

        # Create a bullet towards the nearest monster
        bullet = Bullet(self.pos_x, self.pos_y, monster.pos_x, monster.pos_y, 4, self.damage_amount)
        world.add_bullet(bullet)

    def update(self, world: IGameWorld):
        if self.__attack_cooldown.is_action_ready():
            self.__shoot_at_nearest_enemy(world)
            self.__attack_cooldown.put_on_cooldown()
