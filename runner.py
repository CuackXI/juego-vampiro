"""Runs the game"""
import logging

import pygame

import settings
import business.entities.player as player
from business.world.game_world import GameWorld
from business.world.monster_spawner import MonsterSpawner
from business.world.tile_map import TileMap
from business.handlers.clock import Clock
from game import Game
from presentation.display import Display
from presentation.input_handler import InputHandler
from presentation.sprite import PlayerSprite


def initialize_player():
    """Initializes the player object"""
    x, y = settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2
    return player.Player(x, y, PlayerSprite(x, y))

def initialize_game_world(display):
    """Initializes the game world"""
    monster_spawner = MonsterSpawner(display)
    tile_map = TileMap()
    player = initialize_player()
    return GameWorld(monster_spawner, tile_map, player, display)

def main():
    """Main function to run the game"""
    # Initialize pygame
    pygame.init()

    # Logging configuration
    logging.basicConfig(
        level=logging.DEBUG,  # Change between INFO, WARNING or DEBUG as needed
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Initialize the game objects
    display = Display()
    world = initialize_game_world(display)
    clock = Clock()
    display.load_world(world)
    input_handler = InputHandler(world)

    # Create a game instance and start it
    game = Game(world, input_handler, clock)

    world.load_game(game)
    world.monster_spawner.load_world(world)
    world.player.load_game(game)

    game.run()

    # Properly quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()