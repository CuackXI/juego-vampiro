from abc import ABC, abstractmethod

from business.entities.interfaces import *

class IPerk():
    @abstractmethod
    def upgrade(self):
        """It upgrades the perk to the next level."""

    @property
    @abstractmethod
    def perk_type(self) -> str:
        """The type of perk.

        Returns:
            str: The type.
        """
        
    @abstractmethod
    def upgrade_amount(self) -> int | float:
        """The amount by which it upgrades a player stat.

        Returns:
            int | float: The amount.
        """

    @property
    @abstractmethod
    def upgradable(self) -> bool:
        """If the current perk at the current level can be upgradable.

        Returns:
            bool: If it's upgradable.
        """

class IBulletFactory(IUpdatable):
    @abstractmethod
    def create_bullet(self):
        """Instances bullet of the specified type in the direction given by the player."""

    @property
    @abstractmethod
    def damage(self) -> float:
        """The damage that the bullet will deal.

        Returns:
            float: The damage amount.
        """

    @property
    @abstractmethod
    def speed(self) -> float:
        """The speed at which the bullet will move.

        Returns:
            float: The speed amount.
        """

    @property
    @abstractmethod
    def health(self) -> float:
        """The health that the bullet will have.

        Returns:
            float: The health amount.
        """

    @property
    @abstractmethod
    def cooldown(self) -> int:
        """The cooldown in which it creates bullets.

        Returns:
            int: The cooldown in miliseconds.
        """