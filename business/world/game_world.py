"""This module contains the implementation of the game world."""

import random
from business.entities.interfaces import IBullet, IMonster, IPlayer, IItem
from business.world.interfaces import IGameWorld, IMonsterSpawner, ITileMap
from business.upgrades.interfaces import *
from business.upgrades.perks import *
from business.upgrades.bullet_factories import *
from business.entities.bullets import *
from business.handlers.boundaries_handler import BoundariesHandler
from business.exceptions import * 
from presentation.interfaces import IDisplay
from business.entities.items.experience_gem import *
from business.entities.monsters.upgrades.bullet_factory import MonsterBulletFactory
from business.entities.items.item_factory import ItemFactory

class GameWorld(IGameWorld):
    """Represents the game world."""

    def __init__(self, spawner: IMonsterSpawner, tile_map: ITileMap, player: IPlayer, display: IDisplay, saved_data: dict | None = None):
        self.__player: IPlayer = player
        self.__monsters: list[IMonster] = []
        self.__bullets: list[IBullet] = []
        self.__items: list[IItem] = []
        self.__in_upgrade = 0
        self.__game = None
        self.__display = display

        self.PERKS_U = []
        self.PERKS_S = []
        self.__perks: list[IPerk] = []

        # Initialize the tile map
        self.tile_map: ITileMap = tile_map

        # Initialize the monster spawner
        self.__monster_spawner = spawner

        if saved_data:
            self.__load_saved_data(saved_data)
            self.__initialize_perks(saved_data = saved_data)
        else:
            self.__initialize_perks()

    def __load_saved_data(self, saved_data: dict):
        """Loads saved data from the data file."""
        self.monster_spawner.load_saved_data(self, saved_data)

        self.__load_bullets(saved_data)
        self.__load_items(saved_data)

    def __initialize_perks(self, saved_data: dict | None = None):
        """Initialize perk's instances."""
        self.PERKS_U: list[IBulletFactory] = [NormalBulletFactory(self.__player), TurretBulletFactory(self.__player), FollowingBulletFactory(self.__player)]
        self.PERKS_S: list[IPerk] = [RegenerationPerk(self.__player), MaxHealthPerk(self.__player), DamageMultiplierPerk(self.__player), SpeedPerk(self.__player)]

        for perk in self.PERKS_S:
            self.__perks.append(perk)
        for perk in self.PERKS_U:
            self.__perks.append(perk)

        if saved_data is not None:
            player = saved_data.get('player')

            # Load static perks
            for perk_type in player['static']:
                for perk in self.PERKS_S:
                    if perk_type == str(type(perk)):
                        for _ in range(player['static'][perk_type]['level']):
                            self.give_perk_to_player(perk)

            # Load updatable perks
            for perk_type in player['updatable']:
                for perk in self.PERKS_U:
                    if perk_type == str(type(perk)):
                        for _ in range(player['updatable'][perk_type]['level']):
                            self.give_perk_to_player(perk)
                            perk.load_cooldown(player['updatable'][perk_type]['attack_cooldown'])
        else:
            # NormalBulletFactory - INITIAL PERK
            self.__player.handle_perk(self.PERKS_U[0])

    def __load_bullets(self, saved_data: dict):
        """Loads the bullets giving the saved data to the bullet factories."""
        saved_data = saved_data.get('bullets')

        for bullet_type in saved_data:
            if 'NormalBullet' in bullet_type:
                NormalBulletFactory(self.__player).load_bullets(saved_data[bullet_type], self)

            if 'Turret' in bullet_type:
                TurretBulletFactory(self.__player).load_bullets(saved_data[bullet_type], self)

            if 'FollowingBullet' in bullet_type:
                FollowingBulletFactory(self.__player).load_bullets(saved_data[bullet_type], self)

            if 'MonsterBullet' in bullet_type:
                MonsterBulletFactory().load_bullets(saved_data[bullet_type], self)

    def __load_items(self, saved_data: dict):
        """Loads the items from the saved data."""
        ItemFactory.load_items(self, saved_data)

    def get_perks_for_display(self):
        amount = 3

        usable_perks = [perk for perk in self.__perks if perk.upgradable]

        for i in range(amount + 1):
            try:
                random_perks = random.sample(usable_perks, i)
            except:
                break

        return random_perks

    def give_perk_to_player(self, perk):
        self.__player.handle_perk(perk)

    def update(self):
        self.player.update(self)

        self.monster_spawner.update(self)

        for bullet in self.bullets:
            bullet.update(self)

        for monster in self.monsters:
            monster.update(self)

        for item in self.items:
            item.update(self)

    def activate_upgrade(self, upgrades):
        self.__in_upgrade = upgrades

    def add_monster(self, monster: IMonster):
        if BoundariesHandler.is_entity_within_world_boundaries(monster):
            self.__monsters.append(monster)
        else:
            raise EntityOutOfBounds

    def remove_monster(self, monster: IMonster):
        self.__monsters.remove(monster)

    def add_item(self, item):
        self.__items.append(item)

    def remove_item(self, item):
        self.__items.remove(item)

    def add_bullet(self, bullet: IBullet):
        self.__bullets.append(bullet)

    def remove_bullet(self, bullet: IBullet):
        self.__bullets.remove(bullet)

    @property
    def monster_spawner(self):
        return self.__monster_spawner

    @property
    def display(self):
        return self.__display

    @property
    def in_upgrade(self):
        return self.__in_upgrade
    
    @in_upgrade.setter
    def in_upgrade(self, value):
        self.__in_upgrade = value

    @property
    def game(self):
        return self.__game

    @property
    def player(self) -> IPlayer:
        return self.__player

    @property
    def monsters(self) -> list[IMonster]:
        return self.__monsters[:]

    @property
    def bullets(self) -> list[IBullet]:
        return self.__bullets[:]

    @property
    def items(self) -> list[IItem]:
        return self.__items[:]