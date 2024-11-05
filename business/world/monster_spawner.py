"""This module contains the MonsterSpawner class."""

import random

import pygame

from business.entities.interfaces import *
from business.entities.monsters.gunner import GunMonster
from business.entities.monsters.monster import Monster
from business.entities.monsters.boss import BossMonster
from business.entities.monsters.boss2 import BigBossMonster
from business.world.interfaces import IGameWorld, IMonsterSpawner
from presentation.interfaces import IDisplay
from business.handlers.cooldown_handler import CooldownHandler
from business.exceptions import EntityOutOfBounds
from business.handlers.clock import GameClockSingleton

class MonsterSpawner(IMonsterSpawner):
    """Spawns monsters in the game world."""

    BASE_DELAY = 100

    def __init__(self, display: IDisplay):
        self.__display = display

        self.__monsters: list[IMonster] = [Monster, GunMonster]
        self.__bosses: list[IMonster] = [BossMonster, BigBossMonster]
        
        self.__minute_boss_added = False
        self.__second_minute_boss_added = False

        self.__spawn_cooldown = CooldownHandler(MonsterSpawner.BASE_DELAY)

    def load_saved_data(self, world: IGameWorld, saved_data: dict):
        mosnters_data = saved_data.get('monsters')

        for monster_type in mosnters_data:
            for monster_data in mosnters_data[monster_type]:
                if 'monster.Monster' in monster_type:
                    monster = Monster(0, 0, monster_data)
                    world.add_monster(monster)
                elif 'boss.BossMonster' in monster_type:
                    monster = BossMonster(0, 0, monster_data)
                    world.add_monster(monster)
                elif 'boss2.BigBossMonster' in monster_type:
                    monster = BigBossMonster(0, 0, monster_data)
                    world.add_monster(monster)
                elif 'Gun' in monster_type:
                    monster = GunMonster(0, 0, monster_data)
                    world.add_monster(monster)

        self.__minute_boss_added = saved_data['monster_spawner']['minute_boss_added']
        self.__second_minute_boss_added = saved_data['monster_spawner']['second_minute_boss_added']

    def to_json(self):
        return {
            'minute_boss_added': self.__minute_boss_added,
            'second_minute_boss_added': self.__second_minute_boss_added
        }

    def update(self, world: IGameWorld):
        if self.__spawn_cooldown.is_action_ready() and len(world.monsters) <= 20:
            self.spawn_monster(world)
            self.__spawn_cooldown.put_on_cooldown()

    def spawn_monster(self, world: IGameWorld):
        while True:
            try:
                camera_left = self.__display.camera.camera_rect.left
                camera_right = self.__display.camera.camera_rect.right
                camera_top = self.__display.camera.camera_rect.top
                camera_bottom = self.__display.camera.camera_rect.bottom

                edge = random.choice(['top', 'bottom', 'left', 'right'])

                if edge == 'top':
                    pos_x = random.randint(camera_left, camera_right)
                    pos_y = camera_top
                elif edge == 'bottom':
                    pos_x = random.randint(camera_left, camera_right)
                    pos_y = camera_bottom
                elif edge == 'left':
                    pos_x = camera_left
                    pos_y = random.randint(camera_top, camera_bottom)
                else:  # 'right'
                    pos_x = camera_right
                    pos_y = random.randint(camera_top, camera_bottom)

                monster_choice = random.randint(1, 100)
                if monster_choice >= 85:
                    monster_choice = 1
                else:
                    monster_choice = 0
                monster = self.__monsters[monster_choice]
                world.add_monster(monster(pos_x, pos_y))

                if GameClockSingleton().game_clock > 60000 and not self.__minute_boss_added:
                    world.add_monster(BossMonster(pos_x, pos_y))
                    self.__minute_boss_added = True

                if GameClockSingleton().game_clock > 120000 and not self.__second_minute_boss_added :
                    world.add_monster(BigBossMonster(pos_x, pos_y))
                    self.__second_minute_boss_added = True

                break
            except EntityOutOfBounds:
                pass