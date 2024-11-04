"""This module contains the CooldownHandler class."""

from business.handlers.clock import GameClockSingleton

class CooldownHandler:
    """A handler for cooldowns."""

    def __init__(self, cooldown_time: int):
        self.last_action_time = GameClockSingleton().game_clock
        self.__cooldown_time = cooldown_time

    def is_action_ready(self):
        """Check if the action is ready to be performed."""
        current_time = GameClockSingleton().game_clock
        return current_time - self.last_action_time >= self.__cooldown_time

    def put_on_cooldown(self):
        """Put the action on cooldown."""
        self.last_action_time = GameClockSingleton().game_clock