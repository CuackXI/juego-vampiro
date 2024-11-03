"""This module contains the MonsterSpawner class."""

import logging
import random

import pygame

import settings
from business.entities.monster import Monster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from presentation.sprite import MonsterSprite
from presentation.interfaces import IDisplay
import business.handlers.cooldown_handler as CH
from business.exceptions import EntityOutOfBounds

class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""

    BASE_DELAY = 100

    def __init__(self, display: IDisplay):
        self.__display = display
        self.__spawn_cooldown = CH.CooldownHandler(MonsterSpawner.BASE_DELAY)

    def load_saved_data(self, world: IGameWorld, saved_data: list):
        """Loads the monsters from the saved game data.
        
        Args:
            world (IGameWorld): The game world instance.
            saved_data: The saved game data.
        """
        for monster_type in saved_data:
            for monster_data in saved_data[monster_type]:
                monster = Monster(0, 0, monster_data)
                world.add_monster(monster)

    def update(self, world: IGameWorld):
        if self.__spawn_cooldown.is_action_ready() and len(world.monsters) <= 40:
            self.spawn_monster(world)
            self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        """Spawns a monster at the edge of the current camera view.

        Args:
            world (IGameWorld): The game world instance.
            camera (Camera): The camera instance.
        """
        while True:
            try:
                camera_left = self.__display.camera.camera_rect.left
                camera_right = self.__display.camera.camera_rect.right
                camera_top = self.__display.camera.camera_rect.top
                camera_bottom = self.__display.camera.camera_rect.bottom

                edge = random.choice(['top', 'bottom', 'left', 'right'])

                if edge == 'top':
                    pos_x = random.randint(camera_left, camera_right)
                    pos_y = camera_top
                elif edge == 'bottom':
                    pos_x = random.randint(camera_left, camera_right)
                    pos_y = camera_bottom
                elif edge == 'left':
                    pos_x = camera_left
                    pos_y = random.randint(camera_top, camera_bottom)
                else:  # 'right'
                    pos_x = camera_right
                    pos_y = random.randint(camera_top, camera_bottom)

                monster = Monster(pos_x, pos_y)
                world.add_monster(monster)

                break
            except EntityOutOfBounds:
                pass