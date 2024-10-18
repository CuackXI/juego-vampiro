"""This module contains the InputHandler class, which handles user input for the game."""

import pygame

from business.world.game_world import GameWorld
from presentation.interfaces import IInputHandler
from business.handlers.boundaries_handler import BoundariesHandler

class InputHandler(IInputHandler):
    """Handles user input for the game."""

    def __init__(self, world: GameWorld):
        self.__world = world

    def __get_player_movement(self, keys):
        SQ_RT_2 = 2 ** 0.5 / 2

        d_x, d_y = 0, 0

        if keys[pygame.K_w] and keys[pygame.K_a]:
            d_x, d_y = -SQ_RT_2, -SQ_RT_2
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            d_x, d_y = SQ_RT_2, -SQ_RT_2
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            d_x, d_y = -SQ_RT_2, SQ_RT_2
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            d_x, d_y = SQ_RT_2, SQ_RT_2
        elif keys[pygame.K_w]:
            d_x, d_y = 0, -1
        elif keys[pygame.K_s]:
            d_x, d_y = 0, 1
        elif keys[pygame.K_a]:
            d_x, d_y = -1, 0
        elif keys[pygame.K_d]:
            d_x, d_y = 1, 0

        self.__world.player.move(d_x, d_y)
        
        if not BoundariesHandler.is_entity_within_world_boundaries(self.__world.player):
            self.__world.player.move(-d_x, -d_y)

    def process_input(self):
        keys = pygame.key.get_pressed()
        self.__get_player_movement(keys)