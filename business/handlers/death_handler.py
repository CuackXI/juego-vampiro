"""Module that contains the DeathHandler class."""

from business.entities.items.experience_gem import *
from business.entities.items.guaymallen import Guaymallen
from business.exceptions import DeadPlayerException
from business.world.interfaces import IGameWorld
from business.handlers.boundaries_handler import BoundariesHandler
from business.entities.interfaces import IDespawnable
from business.entities.monsters.monster import Monster
from business.entities.monsters.boss import BossMonster
from business.entities.monsters.boss2 import BigBossMonster
from business.entities.items.item_factory import ItemFactory
import random

class DeathHandler:
    """Class that handles entity deaths."""

    @staticmethod
    def check_deaths(world: IGameWorld):
        """Check if any entities have died and remove them from the game world.

        Args:
            world (IGameWorld): The game world to check for dead entities.
        """
        
        for bullet in world.bullets:
            if bullet.health <= 0:
                world.remove_bullet(bullet)
            elif not BoundariesHandler.is_entity_within_world_boundaries(bullet):
                world.remove_bullet(bullet)

            if isinstance(bullet, IDespawnable):
                if bullet.can_despawn:
                    world.remove_bullet(bullet)

        for item in world.items:
            if isinstance(item, IDespawnable):
                if item.can_despawn:
                    world.remove_item(item)

        for monster in world.monsters:
            if monster.health <= 0:
                if isinstance(monster, BossMonster) or isinstance(monster, BigBossMonster):
                    ItemFactory.create_item(ItemFactory.RED_GEM, monster, world, xp_amount=100)

                elif isinstance(monster, Monster):
                    random_number = random.randint(1,100) 
                    if random_number in range(1, 70):
                        ItemFactory.create_item(ItemFactory.COMMON_GEM, monster, world, xp_amount=1)

                    elif random_number in range(70, 80):
                        ItemFactory.create_item(ItemFactory.GREEN_GEM, monster, world, xp_amount=3)

                    elif random_number in range(80, 85):
                        ItemFactory.create_item(ItemFactory.BLUE_GEM, monster, world, xp_amount=5)

                    elif random_number == 100:
                        ItemFactory.create_item(ItemFactory.GUAYMALLEN, monster, world)

                world.remove_monster(monster)
                    
            elif not BoundariesHandler.is_entity_within_world_boundaries(monster):
                world.remove_monster(monster)

        if world.player.health <= 0:
            raise DeadPlayerException
