"""Module for items interfaces."""

from abc import ABC, abstractmethod
from business.world.interfaces import IGameWorld
from business.entities.entity import Entity

class IItemFactory(ABC):
    """Interface for item factories"""

    @staticmethod
    @abstractmethod
    def create_item(type: str, entity: Entity, world: IGameWorld):
        """Creates an item given an item type.

        Args:
            type (str): The type.
            entity (Entity): The entity where the item will be created.
            world (IGameWorld): The world where this item is created.
        """

    @staticmethod
    @abstractmethod
    def load_items(world: IGameWorld, saved_data: dict):
        """Loads items from the data file.

        Args:
            world (IGameWorld): The world.
            saved_data (dict): The data.
        """