import unittest
from unittest.mock import MagicMock
import pygame
from presentation.sprite import Sprite
from business.entities.bullets import FollowingBullet
from business.world.interfaces import IGameWorld
from business.entities.interfaces import IMonster

class TestFollowingBullet(unittest.TestCase):
    class TestMonster(IMonster):
        def __init__(self, pos_x, pos_y):
            self._pos_x = pos_x
            self._pos_y = pos_y
            self._health = 10
            self._max_health = 10
            self._damage_amount = 5
            self._speed = 1.0
            self._sprite = MagicMock(spec=Sprite)

        @property
        def pos_x(self):
            return self._pos_x

        @property
        def pos_y(self):
            return self._pos_y

        @property
        def health(self):
            return self._health

        @property
        def max_health(self):
            return self._max_health

        @property
        def damage_amount(self):
            return self._damage_amount

        @property
        def speed(self):
            return self._speed

        @property
        def sprite(self):
            return self._sprite

        def move(self, dx, dy):
            self._pos_x += dx
            self._pos_y += dy

        def take_damage(self, amount):
            self._health = max(0, self._health - amount)

        def to_json(self):
            return {
                'pos_x': self.pos_x,
                'pos_y': self.pos_y,
                'health': self.health,
                'max_health': self.max_health,
            }

        def update(self):
            pass

    class TestGameWorld(IGameWorld):
        def __init__(self, monsters):
            self._monsters = monsters
            self._bullets = []
            self._items = []

        @property
        def monsters(self):
            return self._monsters

        @property
        def bullets(self):
            return self._bullets

        @property
        def items(self):
            return self._items

        @property
        def player(self):
            return MagicMock()

        @property
        def monster_spawner(self):
            return MagicMock()

        @property
        def display(self):
            return MagicMock()

        @property
        def game(self):
            return MagicMock()
        
        def add_monster(self, monster):
            self._monsters.append(monster)

        def remove_monster(self, monster):
            self._monsters.remove(monster)

        def add_bullet(self, bullet):
            self._bullets.append(bullet)

        def remove_bullet(self, bullet):
            self._bullets.remove(bullet)

        def add_item(self, item):
            self._items.append(item)

        def remove_item(self, item):
            self._items.remove(item)

        def activate_upgrade(self, upgrade):
            pass

        def give_perk_to_player(self, perk):
            pass

        def in_upgrade(self):
            return False
        
        def get_perks_for_display(self):
            return []

        def update(self):
            pass

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)
        self.mock_sprite = MagicMock(spec=Sprite)
        self.target_monster = self.TestMonster(5, 5)
        self.bullet = FollowingBullet(0, 0, self.target_monster, speed=1.0, damage=10, health=10)

    def tearDown(self):
        pygame.quit()

    def test_calculate_direction(self):
        dx, dy = self.bullet._FollowingBullet__calculate_direction(3, 4)
        self.assertAlmostEqual(dx, 0.6)
        self.assertAlmostEqual(dy, 0.8)

    def test_update_moves_towards_monster(self):
        world = self.TestGameWorld([self.target_monster])
        self.bullet.update(world)

        self.assertAlmostEqual(round(self.bullet.pos_x, 1), 0.7)
        self.assertAlmostEqual(round(self.bullet.pos_y, 1), 0.7)

    def test_take_damage(self):
        self.bullet.take_damage(5)
        self.assertEqual(self.bullet.health, 5)

        self.bullet.take_damage(10)
        self.assertEqual(self.bullet.health, 0)

    def test_can_despawn(self):
        self.assertFalse(self.bullet.can_despawn)
        self.bullet._FollowingBullet__despawn_cooldown.last_action_time = 0
        self.bullet._FollowingBullet__despawn_cooldown._CooldownHandler__cooldown_time = 0
        self.assertTrue(self.bullet.can_despawn)

    def test_to_json(self):
        self.bullet.take_damage(5)
        json_data = self.bullet.to_json()
        expected_data = {
            'pos_x': self.bullet.pos_x,
            'pos_y': self.bullet.pos_y,
            'damage': self.bullet.damage_amount,
            'health': 5,
            'speed': self.bullet.speed,
            'despawn_cooldown': self.bullet._FollowingBullet__despawn_cooldown.last_action_time
        }
        self.assertEqual(json_data, expected_data)

if __name__ == '__main__':
    unittest.main()