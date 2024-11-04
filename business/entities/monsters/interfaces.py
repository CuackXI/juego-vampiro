"""Module with special monsters interfaces"""

from abc import abstractmethod
from business.entities.interfaces import *
from business.entities.entity import MovableEntity
from business.upgrades.interfaces import IBulletFactory

class IMonsterGun(MovableEntity, IMonster):
    @property
    @abstractmethod
    def inventory(self) -> list[IBulletFactory]:
        """The monster's invetory.

        Returns:
            list: The list of guns.
        """

    @property
    @abstractmethod
    def multiplier(self) -> float:
        """The multiplier used for the monster's guns.

        Returns:
            float: The multiplier.
        """

class IMonsterBullet(MovableEntity, IUpdatable, ICanMove, IDamageable, ICanDealDamage, JSONable):
    """Interface for monster's bullets."""