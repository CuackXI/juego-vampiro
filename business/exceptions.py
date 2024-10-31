"""Module that contains custom exceptions."""


class DeadPlayerException(Exception):
    """Exception raised when the player dies."""

class EntityOutOfBounds(Exception):
    """When an entity spawns outside the map."""