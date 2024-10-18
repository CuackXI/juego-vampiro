"""This module contains the MonsterSpawner class."""

import logging
import random

import pygame

import settings
from business.entities.monster import Monster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from presentation.sprite import MonsterSprite
from business.handlers.cooldown_handler import CooldownHandler

class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""

    BASE_DELAY = 250

    def __init__(self):
        self.__spawn_cooldown = CooldownHandler(MonsterSpawner.BASE_DELAY)
        self.__logger = logging.getLogger(__name__)

    def update(self, world: IGameWorld):
        if self.__spawn_cooldown.is_action_ready() and len(world.monsters) <= 10:
            self.spawn_monster(world)
            self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        pos_x = random.randint(0, settings.WORLD_WIDTH)
        pos_y = random.randint(0, settings.WORLD_HEIGHT)
        monster = Monster(pos_x, pos_y, MonsterSprite(pos_x, pos_y))
        world.add_monster(monster)
        # self.__logger.debug("Spawning monster at (%d, %d)", pos_x, pos_y)
