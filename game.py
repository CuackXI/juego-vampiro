"""This module defines the Game class."""

import logging

import pygame

import settings
from business.handlers.colission_handler import CollisionHandler
from business.handlers.death_handler import DeathHandler
from business.world.interfaces import IGameWorld
from business.handlers.clock import GameClockSingleton
from business.exceptions import DeadPlayerException, ResetGame
from presentation.interfaces import IInputHandler
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from persistence.daointerfaces import IGameDAO

class Game:
    """
    Main game class.

    This is the game entrypoint.
    """

    RESET_EVENT = 'RESET'

    def __init__(self, game_world: IGameWorld, input_handler: IInputHandler, dao: "IGameDAO"):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__clock = pygame.time.Clock()
        self.__world = game_world
        self.__input_handler = input_handler
        self.__running = True
        self.__paused = False
        self.__dead = False
        self.__winned = False
        self.__dao = dao

    @property
    def paused(self):
        """If the game is being paused."""
        return self.__paused

    @property
    def elapsed_time(self):
        """The elapsed time using pygame clock"""
        return pygame.time.get_ticks()
    
    @property
    def world(self):
        """The gameworld"""
        return self.__world

    def win(self):
        """Wins the game"""
        self.__winned = True

    def close_game_loop(self):
        """Method to close the game loop"""
        self.__running = False

    def process_game_events(self):
        """Process common pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__logger.debug("QUIT event detected")
                self.__running = False

    def save_game(self):
        """Saves the game if the player is not dead"""
        if not self.__dead:
            self.__dao.save_game(self)

    def clear_save(self):
        """Clears the save file."""
        self.__dao.clear_save()

    def unpause_event(self):
        """Unpauses the game."""
        self.__paused = not self.__paused

    def run(self):
        """Starts the game loop."""
        self.__logger.debug("Starting the game loop.")
        while self.__running:
            try:
                self.process_game_events()

                if not self.__world.in_upgrade and self.__input_handler.is_pause_pressed() and not self.__dead:
                    self.__paused = self.__input_handler.process_pause(self)

                if self.__paused or self.__world.in_upgrade != 0 or self.__dead or self.__winned:
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
            except ResetGame:
                self.clear_save()
                return Game.RESET_EVENT
            
            except Exception as error:
                # For debugging
                print(f'{type(error)} : {error}')