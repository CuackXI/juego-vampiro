from abc import abstractmethod

from persistence.json_interfaces import JSONable
from business.common.interfaces import IUpdatable
from presentation.sprite import Sprite

class IPerk(JSONable):
    @abstractmethod
    def upgrade(self):
        """It upgrades the perk to the next level."""

    @abstractmethod
    def upgrade_amount(self) -> int | float:
        """The amount by which it upgrades a player stat.

        Returns:
            int | float: The amount.
        """

    @property
    @abstractmethod
    def sprite(self) -> Sprite:
        """The perk sprite.

        Returns:
            Sprite: The sprite.
        """

    @property
    @abstractmethod
    def upgradable(self) -> bool:
        """If the current perk at the current level can be upgraded.

        Returns:
            bool: If it's upgradable.
        """

    @property
    @abstractmethod
    def level(self) -> bool:
        """Current level of the perk.

        Returns:
            int: The level.
        """

class IBulletFactory(IPerk, IUpdatable):
    @abstractmethod
    def create_bullet(self):
        """Instances bullet of the specified type in the direction given by the player."""

    @abstractmethod
    def load_cooldown(self, cooldown: float):
        """Loads the last cooldown of the CooldownHandler from the save file.

        Args:
            cooldown (float): The cooldown amount.
        """

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