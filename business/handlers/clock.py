import settings

class GameClockSingleton:

    """A singleton class for managing the game clock."""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameClockSingleton, cls).__new__(cls)
            cls._instance.game_clock = 0  # Initialize the clock
        return cls._instance
        
    def update(self):
        self.game_clock += 1000 / settings.FPS