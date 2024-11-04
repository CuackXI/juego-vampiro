import settings

class GameClockSingleton:
    """A singleton for managing the game clock."""
    
    _instance = None

    def __init__(self):
        self.__game_clock = 0 # Documentation

    def __new__(cls, saved_time=None):
        if cls._instance is None:
            cls._instance = super(GameClockSingleton, cls).__new__(cls)
            cls._instance.__game_clock = 0
            if saved_time:
                cls._instance.__game_clock = saved_time
        return cls._instance
    
    @classmethod
    def delete(cls):
        """Delete the singleton instance."""
        cls._instance = None

    @property
    def game_clock(self):
        """The current time value of the game in miliseconds."""
        return self.__game_clock

    def update(self):
        """Updates every tick by the amount of ms determined by the FPS of the settings."""
        self.__game_clock += 1000 / settings.FPS