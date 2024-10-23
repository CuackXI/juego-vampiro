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
        SQUARE_ROOT_2 = 1.414 / 2

        d_x, d_y = 0, 0

        if keys[pygame.K_w] and keys[pygame.K_a]:
            d_x, d_y = -SQUARE_ROOT_2, -SQUARE_ROOT_2
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            d_x, d_y = SQUARE_ROOT_2, -SQUARE_ROOT_2
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            d_x, d_y = -SQUARE_ROOT_2, SQUARE_ROOT_2
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            d_x, d_y = SQUARE_ROOT_2, SQUARE_ROOT_2
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

    def __get_pause(self, keys, game):
        if keys[pygame.K_p]:
            return not game.paused

    def process_input(self):
        keys = pygame.key.get_pressed()
        self.__get_player_movement(keys)
    
    def process_pause(self, game):
        keys = pygame.key.get_pressed()
        return self.__get_pause(keys, game)