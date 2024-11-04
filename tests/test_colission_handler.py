import unittest
from unittest.mock import Mock, create_autospec
from business.entities.interfaces import IBullet, IMonster, IPlayer, IItem
from business.entities.monsters.interfaces import IMonsterBullet
from business.world.interfaces import IGameWorld
from business.handlers.colission_handler import CollisionHandler

class TestCollisionHandler(unittest.TestCase):

    def setUp(self):
        self.player = create_autospec(IPlayer)
        self.world = create_autospec(IGameWorld)
    
        self.bullet = create_autospec(IBullet)
        self.bullet.damage_amount = 10
        
        self.monster = create_autospec(IMonster)
        self.monster.take_damage = Mock()
        
        self.item = create_autospec(IItem)
        
        self.bullet.sprite = Mock()
        self.bullet.sprite.rect = Mock()
        self.bullet.sprite.rect.colliderect = Mock(return_value=False)
        
        self.monster.sprite = Mock()
        self.monster.sprite.rect = Mock()
        self.monster.sprite.rect.colliderect = Mock(return_value=False)
        
        self.player.sprite = Mock()
        self.player.sprite.rect = Mock()
        self.player.sprite.rect.colliderect = Mock(return_value=False)
        
        self.world.bullets = [self.bullet]
        self.world.monsters = [self.monster]
        self.world.player = self.player
        self.world.items = [self.item]

    def test_bullet_monster_collision(self):
        self.bullet.sprite.rect.colliderect.return_value = True
        self.monster.sprite.rect.colliderect.return_value = True
        
        CollisionHandler._CollisionHandler__handle_bullets(self.world.bullets, self.world.monsters, self.world.player)

        self.monster.take_damage.assert_called_with(self.bullet.damage_amount)
        self.bullet.take_damage.assert_called_with(self.bullet.damage_amount)

    def test_bullet_player_collision(self):
        self.bullet.sprite.rect.colliderect.return_value = True
        self.bullet = create_autospec(IMonsterBullet)
        self.bullet.damage_amount = 10
        self.world.bullets = [self.bullet]

        CollisionHandler._CollisionHandler__handle_bullets(self.world.bullets, self.world.monsters, self.world.player)

        self.player.take_damage.assert_called_with(self.bullet.damage_amount)
        self.bullet.take_damage.assert_called_with(self.bullet.damage_amount)

    def test_item_pickup(self):
        self.item.in_player_range = Mock(return_value=True)
        
        self.player.pickup_item = Mock()

        CollisionHandler._CollisionHandler__handle_items([self.item], self.player, self.world)

        self.player.pickup_item.assert_called_once_with(self.item, self.world)
        self.world.remove_item.assert_called_once_with(self.item)

    def test_no_collision_with_no_bullets(self):
        self.world.bullets = []
        
        CollisionHandler._CollisionHandler__handle_bullets([], self.world.monsters, self.world.player)

        self.monster.take_damage.assert_not_called()
        self.player.take_damage.assert_not_called()

    def test_no_item_pickup_if_not_in_range(self):
        self.item.in_player_range = Mock(return_value=False)
        
        CollisionHandler._CollisionHandler__handle_items([self.item], self.player, self.world)

        self.player.pickup_item.assert_not_called()
        self.world.remove_item.assert_not_called()

if __name__ == '__main__':
    unittest.main()
