"""This module contains interfaces for the entities in the game."""

from abc import ABC, abstractmethod

from presentation.sprite import Sprite

class ICanDealDamage(ABC):
    """Interface for entities that can deal damage."""

    @property
    @abstractmethod
    def damage_amount(self) -> int:
        """The amount of damage the entity can deal.

        Returns:
            int: The amount of damage the entity can deal.
        """


class IDamageable(ABC):
    """Interface for entities that can take damage."""

    @property
    @abstractmethod
    def health(self) -> int:
        """The health of the entity.

        Returns:
            int: The health of the entity.
        """

    @abstractmethod
    def take_damage(self, amount: int):
        """Take damage.

        Args:
            amount (int): The amount of damage to take.
        """


class IUpdatable(ABC):
    """Interface for entities that can be updated."""

    @abstractmethod
    def update(self, world):
        """Update the state of the entity."""


class IHasSprite(ABC):
    """Interface for entities that have a sprite."""

    @property
    @abstractmethod
    def sprite(self) -> Sprite:
        """The sprite of the entity.

        Returns:
            Sprite: The sprite of the entity.
        """


class IHasPosition(IHasSprite):
    """Interface for entities that have a position."""

    @property
    @abstractmethod
    def pos_x(self) -> float:
        """The x-coordinate of the entity.

        Returns:
            float: The x-coordinate of the entity.
        """

    @property
    @abstractmethod
    def pos_y(self) -> float:
        """The y-coordinate of the entity.

        Returns:
            float: The y-coordinate of the entity.
        """


class ICanMove(IHasPosition):
    """Interface for entities that can move."""

    @property
    @abstractmethod
    def speed(self) -> float:
        """The speed of the entity.

        Returns:
            float: The speed of the entity.
        """

    @abstractmethod
    def move(self, direction_x: float, direction_y: float):
        """Move the entity in the given direction based on its speed.

        This method should update the entity's position and sprite.

        Args:
            direction_x (float): The direction in x-coordinate.
            direction_y (float): The direction in y-coordinate.
        """


class IMonster(IUpdatable, ICanMove, IDamageable, ICanDealDamage):
    """Interface for monster entities."""
    @property
    @abstractmethod
    def max_health(self) -> int:
        """The maximum health of the entity.

        Returns:
            int: The maximum health of the entity.
        """

class IBullet(IUpdatable, ICanMove, IDamageable, ICanDealDamage):
    """Interface for bullet entities."""
    
class IItem(IHasPosition):
    @abstractmethod
    def in_player_range(self, player) -> bool:
        """Detects if the player is in range of the gem.

        Args:
            player: The player to check if it's in range.

        Returns:
            bool: If it's in range.
        """

class IExperienceGem(IItem, IHasPosition):
    """Interface for experience gem entities."""

    @property
    @abstractmethod
    def amount(self) -> int:
        """The amount of experience the gem gives.

        Returns:
            int: The amount of experience the gem gives.
        """

class IPlayer(IUpdatable, ICanMove, IDamageable, ICanDealDamage):
    """Interface for the player entity."""

    @abstractmethod
    def pickup_item(self, item: IItem):
        """Picks up an item.

        Args:
            item (IItem): The item.
        """

    @abstractmethod
    def heal(self):
        """Heals the player based on its health regen amount."""

    @property
    @abstractmethod
    def level(self) -> int:
        """The level of the player.

        Returns:
            int: The level of the player.
        """

    @property
    @abstractmethod
    def experience(self) -> int:
        """The experience of the player.

        Returns:
            int: The experience of the player.
        """

    @property
    @abstractmethod
    def experience_to_next_level(self) -> int:
        """The experience required to reach the next level.

        Returns:
            int: The experience required to reach the next level.
        """

    @property
    @abstractmethod
    def damage_multiplier(self) -> float:
        """Indicates the player's damage multiplier.

        Returns:
            float: The multiplier that will be applied on bullets.
        """
    
    @property
    @abstractmethod
    def inventory(self) -> list:
        """A list of all the perks the player has obtained.

        Returns:
            list: The list of perks.
        """

    @abstractmethod
    def handle_perk(self):
        """Handles what happens with a perk with the current inventory"""
