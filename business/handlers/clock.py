import settings

class GameClockSingleton:
    """A singleton class for managing the game clock."""
    
    _instance = None

    def __new__(cls, saved_time = None):
        if cls._instance is None:
            cls._instance = super(GameClockSingleton, cls).__new__(cls)
            cls._instance.game_clock = 0
            if saved_time:
                cls._instance.game_clock = saved_time
        return cls._instance
        
    def update(self):
        """Updates every tick by the amount of ms determined by the FPS"""
        self.game_clock += 1000 / settings.FPS