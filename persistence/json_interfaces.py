from abc import ABC, abstractmethod

class JSONable(ABC):
    """Interface for JSONable classes"""

    @abstractmethod
    def to_json(self) -> dict:
        """Converts the necessary information from the class to a json_format

        Returns:
            dict: The data.
        """