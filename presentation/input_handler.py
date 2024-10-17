"""This module contains the InputHandler class, which handles user input for the game."""

import pygame

from business.world.game_world import GameWorld
from presentation.interfaces import IInputHandler


class InputHandler(IInputHandler):
    """Handles user input for the game."""

    def __init__(self, world: GameWorld):
        self.__world = world

    def __get_player_movement(self, keys):
        if keys[pygame.K_w]:
            self.__world.player.move(0, -1)

        if keys[pygame.K_s]:
            self.__world.player.move(0, 1)

        if keys[pygame.K_a]:
            self.__world.player.move(-1, 0)
            
        if keys[pygame.K_d]:
            self.__world.player.move(1, 0)

    def process_input(self):
        keys = pygame.key.get_pressed()
        self.__get_player_movement(keys)