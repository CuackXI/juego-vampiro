"""This module defines the Game class."""

import logging

import pygame

import settings
from business.exceptions import DeadPlayerException
from business.handlers.colission_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.interfaces import IGameWorld
from presentation.interfaces import IDisplay, IInputHandler


class Game:
    """
    Main game class.

    This is the game entrypoint.
    """

    def __init__(self, display: IDisplay, game_world: IGameWorld, input_handler: IInputHandler):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__clock = pygame.time.Clock()
        self.__display = display
        self.__world = game_world
        self.__input_handler = input_handler
        self.__running = True
        self.__paused = False
        self.__in_upgrade_menu = False

    @property
    def paused(self):
        return self.__paused

    @property
    def in_upgrade_menu(self):
        return self.__in_upgrade_menu
    
    @in_upgrade_menu.setter
    def in_upgrade_menu(self, value: bool):
        self.__in_upgrade_menu = value

    @property
    def elapsed_time(self):
        return pygame.time.get_ticks()

    def close_game_loop(self):
        self.__running = False

    def __process_game_events(self):
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
                self.__process_game_events()

                if self.__input_handler.is_pause_pressed():
                    self.__paused = self.__input_handler.process_pause(self)

                if self.__world.in_upgrade:
                    self.__in_upgrade_menu = True

                if not self.__paused or not self.__in_upgrade_menu:
                    self.__input_handler.process_input()
                    self.__world.update()
                    CollisionHandler.handle_collisions(self.__world)
                    DeathHandler.check_deaths(self.__world)

                self.__display.render_frame(self.__paused, self.__in_upgrade_menu, self)

                self.__clock.tick(settings.FPS)
            except DeadPlayerException:
                self.__running = False