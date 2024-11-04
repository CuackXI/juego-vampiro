import unittest
from unittest.mock import patch
from business.handlers.cooldown_handler import CooldownHandler
from business.handlers.clock import GameClockSingleton

class TestCooldownHandler(unittest.TestCase):

    def setUp(self):
        self.mock_game_clock = GameClockSingleton()
        self.mock_game_clock._GameClockSingleton__game_clock = 0
        self.cooldown_time = 5000
        self.cooldown_handler = CooldownHandler(self.cooldown_time)

    def test_initial_action_not_ready(self):
        self.mock_game_clock._GameClockSingleton__game_clock = 0
        self.assertFalse(self.cooldown_handler.is_action_ready())

    def test_action_ready_after_cooldown(self):
        self.cooldown_handler.put_on_cooldown()
        self.mock_game_clock._GameClockSingleton__game_clock = self.cooldown_time
        self.assertTrue(self.cooldown_handler.is_action_ready())

    def test_action_not_ready_before_cooldown(self):
        self.mock_game_clock._GameClockSingleton__game_clock = 4000
        self.cooldown_handler.put_on_cooldown()
        self.assertFalse(self.cooldown_handler.is_action_ready())

    def test_put_on_cooldown_updates_last_action_time(self):
        self.mock_game_clock._GameClockSingleton__game_clock = 1000
        self.cooldown_handler.put_on_cooldown()
        self.assertEqual(self.cooldown_handler.last_action_time, 1000)

        self.mock_game_clock._GameClockSingleton__game_clock = 2000
        self.cooldown_handler.put_on_cooldown()
        self.assertEqual(self.cooldown_handler.last_action_time, 2000)

if __name__ == '__main__':
    unittest.main()