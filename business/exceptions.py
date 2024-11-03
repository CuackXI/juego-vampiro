"""Module that contains custom exceptions."""


class DeadPlayerException(Exception):
    """Exception raised when the player dies."""

class EntityOutOfBounds(Exception):
    """When an entity spawns outside the map."""

class ResetGame(Exception):
    """Game event where the game needs to be reseted."""