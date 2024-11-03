"""Module for the Sprite class."""

import pygame

import settings
from presentation.tileset import Tileset


class Sprite(pygame.sprite.Sprite):
    """A class representing a sprite."""

    def __init__(self, image: pygame.Surface, rect: pygame.Rect, *groups):
        self._image: pygame.Surface = image
        self._rect: pygame.Rect = rect
        super().__init__(*groups)
        self.__is_in_damage_countdown = 0
        self.__is_in_heal_countdown = 0
        self.__original_image: pygame.Surface = image

    @property
    def image(self) -> pygame.Surface:
        """The image of the sprite."""
        return self._image

    @property
    def rect(self) -> pygame.Rect:
        """The rect of the sprite."""
        return self._rect

    def update_pos(self, pos_x: float, pos_y: float):
        """Update the position of the sprite."""
        self._rect.center = (int(pos_x), int(pos_y))

    def __restore_image(self):
        self._image = self.__original_image.copy()

    def __change_color(self, color: tuple[int, int, int]):
        self._image = self.__original_image.copy()
        self._image.fill(color, special_flags=pygame.BLEND_MULT)
        self._image.set_colorkey((0, 0, 0))

    def __decrease_damage_countdown(self):
        self.__is_in_damage_countdown -= 1
        if self.__is_in_damage_countdown <= 0:
            self.__is_in_damage_countdown = 0
            self.__restore_image()

    def __decrease_heal_countdown(self):
        self.__is_in_heal_countdown -= 1
        if self.__is_in_heal_countdown <= 0:
            self.__is_in_heal_countdown = 0
            self.__restore_image()

    def take_damage(self):
        """Take damage."""
        self.__change_color((255, 0, 0))
        self.__is_in_damage_countdown = 20

    def heal(self):
        """Heal the player by turning the sprite green for 0.2 seconds."""
        self.__change_color((0, 255, 0))

        self.__is_in_heal_countdown = 24

    def update(self, *args, **kwargs):
        """Update the sprite behavior."""
        super().update(*args, **kwargs)
        if self.__is_in_damage_countdown > 0:
            self.__decrease_damage_countdown()
        if self.__is_in_heal_countdown > 0:
            self.__decrease_heal_countdown()

class PlayerSprite(Sprite):
    """A class representing the player sprite."""

    ASSET = "./assets/adventurer-idle-00.png"

    def __init__(self, pos_x: float, pos_y: float):
        image: pygame.Surface = pygame.image.load(PlayerSprite.ASSET).convert_alpha()
        image = pygame.transform.scale(image, settings.TILE_DIMENSION)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)


class MonsterSprite(Sprite):
    """A class representing the monster sprite."""

    ASSET = "./assets/monster.png"

    def __init__(self, pos_x: float, pos_y: float, size: float):
        image = pygame.image.load(MonsterSprite.ASSET).convert_alpha()
        original_width, original_height = image.get_size()

        new_width = int(original_width * size)
        new_height = int(original_height * size)

        image = pygame.transform.scale(image, (new_width, new_height))
        rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)

class BossMonsterSprite(Sprite):
    """A class representing the boss monster sprite."""

    ASSET = "./assets/boss1.png"

    def __init__(self, pos_x: float, pos_y: float, size: float):
        image = pygame.image.load(BossMonsterSprite.ASSET).convert_alpha()
        original_width, original_height = image.get_size()

        new_width = int(original_width * size)
        new_height = int(original_height * size)

        image = pygame.transform.scale(image, (new_width, new_height))
        rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)

class BulletSprite(Sprite):
    """A class representing the bullet sprite."""

    def __init__(self, pos_x: float, pos_y: float):
        image_size = 30

        image = pygame.Surface((image_size, image_size), pygame.SRCALPHA)  # pylint: disable=E1101
        pygame.draw.circle(image, (255, 255, 0), (image_size // 2, image_size // 2), image_size // 2)
        rect: pygame.rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)
    
class TurretBulletSprite(Sprite):
    """A class representing the bullet sprite."""

    def __init__(self, pos_x: float, pos_y: float):
        image_size = 20
        image = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
        pygame.draw.circle(image, (255, 100, 100), (image_size // 2, image_size // 2), image_size // 2)

        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)

class FollowingBulletSprite(Sprite):
    """A class representing the bullet sprite."""

    def __init__(self, pos_x: float, pos_y: float):
        image_size = 40
        image = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
        pygame.draw.circle(image, (0, 0, 0), (image_size // 2, image_size // 2), image_size // 2)

        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)

class ExperienceGemSprite(Sprite):
    """A class representing the experience gem sprite."""

    ASSET = "./assets/experience_gems.png"

    def __init__(self, pos_x: float, pos_y: float):
        tileset = Tileset(
            ExperienceGemSprite.ASSET, settings.TILE_HEIGHT, settings.TILE_HEIGHT, 2, 2
        )
        image: pygame.Surface = tileset.get_tile(3)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)

class GuaymallenSprite(Sprite):
    """A class representing the guaymallen sprite."""

    ASSET = "./assets/guaymallen.webp"

    def __init__(self, pos_x: float, pos_y: float):
        tileset = Tileset(
            GuaymallenSprite.ASSET, settings.TILE_HEIGHT, settings.TILE_HEIGHT, 1, 1
        )
        image: pygame.Surface = tileset.get_tile(0)
        rect: pygame.Rect = image.get_rect(center=(int(pos_x), int(pos_y)))

        super().__init__(image, rect)