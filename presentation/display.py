"""Module for displaying the game world."""

import pygame
import logging
import settings
from business.world.game_world import GameWorld
from presentation.camera import Camera
from presentation.interfaces import IDisplay
from presentation.tileset import Tileset
from business.handlers.clock import GameClockSingleton
import random
from game import Game

class Display(IDisplay):
    """Class for displaying the game world."""

    def __init__(self):
        # Set the window display mode
        self.__screen = pygame.display.set_mode(settings.SCREEN_DIMENSION)

        # Set the window title
        pygame.display.set_caption(settings.GAME_TITLE)

        # Initialize the camera
        self.camera = Camera()

        self.__perks_for_display = []

        self.__ground_tileset = self.__load_ground_tileset()
        self.__world: GameWorld = None

    def __get_perks(self):
        if len(self.__perks_for_display) == 0:
            self.__perks_for_display = self.__world.get_perks_for_display()
        
        return self.__perks_for_display

    def __load_ground_tileset(self):
        return Tileset(
            "./assets/ground_tileset.png", settings.TILE_WIDTH, settings.TILE_HEIGHT, 2, 3
        )

    def __render_ground_tiles(self):
        # Calculate the range of tiles to render based on the camera position
        start_col = max(0, self.camera.camera_rect.left // settings.TILE_WIDTH)
        end_col = min(
            settings.WORLD_COLUMNS, (self.camera.camera_rect.right // settings.TILE_WIDTH) + 1
        )
        start_row = max(0, self.camera.camera_rect.top // settings.TILE_HEIGHT)
        end_row = min(
            settings.WORLD_ROWS, (self.camera.camera_rect.bottom // settings.TILE_HEIGHT) + 1
        )

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                # Get the tile index from the tile map
                # tile_index = self.__world.tile_map.get(row, col)
                tile_image = self.__ground_tileset.get_tile(1)

                # Calculate the position on the screen
                x = col * settings.TILE_WIDTH - self.camera.camera_rect.left
                y = row * settings.TILE_HEIGHT - self.camera.camera_rect.top

                self.__screen.blit(tile_image, (x, y))

    def __draw_player_health_bar(self):
        """Draws the player's health bar and health value on the screen."""
        player = self.__world.player

        # Define the health bar dimensions
        bar_width = settings.TILE_WIDTH
        bar_height = 5
        bar_x = player.sprite.rect.centerx - bar_width // 2 - self.camera.camera_rect.left
        bar_y = player.sprite.rect.bottom + 5 - self.camera.camera_rect.top

        # Draw the background bar (red)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.__screen, (255, 0, 0), bg_rect)

        # Draw the health bar (green)
        health_percentage = player.health / player.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(self.__screen, (0, 255, 0), health_rect)

        # Render the health value
        health_text = f"{int(player.health)}"
        font = pygame.font.Font(None, 24)  # Use default font and set size
        text_surface = font.render(health_text, True, (255, 255, 255))  # White text
        text_x = bar_x + (bar_width - text_surface.get_width()) // 2  # Center below the health bar
        text_y = bar_y + bar_height + 5  # Position below the health bar

        # Draw the health value text
        self.__screen.blit(text_surface, (text_x, text_y))

    def __draw_monster_health_bar(self, monster):
        """Draws the monster's health bar and health value on the screen."""
        
        # Define the health bar dimensions
        bar_width = settings.TILE_WIDTH
        bar_height = 5
        bar_x = monster.sprite.rect.centerx - bar_width // 2 - self.camera.camera_rect.left
        bar_y = monster.sprite.rect.bottom + 5 - self.camera.camera_rect.top

        # Draw the background bar (red)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.__screen, (255, 0, 0), bg_rect)

        # Draw the health bar (green)
        health_percentage = monster.health / monster.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(self.__screen, (0, 255, 0), health_rect)

    def __draw_player(self):
        adjusted_rect = self.camera.apply(self.__world.player.sprite.rect)
        self.__screen.blit(self.__world.player.sprite.image, adjusted_rect)

        self.__draw_player_health_bar()

        # Draw the experience text
        font = pygame.font.SysFont(None, 48)
        experience_text = font.render(
            f"LEVEL {self.__world.player.level} XP: {self.__world.player.experience}/{self.__world.player.experience_to_next_level}",
            True,
            (255, 255, 255),
        )
        self.__screen.blit(experience_text, (10, 10))

    def load_world(self, world: GameWorld):
        self.__world = world

    def __draw_pause_menu(self, game):
        x = self.__world.player.pos_x
        y = self.__world.player.pos_y

        x = max(0, min(x, settings.WORLD_WIDTH - settings.SCREEN_WIDTH))
        y = max(0, min(y, settings.WORLD_HEIGHT - settings.SCREEN_HEIGHT))

        opacity_square = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        opacity_square.fill((0, 0, 0, 30))

        self.__screen.blit(opacity_square, (0, 0))

        continue_button = pygame.Rect(150, 150, 200, 50)
        quit_button = pygame.Rect(150, 250, 200, 50)

        font = pygame.font.Font(None, 36)
        continue_text = font.render("Continuar", True, (255, 255, 255))
        quit_text = font.render("Salir y guardar", True, (255, 255, 255))

        self.__screen.blit(opacity_square, (0, 0))

        continue_button.x = (settings.SCREEN_WIDTH - continue_button.x) // 2 - 200
        continue_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        quit_button.x = (settings.SCREEN_WIDTH - quit_button.x) // 2 + 200
        quit_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, (0, 0, 0), continue_button)
        pygame.draw.rect(self.__screen, (0, 0, 0), quit_button)

        self.__screen.blit(continue_text, (continue_button.x + 40, continue_button.y + 10))
        self.__screen.blit(quit_text, (quit_button.x + 17, quit_button.y + 10))

        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if continue_button.collidepoint(mouse_pos):
                game.unpause_event()
                return
            elif quit_button.collidepoint(mouse_pos):
                game.close_game_loop()
                game.save_game()
                pygame.quit()
                return

    def __draw_clock(self):
        clock = GameClockSingleton()
        total_seconds = clock.game_clock // 1000
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        if minutes < 10:
            minutes = "0" + str(minutes)

        if seconds < 10:
            seconds = "0" + str(seconds)

        formatted_time = f"{minutes}:{seconds}"

        font = pygame.font.Font(None, 36)
        time_text = font.render(formatted_time, True, (255, 255, 255))

        text_width, text_height = time_text.get_size()

        opacity_square = pygame.Surface((text_width + 20, text_height + 10), pygame.SRCALPHA)
        opacity_square.fill((0, 0, 0, 77))

        box_x = (settings.SCREEN_WIDTH- text_width) // 2 - 10
        box_y = 10

        self.__screen.blit(opacity_square, (box_x, box_y))

        self.__screen.blit(time_text, (box_x + 10, box_y + 5))

    def __draw_game_over_screen(self, game):
        x = self.__world.player.pos_x
        y = self.__world.player.pos_y

        x = max(0, min(x, settings.WORLD_WIDTH - settings.SCREEN_WIDTH))
        y = max(0, min(y, settings.WORLD_HEIGHT - settings.SCREEN_HEIGHT))

        opacity_square = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        opacity_square.fill((0, 0, 0, 120))

        self.__screen.blit(opacity_square, (0, 0))

        game_over_font = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)

        game_over_text = game_over_font.render("Juego terminado!", True, (255, 150, 150))

        self.__screen.blit(game_over_text, ((settings.SCREEN_WIDTH // 2) - 190, (settings.SCREEN_HEIGHT // 2) - 10))

        # Boton de reset

        reset_button = pygame.Rect(150, 250, 200, 50)
        reset_text = font.render("Reiniciar", True, (255, 255, 255))

        reset_button.x = (settings.SCREEN_WIDTH // 2) - (reset_button.width // 2) - 150
        reset_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, (0, 0, 0), reset_button)

        self.__screen.blit(reset_text, (reset_button.x + 40, reset_button.y + 10))

        # Boton de salir

        quit_button = pygame.Rect(150, 250, 200, 50)
        quit_text = font.render("Salir", True, (255, 255, 255))

        quit_button.x = (settings.SCREEN_WIDTH // 2) - (quit_button.width // 2) + 150
        quit_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, (0, 0, 0), quit_button)

        self.__screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if quit_button.collidepoint(mouse_pos):
                game.close_game_loop()
                game.clear_save()
                pygame.quit()
                return
            elif reset_button.collidepoint(mouse_pos):
                game.reset_game()
                return

    def __draw_upgrade_menu(self):
        perks = self.__get_perks()

        opacity_square = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        opacity_square.fill((0, 0, 0, 30))
        self.__screen.blit(opacity_square, (0, 0))

        upgrade_buttons = []

        font = pygame.font.Font(None, 36)

        if len(perks) != 0:
            for i in range(len(perks)):
                upgrade_button = pygame.Rect(0, 0, settings.SCREEN_WIDTH - 100, settings.SCREEN_HEIGHT // 20)
                upgrade_button.x = 50
                upgrade_button.y = 100 + (i * 200)

                upgrade_buttons.append(upgrade_button)

                upgrade_text = font.render(str(perks[i]), True, (255, 255, 255))
                pygame.draw.rect(self.__screen, (0, 0, 0), upgrade_button)
                self.__screen.blit(upgrade_text, (upgrade_button.x + 40, upgrade_button.y + 10))
        else:
            upgrade_button = pygame.Rect(0, 0, settings.SCREEN_WIDTH - 100, settings.SCREEN_HEIGHT // 20)
            upgrade_button.x = 50
            upgrade_button.y = 700

            upgrade_buttons.append(upgrade_button)

            upgrade_text = font.render(("Sin mejoras disponibles"), True, (255, 255, 255))
            pygame.draw.rect(self.__screen, (0, 0, 0), upgrade_button)
            self.__screen.blit(upgrade_text, (upgrade_button.x + 40, upgrade_button.y + 10))

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(upgrade_buttons):
            if button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.__world.in_upgrade = False
                if len(perks) != 0:
                    self.__world.give_perk_to_player(perks[i])
                    self.__perks_for_display.clear()
                return

    def render_frame(self, paused = None, in_upgrade = None, dead = None, game = None):
        self.camera.update(self.__world.player.sprite.rect)

        # Render the ground tiles
        self.__render_ground_tiles()

        # Draw all the experience gems
        for gem in self.__world.experience_gems:
            if self.camera.camera_rect.colliderect(gem.sprite.rect):
                adjusted_rect = self.camera.apply(gem.sprite.rect)
                self.__screen.blit(gem.sprite.image, adjusted_rect)

        # Draw all monsters
        for monster in self.__world.monsters:
            if self.camera.camera_rect.colliderect(monster.sprite.rect):
                adjusted_rect = self.camera.apply(monster.sprite.rect)
                self.__screen.blit(monster.sprite.image, adjusted_rect)
                if monster.health != monster.max_health:
                    self.__draw_monster_health_bar(monster)

        # Draw the bullets
        for bullet in self.__world.bullets:
            if self.camera.camera_rect.colliderect(bullet.sprite.rect):
                adjusted_rect = self.camera.apply(bullet.sprite.rect)
                self.__screen.blit(bullet.sprite.image, adjusted_rect)

        # Draw the player
        self.__draw_player()

        self.__draw_clock()

        if in_upgrade:
            self.__draw_upgrade_menu()

        if dead:
            self.__draw_game_over_screen(game)

        if paused:
            self.__draw_pause_menu(game)

        # Update the display
        pygame.display.flip()