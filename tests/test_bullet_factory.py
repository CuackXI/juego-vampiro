import unittest
from unittest.mock import Mock
from business.entities.interfaces import IPlayer
from business.upgrades.bullet_factories import NormalBulletFactory
import pygame
from unittest.mock import patch, Mock

class TestNormalBulletFactory(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

        self.player = Mock(spec=IPlayer)
        self.player.damage_multiplier = 1.0
        self.player.pos_x = 0
        self.player.pos_y = 0
        self.player.inventory = []

        self.world = Mock()
        self.world.monsters = []

        self.bullet_factory = NormalBulletFactory(self.player)
    
    def tearDown(self):
        pygame.quit()

    def test_initial_level(self):
        self.assertEqual(self.bullet_factory.level, 1)
        self.assertEqual(self.bullet_factory.cooldown, 1000)
        self.assertEqual(self.bullet_factory.damage, 5)
        self.assertEqual(self.bullet_factory.speed, 4)
        self.assertEqual(self.bullet_factory.health, 50)

    def test_upgrade(self):
        self.bullet_factory.upgrade()
        self.assertEqual(self.bullet_factory.level, 2)
        self.assertEqual(self.bullet_factory.cooldown, 937)
        self.assertEqual(self.bullet_factory.damage, 10)

    @patch('business.upgrades.bullet_factories.NormalBullet')
    def test_create_bullet(self, MockBullet):
        self.world.player = Mock()
        self.world.player.pos_x = 0
        self.world.player.pos_y = 0

        monster = Mock()
        monster.pos_x = 5
        monster.pos_y = 5
        self.world.monsters.append(monster)

        mock_bullet_instance = Mock()
        mock_bullet_instance.speed = self.bullet_factory.speed
        mock_bullet_instance.damage = self.bullet_factory.damage
        mock_bullet_instance.health = self.bullet_factory.health
        MockBullet.return_value = mock_bullet_instance

        self.bullet_factory.create_bullet(self.world)
        self.world.add_bullet.assert_called_once_with(mock_bullet_instance)

        bullet = self.world.add_bullet.call_args[0][0]
        self.assertEqual(bullet.speed, self.bullet_factory.speed)
        self.assertEqual(bullet.damage, self.bullet_factory.damage)
        self.assertEqual(bullet.health, self.bullet_factory.health)

    def test_update_with_cooldown(self):
        self.world.player = Mock()
        self.world.player.pos_x = 0
        self.world.player.pos_y = 0

        monster = Mock()
        monster.pos_x = 5
        monster.pos_y = 5
        self.world.monsters.append(monster)

        self.bullet_factory.update(self.world)
        self.world.add_bullet.assert_not_called()

        self.bullet_factory.load_cooldown(-1000)
        self.bullet_factory.update(self.world)
        self.world.add_bullet.assert_called_once()

    def test_to_json(self):
        self.bullet_factory.load_cooldown(500)
        json_data = self.bullet_factory.to_json()
        self.assertEqual(json_data, {'level': 1, 'attack_cooldown': 500})

    def test_upgradable_property(self):
        self.assertTrue(self.bullet_factory.upgradable)
        for _ in range(max(NormalBulletFactory.BASE_LEVEL_STATS.keys()) - 1):
            self.bullet_factory.upgrade()
        self.assertFalse(self.bullet_factory.upgradable)

if __name__ == "__main__":
    unittest.main()
