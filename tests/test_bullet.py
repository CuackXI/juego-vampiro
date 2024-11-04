# pylint: disable=C0114,C0115,C0116
import unittest
import pygame
from unittest.mock import patch, MagicMock
from business.entities.bullets import NormalBullet

class TestBullet(unittest.TestCase):
    @patch('pygame.transform.scale')
    @patch('pygame.image.load')
    def setUp(self, mock_image_load, mock_scale):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

        mock_surface = MagicMock(spec=pygame.Surface)
        mock_surface.convert_alpha.return_value = mock_surface
        mock_surface.get_size.return_value = (64, 64)

        mock_image_load.return_value = mock_surface
        mock_scale.return_value = mock_surface

        self.bullet = NormalBullet(0, 0, 10, 10, 5, 5, 5)

    def test_convert_data_to_json(self):
        data_to_save = ['pos_x', 'pos_y', 'dir_x', 'dir_y', 'damage', 'health', 'speed']

        result = self.bullet.to_json()
        for element in result:
            self.assertTrue(element in data_to_save)

    def test_initial_health(self):
        self.assertEqual(self.bullet.health, 5)

    def test_damage_amount(self):
        self.assertEqual(self.bullet.damage_amount, 5)

    def test_take_damage(self):
        self.bullet.take_damage(2)
        self.assertEqual(self.bullet.health, 3)

    def test_update_position(self):
        x_distance, y_distance = 3, 4

        self.bullet = NormalBullet(0, 0, x_distance, y_distance, 1, 1, 5)
        self.bullet.update(None)

        x, y = self.bullet.pos_x, self.bullet.pos_y
        self.assertAlmostEqual(x, 0.6)
        self.assertAlmostEqual(y, 0.8)
        self.assertAlmostEqual(x / x_distance, y / y_distance)

    def test_update_position_vertical(self):
        x_distance, y_distance = 0, 10

        self.bullet = NormalBullet(0, 0, x_distance, y_distance, 1, 1, 5)
        self.bullet.update(None)

        x, y = self.bullet.pos_x, self.bullet.pos_y
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 1)

    def test_update_position_horizontal(self):
        x_distance, y_distance = 10, 0

        self.bullet = NormalBullet(0, 0, x_distance, y_distance, 1, 1, 5)
        self.bullet.update(None)

        x, y = self.bullet.pos_x, self.bullet.pos_y
        self.assertAlmostEqual(x, 1)
        self.assertAlmostEqual(y, 0)

    def test_update_position_non_zero_src(self):
        src_x, src_y, dst_x, dst_y = 5, 5, 10, 10

        self.bullet = NormalBullet(src_x, src_y, dst_x, dst_y, 1, 1, 5)
        self.bullet.update(None)

        x, y = self.bullet.pos_x, self.bullet.pos_y
        self.assertAlmostEqual(x, 5.707, 2)
        self.assertAlmostEqual(y, 5.707, 2)

    def tearDown(self):
        pygame.display.quit()
        pygame.quit()

if __name__ == "main":
    unittest.main()
