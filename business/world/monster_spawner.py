"""This module contains the MonsterSpawner class."""

import logging
import random

import pygame

import settings
from business.entities.monster import Monster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from presentation.sprite import MonsterSprite
import business.handlers.cooldown_handler as CH
from business.exceptions import EntityOutOfBounds

class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""

    BASE_DELAY = 250

    def __init__(self):
        self.__spawn_cooldown = CH.CooldownHandler(MonsterSpawner.BASE_DELAY)
        self.__logger = logging.getLogger(__name__)

    def update(self, world: IGameWorld):
        if self.__spawn_cooldown.is_action_ready() and len(world.monsters) <= 20:
            self.spawn_monster(world)
            self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        #TODO: CAMBIAR ESTO PARA QUE USE LOS BORDES DE LA CAMARA (TIRA CIRCULAR IMPORT CUALQUIER IMPORT DEL RUNNER)
        while True:
            try:
                player_x = int(world.player.pos_x)
                player_y = int(world.player.pos_y)
                screen_width = settings.SCREEN_WIDTH // 2
                screen_height = settings.SCREEN_HEIGHT // 2

                left_edge = player_x - screen_width
                right_edge = player_x + screen_width
                top_edge = player_y - screen_height
                bottom_edge = player_y + screen_height

                edge = random.choice(['top', 'bottom', 'left', 'right'])

                if edge == 'top':
                    pos_x = random.randint(left_edge, right_edge)
                    pos_y = top_edge
                elif edge == 'bottom':
                    pos_x = random.randint(left_edge, right_edge)
                    pos_y = bottom_edge
                elif edge == 'left':
                    pos_x = left_edge
                    pos_y = random.randint(top_edge, bottom_edge)
                else:
                    pos_x = right_edge
                    pos_y = random.randint(top_edge, bottom_edge)

                monster = Monster(pos_x, pos_y, MonsterSprite(pos_x, pos_y))
                world.add_monster(monster)

                break
            except EntityOutOfBounds:
                print("Spawneando en otra posicion :v")