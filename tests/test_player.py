import unittest
from unittest.mock import MagicMock, patch
from business.entities.items.experience_gem import IExperienceGem
from business.entities.items.guaymallen import Guaymallen
from business.world.interfaces import IGameWorld
from business.upgrades.perks import DamageMultiplierPerk, SpeedPerk
from presentation.sprite import Sprite
from business.handlers.cooldown_handler import CooldownHandler
from business.entities.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.sprite_mock = MagicMock(spec=Sprite)
        self.player = Player(pos_x=0, pos_y=0, sprite=self.sprite_mock)

    def test_move(self):
        initial_x = self.player._pos_x
        initial_y = self.player._pos_y
        self.player.move(1, 0)
        self.assertNotEqual(self.player._pos_x, initial_x)
        self.assertEqual(self.player._pos_y, initial_y)

        self.player.move(0, 1)
        self.assertNotEqual(self.player._pos_y, initial_y)

    def test_gain_experience(self):
        world_mock = MagicMock(spec=IGameWorld)

        self.player._Player__gain_experience(1, world_mock)
        self.assertEqual(self.player.experience, 1)

    def test_level_up_by_gaining_experience(self):
        world_mock = MagicMock(spec=IGameWorld)
        initial_level = self.player.level

        self.player._Player__gain_experience(1000, world_mock)
        self.assertGreater(self.player.level, initial_level)

    def test_pickup_item(self):
        world_mock = MagicMock(spec=IGameWorld)
        experience_gem = MagicMock(spec=IExperienceGem)
        experience_gem.amount = 10

        self.player.pickup_item(experience_gem, world_mock)
        self.assertGreater(self.player.experience, 0)

    def test_pickup_guaymallen_and_heal(self):
        world_mock = MagicMock(spec=IGameWorld)

        guaymallen_mock = MagicMock(spec=Guaymallen)
        self.player.take_damage(20)
        self.player.pickup_item(guaymallen_mock, world_mock)
        self.assertGreater(self.player.health, 80)

    def test_handle_perk(self):
        perk_mock = MagicMock(spec=DamageMultiplierPerk)
        perk_mock.upgrade_amount.return_value = 0.5

        self.player.handle_perk(perk_mock)
        self.assertIn(perk_mock, self.player.inventory)

        self.assertEqual(self.player.damage_multiplier, 1.5)

        speed_perk = MagicMock(spec=SpeedPerk)
        speed_perk.upgrade_amount.return_value = 0.2
        self.player.handle_perk(speed_perk)
        self.assertEqual(self.player.speed_multiplier, 1.2)

    def test_take_damage(self):
        initial_health = self.player.health
        self.player.take_damage(20)
        self.assertEqual(self.player.health, initial_health - 20)

    def test_heal(self):
        self.player.take_damage(20)
        initial_health = self.player.health
        self.player.heal(10)
        self.assertEqual(self.player.health, initial_health + 10)

        self.player.heal(100)
        self.assertEqual(self.player.health, self.player.max_health)

    def test_experience_progress(self):
        self.player._Player__experience = 1
        expected_progress = self.player.experience / self.player.experience_to_next_level
        self.assertEqual(self.player.experience_progress, expected_progress)

if __name__ == '__main__':
    unittest.main()