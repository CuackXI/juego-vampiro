"""Module for displaying the game world."""

import pygame
import settings
from business.world.interfaces import IGameWorld
from business.exceptions import ResetGame
from presentation.camera import Camera
from presentation.interfaces import IDisplay
from presentation.tileset import Tileset
from business.handlers.clock import GameClockSingleton
from business.entities.interfaces import IPlayer, IMonster
from business.upgrades.interfaces import IPerk
from game import Game

class Display(IDisplay):
    """Class for displaying the game world."""

    COLOR_MENUS_BG = (0, 0, 0, 210)
    COLOR_BUTTON = (255, 255, 255)
    COLOR_BUTTON_TEXT = (0, 0, 0)
    COLOR_UI_OVERLAY = (0, 0, 0, 130)

    def __init__(self):
        self.__screen = pygame.display.set_mode(settings.SCREEN_DIMENSION)

        pygame.display.set_caption(settings.GAME_TITLE)

        self.__camera = Camera()

        self.__perks_for_display = []

        self.__ground_tileset = self.__load_ground_tileset()
        self.__world: IGameWorld = None

        self.__button_clicked = False

    def load_world(self, world: IGameWorld):
        self.__world = world

    @property
    def camera(self) -> Camera:
        return self.__camera

    def __get_perks(self):
        if len(self.__perks_for_display) == 0:
            self.__perks_for_display = self.__world.get_perks_for_display()
        
        return self.__perks_for_display

    def __load_ground_tileset(self):
        return Tileset(
            "./assets/ground_tileset.png", settings.TILE_WIDTH, settings.TILE_HEIGHT, 2, 3
        )

    def __render_ground_tiles(self):
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
                tile_image = self.__ground_tileset.get_tile(1)

                x = col * settings.TILE_WIDTH - self.camera.camera_rect.left
                y = row * settings.TILE_HEIGHT - self.camera.camera_rect.top

                self.__screen.blit(tile_image, (x, y))

    def __draw_player_health_bar(self):
        """Draws the player's health bar and health value on the screen."""
        player: IPlayer = self.__world.player

        bar_width = settings.TILE_WIDTH
        bar_height = 5
        bar_x = player.sprite.rect.centerx - bar_width // 2 - self.camera.camera_rect.left
        bar_y = player.sprite.rect.bottom + 5 - self.camera.camera_rect.top

        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.__screen, (255, 0, 0), bg_rect)

        health_percentage = player.health / player.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(self.__screen, (0, 255, 0), health_rect)

        health_text = f"{int(player.health)}"
        font = pygame.font.Font(None, 24)
        text_surface = font.render(health_text, True, (255, 255, 255))
        text_x = bar_x + (bar_width - text_surface.get_width()) // 2
        text_y = bar_y + bar_height + 5

        # Draw the health value text
        self.__screen.blit(text_surface, (text_x, text_y))

    def __draw_monster_health_bar(self, monster: IMonster):
        """Draws the monster's health bar and health value on the screen, only if its health is under its max health."""
        
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

    def __draw_player_inventory(self):
        inventory = self.__world.player.inventory

        level_font = pygame.font.SysFont(None, 20)
        title_text = level_font.render(
            f"Inventario:",
            True,
            (255, 255, 255),
        )
        self.__screen.blit(title_text, (10, 50))

        opacity_square = pygame.Surface(((len(inventory) * 55) + 10, 65), pygame.SRCALPHA)
        opacity_square.fill(self.COLOR_UI_OVERLAY)

        self.__screen.blit(opacity_square, (10, 70))

        level_font = pygame.font.SysFont(None, 30)
        for i in range(len(inventory)):
            perk_sprite = inventory[i].sprite
            perk_level = level_font.render(
                f"{inventory[i].level}",
                True,
                (255, 255, 255),
            )

            self.__screen.blit(perk_sprite.image, (15 + (i * 55), 75))
            self.__screen.blit(perk_level, (45 + (i * 55), 115))

    def __draw_pause_menu(self, game: Game):
        x = self.__world.player.pos_x
        y = self.__world.player.pos_y

        x = max(0, min(x, settings.WORLD_WIDTH - settings.SCREEN_WIDTH))
        y = max(0, min(y, settings.WORLD_HEIGHT - settings.SCREEN_HEIGHT))

        opacity_square = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        opacity_square.fill(self.COLOR_MENUS_BG)

        continue_button = pygame.Rect(150, 150, 200, 50)
        quit_button = pygame.Rect(150, 250, 200, 50)

        font = pygame.font.Font(None, 36)
        continue_text = font.render("Continuar", True, self.COLOR_BUTTON_TEXT)
        quit_text = font.render("Salir y guardar", True, self.COLOR_BUTTON_TEXT)

        continue_button.x = (settings.SCREEN_WIDTH - continue_button.x) // 2 - 200
        continue_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        quit_button.x = (settings.SCREEN_WIDTH - quit_button.x) // 2 + 200
        quit_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pause_font = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)

        pause_text = pause_font.render("En pausa", True, (255, 255, 255))

        self.__screen.blit(opacity_square, (0, 0))
        pygame.draw.rect(self.__screen, self.COLOR_BUTTON, continue_button)
        pygame.draw.rect(self.__screen, self.COLOR_BUTTON, quit_button)
        self.__screen.blit(continue_text, (continue_button.x + 40, continue_button.y + 10))
        self.__screen.blit(quit_text, (quit_button.x + 17, quit_button.y + 10))
        self.__screen.blit(pause_text, ((settings.SCREEN_WIDTH // 2) - 100, (settings.SCREEN_HEIGHT // 2) - 60))

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
        time = self.__time_as_text()

        font = pygame.font.Font(None, 36)
        time_text = font.render(time, True, (255, 255, 255))

        text_width, text_height = time_text.get_size()

        opacity_square = pygame.Surface((text_width + 20, text_height + 10), pygame.SRCALPHA)
        opacity_square.fill(self.COLOR_UI_OVERLAY)

        box_x = (settings.SCREEN_WIDTH- text_width) // 2 - 10
        box_y = 10

        self.__screen.blit(opacity_square, (box_x, box_y))

        self.__screen.blit(time_text, (box_x + 10, box_y + 5))

    def __draw_game_over_screen(self, game: Game):
        x = self.__world.player.pos_x
        y = self.__world.player.pos_y

        x = max(0, min(x, settings.WORLD_WIDTH - settings.SCREEN_WIDTH))
        y = max(0, min(y, settings.WORLD_HEIGHT - settings.SCREEN_HEIGHT))

        opacity_square = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        opacity_square.fill(self.COLOR_MENUS_BG)

        self.__screen.blit(opacity_square, (0, 0))

        game_over_font = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)

        time = self.__time_as_text()

        game_over_text = game_over_font.render("Juego terminado!", True, (255, 150, 150))
        level_text = font.render(f"Nivel: {self.__world.player.level}", True, (255, 255, 255))
        time_text = font.render(f"Tiempo: {time}", True, (255, 255, 255))

        self.__screen.blit(game_over_text, ((settings.SCREEN_WIDTH // 2) - 210, (settings.SCREEN_HEIGHT // 2) - 60))
        self.__screen.blit(level_text, ((settings.SCREEN_WIDTH // 2) - 80, (settings.SCREEN_HEIGHT // 2) + 10))
        self.__screen.blit(time_text, ((settings.SCREEN_WIDTH // 2) - 80, (settings.SCREEN_HEIGHT // 2) + 40))

        # Boton de reset

        reset_button = pygame.Rect(150, 250, 200, 50)
        reset_text = font.render("Reiniciar", True, self.COLOR_BUTTON_TEXT)

        reset_button.x = (settings.SCREEN_WIDTH // 2) - (reset_button.width // 2) - 150
        reset_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, self.COLOR_BUTTON, reset_button)

        self.__screen.blit(reset_text, (reset_button.x + 40, reset_button.y + 10))

        # Boton de salir

        quit_button = pygame.Rect(150, 250, 200, 50)
        quit_text = font.render("Salir", True, self.COLOR_BUTTON_TEXT)

        quit_button.x = (settings.SCREEN_WIDTH // 2) - (quit_button.width // 2) + 150
        quit_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, self.COLOR_BUTTON, quit_button)

        self.__screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if quit_button.collidepoint(mouse_pos):
                game.close_game_loop()
                game.clear_save()
                pygame.quit()
                return
            elif reset_button.collidepoint(mouse_pos):
                raise ResetGame
            
    def __draw_win_screen(self, game: Game):
        game.win()

        x = self.__world.player.pos_x
        y = self.__world.player.pos_y

        x = max(0, min(x, settings.WORLD_WIDTH - settings.SCREEN_WIDTH))
        y = max(0, min(y, settings.WORLD_HEIGHT - settings.SCREEN_HEIGHT))

        opacity_square = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        opacity_square.fill(self.COLOR_MENUS_BG)

        self.__screen.blit(opacity_square, (0, 0))

        game_over_font = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)

        time = self.__time_as_text()

        game_over_text = game_over_font.render("Ganaste!", True, (150, 255, 150))
        level_text = font.render(f"Nivel: {self.__world.player.level}", True, (255, 255, 255))

        self.__screen.blit(game_over_text, ((settings.SCREEN_WIDTH // 2) - 100, (settings.SCREEN_HEIGHT // 2) - 60))
        self.__screen.blit(level_text, ((settings.SCREEN_WIDTH // 2) - 80, (settings.SCREEN_HEIGHT // 2) + 10))
        # Boton de reset

        reset_button = pygame.Rect(150, 250, 200, 50)
        reset_text = font.render("Reiniciar", True, self.COLOR_BUTTON_TEXT)

        reset_button.x = (settings.SCREEN_WIDTH // 2) - (reset_button.width // 2) - 150
        reset_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, self.COLOR_BUTTON, reset_button)

        self.__screen.blit(reset_text, (reset_button.x + 40, reset_button.y + 10))

        # Boton de salir

        quit_button = pygame.Rect(150, 250, 200, 50)
        quit_text = font.render("Salir", True, self.COLOR_BUTTON_TEXT)

        quit_button.x = (settings.SCREEN_WIDTH // 2) - (quit_button.width // 2) + 150
        quit_button.y = (settings.SCREEN_HEIGHT // 2) + 200

        pygame.draw.rect(self.__screen, self.COLOR_BUTTON, quit_button)

        self.__screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if quit_button.collidepoint(mouse_pos):
                game.close_game_loop()
                game.clear_save()
                pygame.quit()
                return
            elif reset_button.collidepoint(mouse_pos):
                raise ResetGame

    def __draw_upgrade_menu(self):
        perks: list[IPerk] = self.__get_perks()

        if len(perks) != 0:
            opacity_square = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
            opacity_square.fill(self.COLOR_MENUS_BG)
            self.__screen.blit(opacity_square, (0, 0))

            upgrade_buttons: list[pygame.Rect] = []

            font = pygame.font.Font(None, 36)
            header_font = pygame.font.Font(None, 72)

            header_text = header_font.render("Subiste de nivel!", True, (255, 255, 255))

            self.__screen.blit(header_text, ((settings.SCREEN_WIDTH // 2) - 190, (settings.SCREEN_HEIGHT // 2) - 60))

            for i in range(len(perks)):
                upgrade_button = pygame.Rect(0, 0, settings.SCREEN_WIDTH - 600, 45)
                upgrade_button.x = 300
                upgrade_button.y = 400 + (i * 70)

                upgrade_buttons.append(upgrade_button)

                # Assuming the perk has a property 'sprite' which contains the instantiated sprite
                perk_sprite = perks[i].sprite
                if perk_sprite:
                    # Draw the perk sprite to the left of the button
                    self.__screen.blit(perk_sprite.image, (upgrade_button.x - 50, upgrade_button.y))

                upgrade_text = font.render(str(perks[i]), True, self.COLOR_BUTTON_TEXT)
                pygame.draw.rect(self.__screen, self.COLOR_BUTTON, upgrade_button)
                self.__screen.blit(upgrade_text, (upgrade_button.x + 40, upgrade_button.y + 10))
        else:
            self.__world.in_upgrade -= 1
            return

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(upgrade_buttons):
            if button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.__button_clicked = True
                self.__index = i

            if button.collidepoint(mouse_pos) and not pygame.mouse.get_pressed()[0] and self.__button_clicked and self.__index == i:
                self.__button_clicked = False
                self.__world.in_upgrade -= 1
                if len(perks) != 0:
                    self.__world.give_perk_to_player(perks[i])
                    self.__perks_for_display.clear()
                return

    def __time_as_text(self) -> str:
        clock = GameClockSingleton()
        total_seconds = clock.game_clock // 1000
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        if minutes < 10:
            minutes = "0" + str(minutes)

        if seconds < 10:
            seconds = "0" + str(seconds)

        formatted_time = f"{minutes}:{seconds}"
        return formatted_time

    def __draw_player_level_bar(self):
        bar_width = 400
        bar_height = 25

        bar_x = 100
        bar_y = 20

        progress_percentage = self.__world.player.experience_progress
        filled_width = int(bar_width * progress_percentage)

        bar_color = (50, 205, 50)
        bg_color = (105, 105, 105)

        pygame.draw.rect(self.__screen, bg_color, (bar_x, bar_y, bar_width, bar_height))

        pygame.draw.rect(self.__screen, bar_color, (bar_x, bar_y, filled_width, bar_height))

        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Nivel {self.__world.player.level}", True, (255, 255, 255))

        text_x = bar_x - 100
        text_y = bar_y

        self.__screen.blit(level_text, (text_x + 2, text_y))

    def render_frame(self, paused = None, in_upgrade = None, dead = None, game = None):
        self.camera.update(self.__world.player.sprite.rect)

        # Render the ground tiles
        self.__render_ground_tiles()

        # Draw all the experience gems
        for item in self.__world.items:
            if self.camera.camera_rect.colliderect(item.sprite.rect):
                adjusted_rect = self.camera.apply(item.sprite.rect)
                self.__screen.blit(item.sprite.image, adjusted_rect)

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

        if in_upgrade != 0:
            self.__draw_upgrade_menu()

        if paused:
            self.__draw_pause_menu(game)

        self.__draw_player_inventory()
        self.__draw_clock()
        self.__draw_player_level_bar()

        if GameClockSingleton().game_clock > 180000:
            self.__draw_win_screen(game)

        if dead:
            self.__draw_game_over_screen(game)

        # Update the display
        pygame.display.flip()