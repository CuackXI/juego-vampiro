"""Module that contains the DeathHandler class."""

from business.entities.items.experience_gem import ExperienceGem
from business.entities.items.guaymallen import Guaymallen
from business.exceptions import DeadPlayerException
from business.world.interfaces import IGameWorld
from business.handlers.boundaries_handler import BoundariesHandler
from business.entities.interfaces import IDespawnable
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

        for monster in world.monsters:
            if monster.health <= 0:
                random_number = random.randint(1,100) 
                if random_number in range(1, 50):
                    world.add_item(ExperienceGem(monster.pos_x, monster.pos_y, 1))
                elif random_number == 100:
                    world.add_item(Guaymallen(monster.pos_x, monster.pos_y))
                world.remove_monster(monster)
                
            elif not BoundariesHandler.is_entity_within_world_boundaries(monster):
                world.remove_monster(monster)

        for item in world.items:
            if isinstance(item, IDespawnable):
                if item.can_despawn:
                    world.remove_item(item)

        if world.player.health <= 0:
            raise DeadPlayerException
