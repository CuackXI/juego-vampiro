import unittest
from unittest.mock import MagicMock
from presentation.sprite import Sprite
from business.entities.entity import Entity

class TestEntity(unittest.TestCase):
    class TestEntityImplementation(Entity):
        def __str__(self):
            return "TestEntity"

    def setUp(self):
        self.mock_sprite = MagicMock(spec=Sprite)
        self.entity = self.TestEntityImplementation(0, 0, self.mock_sprite)

    def test_distance_to_another_entity(self):
        other_entity = self.TestEntityImplementation(3, 4, self.mock_sprite)
        self.assertEqual(self.entity._get_distance_to(other_entity), 5.0)

    def test_update_calls_sprite_update(self):
        self.entity.update(None)
        self.entity.sprite.update.assert_called_once()

if __name__ == '__main__':
    unittest.main()
