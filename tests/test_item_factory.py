import unittest
from unittest.mock import Mock, patch, ANY
from business.entities.items.experience_gem import ExperienceGem, RedExperienceGem, GreenExperienceGem, BlueExperienceGem
from business.entities.items.guaymallen import Guaymallen
from business.world.interfaces import IGameWorld
from business.entities.items.item_factory import ItemFactory
import pygame

class TestItemFactory(unittest.TestCase):
    @patch('business.entities.items.experience_gem.ExperienceGemSprite')
    @patch('pygame.image.load')
    def setUp(self, mock_load, mock_sprite):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

        self.mock_surface = pygame.Surface((10, 10))
        mock_load.return_value = self.mock_surface
        mock_sprite.return_value = self.mock_surface

        self.world = Mock(spec=IGameWorld)
        self.entity = Mock()
        self.entity.pos_x = 10
        self.entity.pos_y = 15
        self.amount = 50
        self.gem = ExperienceGem(self.entity.pos_x, self.entity.pos_y, self.amount)

    def test_create_common_gem(self):
        xp_amount = 100
        ItemFactory.create_item(ItemFactory.COMMON_GEM, self.entity, self.world, xp_amount)
        self.world.add_item.assert_called_once_with(ANY)

    def test_create_red_gem(self):
        xp_amount = 200
        ItemFactory.create_item(ItemFactory.RED_GEM, self.entity, self.world, xp_amount)
        self.world.add_item.assert_called_once_with(ANY)

    def test_create_green_gem(self):
        xp_amount = 300
        ItemFactory.create_item(ItemFactory.GREEN_GEM, self.entity, self.world, xp_amount)
        self.world.add_item.assert_called_once_with(ANY)

    def test_create_blue_gem(self):
        xp_amount = 400
        ItemFactory.create_item(ItemFactory.BLUE_GEM, self.entity, self.world, xp_amount)
        self.world.add_item.assert_called_once_with(ANY)

    def test_create_guaymallen(self):
        ItemFactory.create_item(ItemFactory.GUAYMALLEN, self.entity, self.world)
        self.world.add_item.assert_called_once_with(ANY)

    def test_load_items(self):
        saved_data = {
            'items': {
                'experience_gem.ExperienceGem': [{'pos_x': 1, 'pos_y': 2, 'amount': 50, 'despawn_cooldown': 10}],
                'RedExperienceGem': [{'pos_x': 3, 'pos_y': 4, 'amount': 75, 'despawn_cooldown': 8}],
                'GreenExperienceGem': [{'pos_x': 5, 'pos_y': 6, 'amount': 100, 'despawn_cooldown': 6}],
                'BlueExperienceGem': [{'pos_x': 7, 'pos_y': 8, 'amount': 125, 'despawn_cooldown': 4}],
                'Guaymallen': [{'pos_x': 9, 'pos_y': 10}]
            }
        }

        ItemFactory.load_items(self.world, saved_data)

        self.world.add_item.assert_any_call(ANY)
        self.world.add_item.assert_any_call(ANY)
        self.world.add_item.assert_any_call(ANY)
        self.world.add_item.assert_any_call(ANY)
        self.world.add_item.assert_any_call(ANY)

        self.assertEqual(self.world.add_item.call_count, 5)

    def tearDown(self):
        pygame.display.quit()
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
