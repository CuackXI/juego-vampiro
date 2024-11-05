"""Handler for entities with a position escaping the boundaries of the world."""

import settings
from business.entities.entity import Entity

class BoundariesHandler:
    """Class that handles things related to the world boundaries."""

    @staticmethod
    def is_entity_within_world_boundaries(entity: Entity):
        """If the entity is inside the world."""
        return (
            20 <= entity.pos_x <= settings.WORLD_WIDTH - 20 and 25 <= entity.pos_y <= settings.WORLD_HEIGHT - 25
        )