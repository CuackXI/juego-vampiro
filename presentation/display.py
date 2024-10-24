"""Module for displaying the game world."""

import pygame

import settings
from business.world.game_world import GameWorld
from presentation.camera import Camera
from presentation.interfaces import IDisplay
from presentation.tileset import Tileset


class Display(IDisplay):
    """Class for displaying the game world."""

    def __init__(self):
        # Set the window display mode
        self.__screen = pygame.display.set_mode(settings.SCREEN_DIMENSION)

        # Set the window title
        pygame.display.set_caption(settings.GAME_TITLE)

        # Initialize the camera
        self.camera = Camera()

        self.__ground_tileset = self.__load_ground_tileset()
        self.__world: GameWorld = None

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
                tile_index = self.__world.tile_map.get(row, col)
                tile_image = self.__ground_tileset.get_tile(tile_index)

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
        continue_text = font.render("Continue", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        self.__screen.blit(opacity_square, (0, 0))

        continue_button.x = (settings.SCREEN_WIDTH - continue_button.x) // 2 - 200
        continue_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        quit_button.x = (settings.SCREEN_WIDTH - quit_button.x) // 2 + 200
        quit_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, (0, 0, 0), continue_button)
        pygame.draw.rect(self.__screen, (0, 0, 0), quit_button)

        self.__screen.blit(continue_text, (continue_button.x + 40, continue_button.y + 10))
        self.__screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    game.unpause_event()
                    return

                if quit_button.collidepoint(event.pos):
                    # save_game()
                    game.close_game_loop()
                    pygame.quit()
                    return

    def __draw_clock(self):
        elapsed_time_ms = pygame.time.get_ticks()

        total_seconds = elapsed_time_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60

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

    def render_frame(self, paused = None, game = None):
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

        if paused:
            self.__draw_pause_menu(game)

        # Update the display
        pygame.display.flip()
