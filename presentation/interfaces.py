"""Interfaces for the presentation layer."""

from abc import ABC, abstractmethod

from presentation.camera import Camera

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.world.interfaces import IGameWorld


class IDisplay(ABC):
    """Interface for displaying the game world."""

    @abstractmethod
    def load_world(self, world: "IGameWorld"):
        """Load the world into the display.

        Args:
            world (IGameWorld): The game world to be displayed.
        """

    @abstractmethod
    def render_frame(self):
        """Render the current frame."""

    @property
    @abstractmethod
    def camera(self) -> Camera:
        """The camera of the display.

        Returns:
            Camera: The camera.
        """

class IInputHandler(ABC):
    """Interface for handling user input."""

    @abstractmethod
    def process_input(self):
        """Process the input from the user."""

    @abstractmethod
    def is_pause_pressed(self):
        """If the pause button is being pressed."""

    @abstractmethod
    def process_pause(self):
        """Toggles the paused state of the game."""
