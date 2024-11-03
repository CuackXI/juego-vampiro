"""Module for the CollisionHandler class."""

from typing import List

from business.entities.interfaces import IBullet, IItem, IHasSprite, IMonster, IPlayer
from business.world.interfaces import IGameWorld


class CollisionHandler:
    """Handles collisions between entities in the game world."""

    @staticmethod
    def __collides_with(an_entity: IHasSprite, another_entity: IHasSprite):
        return an_entity.sprite.rect.colliderect(another_entity.sprite.rect)

    @staticmethod
    def __handle_bullets(bullets: List[IBullet], monsters: List[IMonster]):
        for bullet in bullets:
            for monster in monsters:
                if CollisionHandler.__collides_with(bullet, monster):
                    monster.take_damage(bullet.damage_amount)
                    bullet.take_damage(bullet.damage_amount)

    @staticmethod
    def __handle_monsters(monsters: List[IMonster], player: IPlayer):
        pass

    @staticmethod
    def __handle_items(items: List[IItem], player: IPlayer, world: IGameWorld):
        for item in items:
            if item.in_player_range(player):
                player.pickup_gem(item, world)
                world.remove_item(item)
        
    @staticmethod
    def handle_collisions(world: IGameWorld):
        """Handles collisions between entities in the game world.

        Args:
            world (IGameWorld): The game world.
        """
        CollisionHandler.__handle_bullets(world.bullets, world.monsters)
        CollisionHandler.__handle_monsters(world.monsters, world.player)
        CollisionHandler.__handle_items(world.items, world.player, world)
