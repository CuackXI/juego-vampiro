"""This module defines the Game class."""

import logging

import pygame

import settings
from business.exceptions import DeadPlayerException
from business.handlers.colission_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.interfaces import IGameWorld
from presentation.interfaces import IInputHandler
from business.handlers.clock import GameClockSingleton

class Game:
    """
    Main game class.

    This is the game entrypoint.
    """

    def __init__(self, game_world: IGameWorld, input_handler: IInputHandler):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__clock = pygame.time.Clock()
        self.__world = game_world
        self.__input_handler = input_handler
        self.__running = True
        self.__paused = False
        self.__dead = False

    @property
    def paused(self):
        return self.__paused

    @property
    def elapsed_time(self):
        return pygame.time.get_ticks()
    
    @property
    def world(self):
        return self.__world

    def close_game_loop(self):
        self.__running = False

    def process_game_events(self):
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:  # pylint: disable=E1101
                self.__logger.debug("QUIT event detected")
                self.__running = False

    def unpause_event(self):
        self.__paused = not self.__paused

    def run(self):
        """Starts the game loop."""
        self.__logger.debug("Starting the game loop.")
        while self.__running:
            try:
                self.process_game_events()

                if not self.__world.in_upgrade and self.__input_handler.is_pause_pressed() and not self.__dead:
                    self.__paused = self.__input_handler.process_pause(self)

                if self.__paused or self.__world.in_upgrade or self.__dead:
                    pass
                else:
                    self.__input_handler.process_input()
                    self.__world.update()
                    CollisionHandler.handle_collisions(self.__world)
                    DeathHandler.check_deaths(self.__world)
                    GameClockSingleton().update()

                self.__world.display.render_frame(self.__paused, self.__world.in_upgrade, self.__dead, self)
                self.__clock.tick(settings.FPS)
            except DeadPlayerException:
                self.__dead = True
            except:
                pass