import unittest
from unittest.mock import Mock, patch
from business.handlers.death_handler import DeathHandler
from business.exceptions import DeadPlayerException
from business.entities.monsters.monster import Monster
from business.entities.monsters.boss import BossMonster
from business.entities.items.item_factory import ItemFactory
from business.entities.items.experience_gem import ExperienceGem
from business.entities.bullets import NormalBullet
from unittest.mock import PropertyMock
import pygame

class TestDeathHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.world = Mock()
        self.bullet = NormalBullet(0, 0, 0, 0, 0, 0, 10)
        self.item = ExperienceGem(0, 0, 0)

        self.monster = Monster(0, 0)
        self.monster._Monster__health = 10
        self.boss_monster = BossMonster(0, 0)
        self.boss_monster._BossMonster__health = 20
        
        self.world.bullets = [self.bullet]
        self.world.items = [self.item]
        self.world.monsters = [self.monster, self.boss_monster]
        self.world.player.health = 100

    def test_remove_bullet_when_health_zero(self):
        self.bullet._NormalBullet__health = 0
        DeathHandler.check_deaths(self.world)
        self.world.remove_bullet.assert_called_once_with(self.bullet)

    @patch('business.handlers.boundaries_handler.BoundariesHandler.is_entity_within_world_boundaries', return_value=False)
    def test_remove_bullet_when_out_of_bounds(self, mock_is_within_bounds):
        self.bullet._NormalBullet__health = 10
        self.bullet.can_despawn = False
        DeathHandler.check_deaths(self.world)
        self.world.remove_bullet.assert_called_once_with(self.bullet)

    @patch.object(ExperienceGem, 'can_despawn', new_callable=PropertyMock)
    def test_remove_item_when_can_despawn(self, mock_can_despawn):
        mock_can_despawn.return_value = True
        self.item._ExperienceGem__despawn_cooldown.last_action_time = 0
        DeathHandler.check_deaths(self.world)
        self.world.remove_item.assert_called_once_with(self.item)

    def test_remove_monster_when_health_zero(self):
        self.monster._Monster__health = 0
        DeathHandler.check_deaths(self.world)
        self.world.remove_monster.assert_called()

    @patch('business.handlers.boundaries_handler.BoundariesHandler.is_entity_within_world_boundaries')
    def test_monster_out_of_bounds(self, mock_is_within_bounds):
        def side_effect(arg):
            return arg != self.monster

        mock_is_within_bounds.side_effect = side_effect
        
        self.monster._Monster__health = 10

        DeathHandler.check_deaths(self.world)

        self.world.remove_monster.assert_called_once_with(self.monster)

    def test_player_death_raises_exception(self):
        self.world.player.health = 0
        with self.assertRaises(DeadPlayerException):
            DeathHandler.check_deaths(self.world)

if __name__ == '__main__':
    unittest.main()