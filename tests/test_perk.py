import unittest
from unittest.mock import Mock, patch
from business.entities.interfaces import IPlayer
from business.upgrades.perks import RegenerationPerk
import pygame

class TestRegenerationPerk(unittest.TestCase):

    @patch('pygame.image.load')
    def setUp(self, mock_load):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

        mock_surface = pygame.Surface((1, 1))
        mock_load.return_value = mock_surface

        self.mock_player = Mock(spec=IPlayer)
        self.mock_player.inventory = []
        self.perk = RegenerationPerk(self.mock_player)

    def tearDown(self):
        pygame.display.quit()
        pygame.quit()

    def test_initial_values(self):
        self.assertEqual(self.perk.level, 1)
        self.assertEqual(self.perk.upgrade_amount(), 1)
        self.assertTrue(self.perk.upgradable)

    def test_upgrade_functionality(self):
        self.perk.upgrade()
        self.assertEqual(self.perk.level, 2)
        self.assertEqual(self.perk.upgrade_amount(), 2)

    def test_upgrade_to_max_level(self):
        max_level = max(RegenerationPerk.BASE_LEVEL_STATS.keys())
        while self.perk.upgradable:
            self.perk.upgrade()
        self.assertEqual(self.perk.level, max_level)
        self.assertFalse(self.perk.upgradable)

    def test_to_json(self):
        self.assertEqual(self.perk.to_json(), {'level': 1})
        self.perk.upgrade()
        self.assertEqual(self.perk.to_json(), {'level': 2})

    def test_string_representation(self):
        self.assertEqual(str(self.perk), 'AUMENTO DE REGENERACIÓN: 1')
        self.mock_player.inventory.append(self.perk)
        self.assertEqual(str(self.perk), 'AUMENTO DE REGENERACIÓN: 2 -> NIVEL 2')

if __name__ == '__main__':
    unittest.main()