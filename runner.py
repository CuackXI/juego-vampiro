"""Runs the game"""
import logging

import pygame

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
    # Initialize pygame
    pygame.init()

    # Logging configuration
    logging.basicConfig(
        level=logging.DEBUG,  # Change between INFO, WARNING or DEBUG as needed
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    #TODO: Si el jugador muere, no guardar los datos :v. Ademas establecer un metodo de reset de partida, con la configuración inicial.

    partidadao = GameJSONDAO()

    # Loads the saved game
    saved_data = partidadao.load_game()
    time = saved_data.get('clock')
    GameClockSingleton(time)

    display = Display()
    world = initialize_game_world(display, saved_data)
    display.load_world(world)
    input_handler = InputHandler(world)

    # Create a game instance and start it
    game = Game(world, input_handler, partidadao)

    game.run()

    # Properly quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()