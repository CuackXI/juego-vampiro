import unittest
from unittest.mock import MagicMock, patch
import pygame

from business.entities.interfaces import IDamageable, IHasPosition
from business.entities.monsters.monster import Monster


class TestMonster(unittest.TestCase):
    def setUp(self):
        pygame.display.init()
        pygame.display.set_mode((800, 600))
        self.monster = Monster(5, 5, MagicMock())

    def tearDown(self):
        pygame.display.quit()

    def test_attack_deals_damage_and_target_takes_damage(self):
        target_mock = MagicMock(spec=IDamageable)
        target_mock.health = 10
        target_mock.pos_x = 2
        target_mock.pos_y = 3

        with patch.object(
            self.monster._Monster__attack_cooldown,  # pylint: disable=W0212
            "is_action_ready",
            return_value=True,
        ):
            with patch.object(self.monster, '_get_distance_to', return_value=30):
                self.monster.attack(target_mock)

        target_mock.take_damage.assert_called_once_with(self.monster.damage_amount)

    def test_convert_data_to_json(self):
        data_to_save = ['pos_x', 'pos_y', 'health','attack_cooldown']

        result = self.monster.to_json()
        for element in result:
            self.assertTrue(element in data_to_save)
    
    def test_attack_is_not_called_when_action_is_not_ready(self):
        target_mock = MagicMock(spec=IDamageable)
        target_mock.health = 10

        with patch.object(
            self.monster._Monster__attack_cooldown,  # pylint: disable=W0212
            "is_action_ready",
            return_value=False,
        ):
            self.monster.attack(target_mock)

        target_mock.take_damage.assert_not_called()
