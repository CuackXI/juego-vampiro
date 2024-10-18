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
        if self.__spawn_cooldown.is_action_ready() and len(world.monsters) <= 20:
            self.spawn_monster(world)
            self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        player_x = int(world.player.pos_x)
        player_y = int(world.player.pos_y)
        screen_width = settings.SCREEN_WIDTH // 2
        screen_height = settings.SCREEN_HEIGHT // 2

        pos_x = random.randint(player_x - screen_width, player_x + screen_width)
        pos_y = random.randint(player_y - screen_height, player_y + screen_height)

        monster = Monster(pos_x, pos_y, MonsterSprite(pos_x, pos_y))
        world.add_monster(monster)
        # self.__logger.debug("Spawning monster at (%d, %d)", pos_x, pos_y)
