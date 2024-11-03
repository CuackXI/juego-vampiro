import os
import json

from collections import defaultdict
from persistence.daointerfaces import IGameDAO
from business.handlers.clock import GameClockSingleton

class GameJSONDAO(IGameDAO):
    """JSON DAO that handles game data."""

    BASE_GAME_DATA = {}

    def __init__(self, json_path = "data/game.json") -> None:
        """Initializes the DAO."""
        self.__json_path = json_path
        if not os.path.exists(self.__json_path):
            with open(self.__json_path, 'w', encoding="utf-8") as file:
                json.dump(self.BASE_GAME_DATA, file, indent=4)

    def __read_data(self) -> dict:
        with open(self.__json_path, 'r', encoding="utf-8") as file:
            data = json.load(file)

        return data

    def __save_data(self, data) -> None:
        with open(self.__json_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def save_game(self, game):
        data = self.__read_data()

        monsters = defaultdict(list)
        for monster in game.world.monsters:
            monsters[str(type(monster))].append(monster.to_json())

        bullets = defaultdict(list)
        for bullet in game.world.bullets:
            bullets[str(type(bullet))].append(bullet.to_json())

        items = defaultdict(list)
        for item in game.world.items:
            items[str(type(item))].append(item.to_json())

        player = game.world.player.to_json()
        clock = GameClockSingleton().game_clock

        data['monsters'] = monsters
        data['bullets'] = bullets
        data['items'] = items
        data['player'] = player
        data['clock'] = clock

        self.__save_data(data)

    def load_game(self):
        data = self.__read_data()
        return data
    
    def clear_save(self):
        self.__save_data(GameJSONDAO.BASE_GAME_DATA)