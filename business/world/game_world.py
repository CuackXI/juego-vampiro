"""This module contains the implementation of the game world."""

from business.entities.interfaces import IBullet, IExperienceGem, IMonster, IPlayer
from business.world.interfaces import IGameWorld, IMonsterSpawner, ITileMap
from business.entities.perks import *
from business.entities.bullet_factory import *

class GameWorld(IGameWorld):
    """Represents the game world."""

    def __init__(self, spawner: IMonsterSpawner, tile_map: ITileMap, player: IPlayer):
        # Initialize the player and lists for monsters, bullets and gems
        self.__player: IPlayer = player
        self.__monsters: list[IMonster] = []
        self.__bullets: list[IBullet] = []
        self.__experience_gems: list[IExperienceGem] = []
        self.__in_upgrade = False

        self.__perks: list[IPerk] = []

        self.__initialize_perks()

        # Initialize the tile map
        self.tile_map: ITileMap = tile_map

        # Initialize the monster spawner
        self.__monster_spawner: IMonsterSpawner = spawner

    def __initialize_perks(self):
        self.PERKS_U = [NormalBulletFactory(self.__player), TurretBulletFactory(self.__player)]
        self.PERKS_S = [RegenerationPerk(), MaxHealthPerk(), DamageMultiplierPerk()]

        for perk in self.PERKS_S:
            self.__perks.append(perk)
        for perk in self.PERKS_U:
            self.__perks.append(perk)

        self.__player.handle_perk(NormalBulletFactory(self))

    def get_perks(self):
        usable_perks: list = self.__perks

        for perk in self.__perks:
            if not perk.upgradable:
                usable_perks.remove(perk)

        return usable_perks

    def give_perk_to_player(self, perk):
        """ESTO DEBERIA SER TEMPORAL PERO ES PARA PROBAR ALGO"""
        self.__player.handle_perk(perk)

    def update(self):
        self.player.update(self)

        self.__monster_spawner.update(self)

        for bullet in self.bullets:
            bullet.update(self)

        for monster in self.monsters:
            monster.update(self)

        for gem in self.experience_gems:
            gem.update(self)

    def add_monster(self, monster: IMonster):
        self.__monsters.append(monster)

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

    def activate_upgrade(self):
        self.__in_upgrade = True

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

    @property
    def in_upgrade(self):
        return self.__in_upgrade