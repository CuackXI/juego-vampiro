"""This module contains interfaces for the game world."""

from abc import ABC, abstractmethod

from business.entities.interfaces import IBullet, IMonster, IPlayer, IItem
from business.upgrades.interfaces import IPerk
from presentation.interfaces import IDisplay
from persistence.json_interfaces import JSONable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.world.interfaces import IMonsterSpawner

class IGameWorld(ABC):
    """Interface for the game world.

    The game world is the environment in which the game entities exist.
    """

    @abstractmethod
    def add_monster(self, monster: IMonster):
        """Adds a monster to the world.

        Args:
            monster (IMonster): The monster to add.
        """

    @abstractmethod
    def remove_monster(self, monster: IMonster):
        """Removes a monster from the world.

        Args:
            monster (IMonster): The monster to remove.
        """

    @abstractmethod
    def add_item(self, item: IItem):
        """Adds an item to the world.

        Args:
            item (IItem): The item.
        """

    @abstractmethod
    def remove_item(self, item: IItem):
        """Removes an item from the world.

        Args:
            item (IItem): The item.
        """

    @abstractmethod
    def add_bullet(self, bullet: IBullet):
        """Adds a bullet to the world.

        Args:
            bullet (IBullet): The bullet to add.
        """

    @abstractmethod
    def remove_bullet(self, bullet: IBullet):
        """Removes a bullet from the world.

        Args:
            bullet (IBullet): The bullet to remove.
        """

    @abstractmethod
    def update(self):
        """Updates the state of the world and all updatable entities within it."""

    @abstractmethod
    def get_perks_for_display(self):
        """Gets a random set of perks for the upgrade menu."""

    @abstractmethod
    def give_perk_to_player(self, perk: IPerk):
        """Gives a certain perk to the world player."""

    @abstractmethod
    def activate_upgrade(self):
        """Creates the activate upgrade state."""

    @property
    @abstractmethod
    def monster_spawner(self) -> "IMonsterSpawner":   
        """The world's monster spawner."""

    @property
    @abstractmethod
    def display(self) -> IDisplay:
        """The world display."""

    @property
    @abstractmethod
    def in_upgrade(self):
        """If the world is in upgrade state."""

    @property
    @abstractmethod
    def game(self):
        """Return the game instance.

        Returns:
            Game: The game.
        """

    @property
    @abstractmethod
    def player(self) -> IPlayer:
        """Gets the player entity.

        Returns:
            IPlayer: The player entity.
        """

    @property
    @abstractmethod
    def monsters(self) -> list[IMonster]:
        """Gets the list of monsters in the world.

        Returns:
            list[IMonster]: A copy of the list of monsters in the world.
        """

    @property
    @abstractmethod
    def bullets(self) -> list[IBullet]:
        """Gets the list of bullets in the world.

        Returns:
            list[IBullet]: A copy of the list of bullets in the world.
        """

    @property
    @abstractmethod
    def items(self) -> list[IItem]:
        """Gets the list of items in the world.

        Returns:
            list[IItem]: A copy of the list of items in the world.
        """


class IUpdatable(ABC):
    """Interface for entities that can be updated."""

    @abstractmethod
    def update(self, world: IGameWorld):
        """Updates the state of the entity.

        Args:
            world (IGameWorld): The game world in which the entity exists.
        """


class IMonsterSpawner(IUpdatable, JSONable):
    """Interface for a monster spawner.

    A monster spawner is responsible for spawning monsters in the game world.
    """

    @abstractmethod
    def load_saved_data(self, data: dict):
        """Loads the latest saved data of the monsters in screen.

        Args:
            data (dict): The data.
        """

    @abstractmethod
    def spawn_monster(self, world: IGameWorld):
        """Spawns a monster in the game world.

        Args:
            world (IGameWorld): The game world in which to spawn the monster.
        """

class ITileMap(ABC):
    """Interface for a tile map.

    A tile map is a grid of tiles that make up the game world.
    Each tile has a value that represents the type of terrain or object at that location.
    """

    @abstractmethod
    def get(self, row, col) -> int:
        """Gets the tile at the specified row and column.

        Args:
            row (int): The row of the tile.
            col (int): The column of the tile.

        Returns:
            int: The tile at the specified row and column.
        """
