import unittest
from unittest.mock import MagicMock
from presentation.sprite import Sprite
from business.entities.entity import MovableEntity

class TestMovableEntity(unittest.TestCase):
    class TestMovableEntityImplementation(MovableEntity):
        def __str__(self):
            return "TestMovableEntity"

    def setUp(self):
        self.mock_sprite = MagicMock(spec=Sprite)
        self.movable_entity = self.TestMovableEntityImplementation(0, 0, 1.0, self.mock_sprite)

    def test_move_updates_position(self):
        self.movable_entity.move(3, 4)
        self.assertEqual(self.movable_entity.pos_x, 3.0)
        self.assertEqual(self.movable_entity.pos_y, 4.0)
        self.movable_entity.sprite.update_pos.assert_called_once_with(3.0, 4.0)
