import unittest
from unittest.mock import Mock
from business.entities.entity import Entity
from business.handlers.boundaries_handler import BoundariesHandler
import settings

class TestBoundariesHandler(unittest.TestCase):

    def setUp(self):
        self.original_world_width = settings.WORLD_WIDTH
        self.original_world_height = settings.WORLD_HEIGHT
        settings.WORLD_WIDTH = 800
        settings.WORLD_HEIGHT = 600

    def tearDown(self):
        settings.WORLD_WIDTH = self.original_world_width
        settings.WORLD_HEIGHT = self.original_world_height

    def test_entity_within_boundaries(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 100
        entity.pos_y = 100
        
        self.assertTrue(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_beyond_left_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 10
        entity.pos_y = 100
        
        self.assertFalse(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_beyond_right_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 790
        entity.pos_y = 100
        
        self.assertFalse(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_beyond_top_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 100
        entity.pos_y = 20
        
        self.assertFalse(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_beyond_bottom_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 100
        entity.pos_y = 580
        
        self.assertFalse(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_on_left_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 20
        entity.pos_y = 100
        
        self.assertTrue(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_on_right_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 780
        entity.pos_y = 100
        
        self.assertTrue(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_on_top_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 100
        entity.pos_y = 25
        
        self.assertTrue(BoundariesHandler.is_entity_within_world_boundaries(entity))

    def test_entity_on_bottom_boundary(self):
        entity = Mock(spec=Entity)
        entity.pos_x = 100
        entity.pos_y = 575
        
        self.assertTrue(BoundariesHandler.is_entity_within_world_boundaries(entity))

if __name__ == '__main__':
    unittest.main()
