"""Module that contains the TileMap class."""

import settings
from business.world.interfaces import ITileMap


class TileMap(ITileMap):
    """Class that represents the tile map of the game world."""

    def __init__(self):
        self.map_data = self.__generate_tile_map()

    def __generate_tile_map(self):
        """Generates the tile map."""
        tile_map = [[0 for _ in range(settings.WORLD_COLUMNS)] for _ in range(settings.WORLD_ROWS)]
        
        return tile_map

    def get(self, row, col) -> int:
        """Gets a certain tile."""
        return self.map_data[row][col]