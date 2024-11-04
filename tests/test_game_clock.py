import unittest
from business.handlers.clock import GameClockSingleton
import settings

class TestGameClockSingleton(unittest.TestCase):
    def test_update_game_clock(self):
        GameClockSingleton().update()

        expected_time = 1000 / settings.FPS
        self.assertAlmostEqual(GameClockSingleton().game_clock, expected_time, places=2)

        GameClockSingleton().update()
        self.assertAlmostEqual(GameClockSingleton().game_clock, expected_time * 2, places=2)

    def test_reset_game_clock(self):
        GameClockSingleton().update()
        self.assertNotEqual(GameClockSingleton().game_clock, 0)

        GameClockSingleton.reset()
        self.assertEqual(GameClockSingleton().game_clock, 0)

if __name__ == '__main__':
    unittest.main()