"""Module that contains the DeathHandler class."""

from business.entities.experience_gem import ExperienceGem
from business.exceptions import DeadPlayerException
from business.world.interfaces import IGameWorld
from business.handlers.boundaries_handler import BoundariesHandler
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

        for monster in world.monsters:
            if monster.health <= 0:
                if random.randint(1,2) == 2:
                    world.add_item(ExperienceGem(monster.pos_x, monster.pos_y, 1))
                world.remove_monster(monster)
                
            elif not BoundariesHandler.is_entity_within_world_boundaries(monster):
                world.remove_monster(monster)

        if world.player.health <= 0:
            raise DeadPlayerException
