import unittest
from unittest.mock import MagicMock, patch
from business.entities.items.experience_gem import ExperienceGem
import pygame


class TestExperienceGem(unittest.TestCase):

    @patch('pygame.image.load', autospec=True)
    @patch('presentation.sprite.ExperienceGemSprite', autospec=True)
    def setUp(self, mock_sprite, mock_load):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

        self.mock_surface = pygame.Surface((10, 10))
        mock_load.return_value = self.mock_surface
        mock_sprite.return_value = self.mock_surface

        self.pos_x = 10
        self.pos_y = 15
        self.amount = 50
        self.gem = ExperienceGem(self.pos_x, self.pos_y, self.amount)

    def test_can_despawn(self):
        self.assertFalse(self.gem.can_despawn)

        self.gem._ExperienceGem__despawn_cooldown.last_action_time = 0
        self.gem._ExperienceGem__despawn_cooldown._CooldownHandler__cooldown_time = 0

        self.assertTrue(self.gem.can_despawn)

    def test_to_json(self):
        json_data = self.gem.to_json()
        expected_data = {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'amount': self.amount,
            'despawn_cooldown': self.gem._ExperienceGem__despawn_cooldown.last_action_time
        }
        self.assertEqual(json_data, expected_data)

    def test_in_player_range(self):
        mock_player = MagicMock()
        mock_player.pick_range = 10
        mock_player.pos_x = 12
        mock_player.pos_y = 18

        with patch.object(self.gem, '_get_distance_to', return_value=8):
            self.assertTrue(self.gem.in_player_range(mock_player))

        with patch.object(self.gem, '_get_distance_to', return_value=12):
            self.assertFalse(self.gem.in_player_range(mock_player))

    def tearDown(self):
        pygame.display.quit()
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
