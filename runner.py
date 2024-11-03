"""Runs the game"""
import logging

import pygame
import gc
import settings
from business.entities.player import Player
from business.world.game_world import GameWorld
from business.world.monster_spawner import MonsterSpawner
from business.world.tile_map import TileMap
from game import Game
from presentation.display import Display
from presentation.input_handler import InputHandler
from presentation.sprite import PlayerSprite
from persistence.gamedao import GameJSONDAO
from business.handlers.clock import GameClockSingleton

def initialize_player(saved_data: dict | None):
    """Initializes the player object"""
    x, y = settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2
    return Player(x, y, PlayerSprite(x, y), saved_data.get('player'))

def initialize_game_world(display, saved_data: dict | None):
    """Initializes the game world"""
    monster_spawner = MonsterSpawner(display)
    tile_map = TileMap()
    player = initialize_player(saved_data)
    return GameWorld(monster_spawner, tile_map, player, display, saved_data) 

def main():
    """Main function to run the game"""
    pygame.init()

    partidadao = GameJSONDAO()

    saved_data = partidadao.load_game()
    time = saved_data.get('clock')
    GameClockSingleton(time)

    display = Display()
    world = initialize_game_world(display, saved_data)
    display.load_world(world)
    input_handler = InputHandler(world)

    game = Game(world, input_handler, partidadao)

    reset = game.run()

    # Delete variables and instances to properly reset the game
    del game
    del world
    del input_handler
    del display
    del partidadao
    GameClockSingleton().delete()

    gc.collect()

    if reset == Game.RESET_EVENT:
        main()

    pygame.quit()

if __name__ == "__main__":
    main()