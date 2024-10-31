import settings

class GameClockSingleton:
    def __init__(self):
        self.game_clock = 0
        
    def update(self):
        self.game_clock += 1000 / settings.FPS

clock = GameClockSingleton()