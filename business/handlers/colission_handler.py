"""Module for the CollisionHandler class."""

from typing import List

from business.entities.interfaces import IBullet, IItem, IHasSprite, IMonster, IPlayer
from business.world.interfaces import IGameWorld
from business.entities.monsters.interfaces import IMonsterBullet

class CollisionHandler:
    """Handles collisions between entities in the game world."""

    @staticmethod
    def __collides_with(an_entity: IHasSprite, another_entity: IHasSprite):
        return an_entity.sprite.rect.colliderect(another_entity.sprite.rect)

    @staticmethod
    def __handle_bullets(bullets: list[IBullet], monsters: list[IMonster], player: IPlayer):
        """Handles bullet collisions with the monsters and the player."""
        for bullet in bullets:
            for monster in monsters:
                if CollisionHandler.__collides_with(bullet, monster) and not isinstance(bullet, IMonsterBullet):
                    monster.take_damage(bullet.damage_amount)
                    bullet.take_damage(bullet.damage_amount)
            if CollisionHandler.__collides_with(bullet, player) and isinstance(bullet, IMonsterBullet):
                player.take_damage(bullet.damage_amount)
                bullet.take_damage(bullet.damage_amount)

    @staticmethod
    def __handle_items(items: list[IItem], player: IPlayer, world: IGameWorld):
        """Handles items collisions with the player."""
        for item in items:
            if item.in_player_range(player):
                player.pickup_item(item, world)
                world.remove_item(item)
        
    @staticmethod
    def handle_collisions(world: IGameWorld):
        """Handles collisions between entities in the game world.

        Args:
            world (IGameWorld): The game world.
        """
        CollisionHandler.__handle_bullets(world.bullets, world.monsters, world.player)
        CollisionHandler.__handle_items(world.items, world.player, world)
