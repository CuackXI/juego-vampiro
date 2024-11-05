"""Module for DAO interfaces."""

from abc import ABC, abstractmethod

from game import Game

class IGameDAO(ABC):
    """Interface for data access objects for the whole game."""

    @abstractmethod
    def save_game(self, game: "Game"):
        """Saves the current game.

        Args:
            game (Game): The game to be saved.
        """

    @abstractmethod
    def load_game(self) -> dict:
        """Loads the saved game."""

    @abstractmethod
    def clear_save(self):
        """Clears the current save file"""
