import settings

class BoundariesHandler:
    """Class that handles things related to the world boundaries."""

    @staticmethod
    def is_entity_within_world_boundaries(entity):
        return (
            20 <= entity.pos_x <= settings.WORLD_WIDTH - 20 and 25 <= entity.pos_y <= settings.WORLD_HEIGHT - 25
        )