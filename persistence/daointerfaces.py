import abc

from game import Game

class IGameDAO:
    @abc.abstractmethod
    def save_game(self, game: 'Game') -> None:
        """Saves the current game.
        """

    @abc.abstractmethod
    def load_game(self) -> dict:
        """Loads the saved game.
        """

    @abc.abstractmethod
    def clear_save(self):
        """Clears the current save file"""