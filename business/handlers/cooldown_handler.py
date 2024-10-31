"""This module contains the CooldownHandler class."""

# from runner import game
import pygame

class CooldownHandler:
    """A handler for cooldowns."""

    def __init__(self, cooldown_time: int, game = None):
        self.__game = game
        # self.__last_action_time = self.__game.game_clock
        self.__last_action_time = pygame.time.get_ticks()
        self.__cooldown_time = cooldown_time

    def is_action_ready(self):
        """Check if the action is ready to be performed."""
        # current_time = self.__game.game_clock
        current_time = pygame.time.get_ticks()
        return current_time - self.__last_action_time >= self.__cooldown_time

    def put_on_cooldown(self):
        """Put the action on cooldown."""
        # self.__last_action_time = self.__game.game_clock
        self.__last_action_time = pygame.time.get_ticks()
