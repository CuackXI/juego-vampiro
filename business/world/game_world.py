"""This module contains the implementation of the game world."""

import random
from business.entities.interfaces import IBullet, IExperienceGem, IMonster, IPlayer
from business.world.interfaces import IGameWorld, IMonsterSpawner, ITileMap
from business.entities.perks import *
from business.entities.bullet_factory import *
from business.handlers.boundaries_handler import BoundariesHandler
from business.exceptions import * 
from presentation.interfaces import IDisplay

class GameWorld(IGameWorld):
    """Represents the game world."""

    def __init__(self, spawner: IMonsterSpawner, tile_map: ITileMap, player: IPlayer, display: IDisplay):
        # Initialize the player and lists for monsters, bullets and gems
        self.__player: IPlayer = player
        self.__monsters: list[IMonster] = []
        self.__bullets: list[IBullet] = []
        self.__experience_gems: list[IExperienceGem] = []
        self.in_upgrade = False
        self.__game = None
        self.__current_upgrade_type = None
        self.display = display

        self.__perks: list[IPerk] = []

        # Initialize the tile map
        self.tile_map: ITileMap = tile_map

        # Initialize the monster spawner
        self.monster_spawner: IMonsterSpawner = spawner

    def __initialize_perks(self):
        initial_perk = NormalBulletFactory(self.__player, self.__game)

        self.PERKS_U = [initial_perk, TurretBulletFactory(self.__player, self.__game)]
        self.PERKS_S = [RegenerationPerk(self.__player), MaxHealthPerk(self.__player), DamageMultiplierPerk(self.__player)]

        for perk in self.PERKS_S:
            self.__perks.append(perk)
        for perk in self.PERKS_U:
            self.__perks.append(perk)

        self.__player.handle_perk(initial_perk)

    def load_game(self, game):
        self.__game = game
        self.__initialize_perks()

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
        """ESTO DEBERIA SER TEMPORAL PERO ES PARA PROBAR ALGO"""
        self.__player.handle_perk(perk)

    def update(self):
        self.player.update(self)

        self.monster_spawner.update(self)

        for bullet in self.bullets:
            bullet.update(self)

        for monster in self.monsters:
            monster.update(self)

        for gem in self.experience_gems:
            gem.update(self)

    def activate_upgrade(self):
        self.in_upgrade = True

    def add_monster(self, monster: IMonster):
        if BoundariesHandler.is_entity_within_world_boundaries(monster):
            self.__monsters.append(monster)
        else:
            raise EntityOutOfBounds

    def remove_monster(self, monster: IMonster):
        self.__monsters.remove(monster)

    def add_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.append(gem)

    def remove_experience_gem(self, gem: IExperienceGem):
        self.__experience_gems.remove(gem)

    def add_bullet(self, bullet: IBullet):
        self.__bullets.append(bullet)

    def remove_bullet(self, bullet: IBullet):
        self.__bullets.remove(bullet)

    @property
    def game(self):
        return self.__game

    @property
    def current_upgrade(self):
        return self.__current_upgrade_type

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
    def experience_gems(self) -> list[IExperienceGem]:
        return self.__experience_gems[:]