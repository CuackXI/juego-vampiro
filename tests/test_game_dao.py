import unittest
import tempfile
import json
import pygame
from unittest.mock import Mock, patch
from business.upgrades.perks import RegenerationPerk
from business.upgrades.bullet_factories import NormalBulletFactory
from persistence.gamedao import GameJSONDAO
from business.entities.monsters.monster import Monster
from business.entities.bullets import NormalBullet
from business.entities.items.experience_gem import ExperienceGem
from business.entities.player import Player
from presentation.sprite import Sprite
from business.handlers.clock import GameClockSingleton
import os

class TestGameJSONDAO(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()

        self.dao = GameJSONDAO(json_path=self.temp_file.name)

    def tearDown(self):
        pygame.display.quit()
        pygame.quit()
        os.remove(self.temp_file.name)

    def test_save_game_creates_data(self):
        monster = Monster(10, 20)
        monster._Monster__health = 10

        bullet = NormalBullet(15, 25, 0, 0, 0, 0, 10)
        bullet._NormalBullet__health = 5
        bullet.__damage = 10

        item = ExperienceGem(30, 40, 1)
        item.__amount = 1

        player = Player(50, 60, Mock(spec=Sprite))
        player._Player__experience = 100
        player._Player__level = 5
        player._Player__health = 80
        
        regeneration_perk = RegenerationPerk(player)
        regeneration_perk._RegenerationPerk__level = 2

        bullet_factory = NormalBulletFactory(player)
        bullet_factory._NormalBulletFactory__level = 3

        player.__static_inventory = [regeneration_perk]
        player.__updatable_inventory = [bullet_factory]
        player.to_json = Mock(return_value={
            'pos_x': player._pos_x,
            'pos_y': player._pos_y,
            'experience': player._Player__experience,
            'level': player._Player__level,
            'health': player._Player__health,
            'health_regen_cooldown': player._Player__health_regen_cooldown.last_action_time,
            'static': {str(type(perk)): perk.to_json() for perk in player.__static_inventory},
            'updatable': {str(type(perk)): perk.to_json() for perk in player.__updatable_inventory},
        })

        monster_spawner = Mock()
        monster_spawner.__minute_boss_added = 10
        monster_spawner.__second_minute_boss_added = 20
        monster_spawner.to_json = Mock(return_value={
            'minute_boss_added': monster_spawner.__minute_boss_added,
            'second_minute_boss_added': monster_spawner.__second_minute_boss_added
        })

        game = Mock()
        game.world.monsters = [monster]
        game.world.bullets = [bullet]
        game.world.items = [item]
        game.world.player = player
        game.world.monster_spawner = monster_spawner

        self.dao.save_game(game)

        with open(self.temp_file.name, 'r', encoding="utf-8") as file:
            saved_data = json.load(file)

        self.assertIn('monsters', saved_data)
        self.assertIn('bullets', saved_data)
        self.assertIn('items', saved_data)
        self.assertIn('player', saved_data)
        self.assertIn('monster_spawner', saved_data)
        self.assertIn('clock', saved_data)

        self.assertEqual(saved_data['monsters'][str(type(monster))][0], {
            'pos_x': monster.pos_x,
            'pos_y': monster.pos_y,
            'health': monster.health,
            'attack_cooldown': monster._Monster__attack_cooldown.last_action_time
        })

        self.assertEqual(saved_data['bullets'][str(type(bullet))][0], {
            'pos_x': bullet.pos_x,
            'pos_y': bullet.pos_y,
            'dir_x': bullet._NormalBullet__dir_x,
            'dir_y': bullet._NormalBullet__dir_y,
            'damage': bullet.damage_amount,
            'health': bullet.health,
            'speed': bullet.speed
        })

        self.assertEqual(saved_data['items'][str(type(item))][0], {
            'pos_x': item.pos_x,
            'pos_y': item.pos_y,
            'amount': item.amount,
            'despawn_cooldown': item._ExperienceGem__despawn_cooldown.last_action_time
        })

        self.assertEqual(saved_data['player'], {
            'pos_x': player.pos_x,
            'pos_y': player.pos_y,
            'experience': player.experience,
            'level': player.level,
            'health': player.health,
            'health_regen_cooldown': player._Player__health_regen_cooldown.last_action_time,
            'static': {'<class \'business.upgrades.perks.RegenerationPerk\'>': {'level': regeneration_perk.level}},
            'updatable': {'<class \'business.upgrades.bullet_factories.NormalBulletFactory\'>': {'level': bullet_factory.level, 
                                                                                                 'attack_cooldown': bullet_factory._NormalBulletFactory__cooldown_handler.last_action_time}},
        })

        self.assertEqual(saved_data['monster_spawner'], {
            'minute_boss_added': monster_spawner.__minute_boss_added,
            'second_minute_boss_added': monster_spawner.__second_minute_boss_added
        })

        self.assertEqual(saved_data['clock'], GameClockSingleton().game_clock)

    def test_load_game_returns_data(self):
        initial_data = {
            'monsters': {},
            'bullets': {},
            'items': {},
            'player': {},
            'monster_spawner': {},
            'clock': 0
        }
        self.dao._GameJSONDAO__save_data(initial_data)

        loaded_data = self.dao.load_game()

        self.assertEqual(loaded_data, initial_data)

    def test_clear_save(self):
        initial_data = {
            'monsters': {},
            'bullets': {},
            'items': {},
            'player': {},
            'monster_spawner': {},
            'clock': 0
        }
        self.dao._GameJSONDAO__save_data(initial_data)

        self.dao.clear_save()

        cleared_data = self.dao.load_game()

        self.assertEqual(cleared_data, GameJSONDAO.BASE_GAME_DATA)

if __name__ == '__main__':
    unittest.main()
