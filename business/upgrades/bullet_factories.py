from business.entities.interfaces import IPlayer, IUpdatable
from business.upgrades.interfaces import IBulletFactory
from business.entities.bullets import *
from business.handlers.cooldown_handler import CooldownHandler
from presentation.sprite import BulletSprite, TurretBulletSprite, FollowingBulletSprite

class NormalBulletFactory(IBulletFactory):
    BASE_LEVEL_STATS = {
        1: {
            'COOLDOWN': 1000,
            'DAMAGE': 5,
            'SPEED': 4,
            'HEALTH': 100
        },
        2: {
            'COOLDOWN': 750,
            'DAMAGE': 10,
            'SPEED': 10,
            'HEALTH': 100
        }
    }

    def __init__(self, player: IPlayer):
        self.__level = 1
        self.__player = player
        self.__sprite = BulletSprite(0, 0)

        self.__cooldown_handler = CooldownHandler(self.cooldown)

    def load_cooldown(self, amount):
        self.__cooldown_handler.last_action_time = amount

    def to_json(self):
        return {
            'level': self.__level,
            'attack_cooldown': self.__cooldown_handler.last_action_time
        }

    @staticmethod
    def load_bullets(data, world: IGameWorld):
        for bullet_data in data:
            pos_x = bullet_data['pos_x']
            pos_y = bullet_data['pos_y']
            dir_x = bullet_data['dir_x']
            dir_y = bullet_data['dir_y']
            damage = bullet_data['damage']
            health = bullet_data['health']
            speed = bullet_data['speed']

            dst_x = pos_x + dir_x
            dst_y = pos_y + dir_y

            bullet = NormalBullet(pos_x,pos_y,dst_x,dst_y,speed,damage,health)
            world.add_bullet(bullet)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_nearest_enemy(world)
    
    def upgrade(self):
        if self.__level + 1 in NormalBulletFactory.BASE_LEVEL_STATS.keys():
            self.__level += 1
    
    @property
    def sprite(self):
        return self.__sprite

    @property
    def upgradable(self):
        return self.__level != max(NormalBulletFactory.BASE_LEVEL_STATS.keys())

    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__cooldown_handler.put_on_cooldown()
            self.create_bullet(world)

    @property
    def cooldown(self):
        return NormalBulletFactory.BASE_LEVEL_STATS[self.__level]['COOLDOWN']

    @property
    def damage(self):
        return NormalBulletFactory.BASE_LEVEL_STATS[self.__level]['DAMAGE'] * self.__player.damage_multiplier

    @property
    def speed(self):
        return NormalBulletFactory.BASE_LEVEL_STATS[self.__level]['SPEED']
    
    @property
    def health(self):
        return NormalBulletFactory.BASE_LEVEL_STATS[self.__level]['HEALTH']

    def __str__(self) -> str:
        if self in self.__player.inventory:
            return f'ARMA COMUN -> NIVEL {self.__level + 1}'
        
        return "DESBLOQUEAR ARMA COMUN"

    def __shoot_at_nearest_enemy(self, world: IGameWorld):
        if not world.monsters:
            return  # No monsters to shoot at

        # Find the nearest monster
        monster = min(
            world.monsters,
            key=lambda monster: (
                (monster.pos_x - world.player.pos_x) ** 2 + (monster.pos_y - world.player.pos_y) ** 2
            ),
        )

        # Create a bullet towards the nearest monster
        bullet = NormalBullet(world.player.pos_x, world.player.pos_y, monster.pos_x, monster.pos_y, 
        self.speed, self.damage, self.health)
        world.add_bullet(bullet)

    def upgrade_amount(self):
        # Not possible to be implemented
        pass

class TurretBulletFactory(IBulletFactory, IUpdatable):

    BASE_LEVEL_STATS = {
        1: {
            'COOLDOWN': 250,
            'DAMAGE': 1,
            'SPEED': 10,
            'HEALTH': 5
        },
        2: {
            'COOLDOWN': 250,
            'DAMAGE': 5,
            'SPEED': 20,
            'HEALTH': 5
        }
    }

    def __init__(self, player: IPlayer):
        self.__level = 1
        self.__player = player
        self.__sprite = TurretBulletSprite(0, 0)

        self.__cooldown_handler = CooldownHandler(self.cooldown)

    def load_cooldown(self, amount):
        self.__cooldown_handler.last_action_time = amount

    def to_json(self):
        return {
            'level': self.__level,
            'attack_cooldown': self.__cooldown_handler.last_action_time
        }

    @staticmethod
    def load_bullets(data, world: IGameWorld):
        for bullet_data in data:
            pos_x = bullet_data['pos_x']
            pos_y = bullet_data['pos_y']
            dir_x = bullet_data['dir_x']
            dir_y = bullet_data['dir_y']
            damage = bullet_data['damage']
            health = bullet_data['health']
            speed = bullet_data['speed']

            dst_x = pos_x + dir_x
            dst_y = pos_y + dir_y

            bullet = TurretBullet(pos_x,pos_y,dst_x,dst_y,speed,damage,health)
            world.add_bullet(bullet)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_nearest_enemy(world)
    
    def upgrade(self):
        if self.__level + 1 in TurretBulletFactory.BASE_LEVEL_STATS.keys():
            self.__level += 1

    @property
    def sprite(self):
        return self.__sprite

    @property
    def upgradable(self):
        return self.__level != max(TurretBulletFactory.BASE_LEVEL_STATS.keys())

    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__cooldown_handler.put_on_cooldown()
            self.create_bullet(world)

    @property
    def cooldown(self):
        return TurretBulletFactory.BASE_LEVEL_STATS[self.__level]['COOLDOWN']

    @property
    def damage(self):
        return TurretBulletFactory.BASE_LEVEL_STATS[self.__level]['DAMAGE'] * self.__player.damage_multiplier

    @property
    def speed(self):
        return TurretBulletFactory.BASE_LEVEL_STATS[self.__level]['SPEED']
    
    @property
    def health(self):
        return TurretBulletFactory.BASE_LEVEL_STATS[self.__level]['HEALTH']

    def __str__(self) -> str:
        if self in self.__player.inventory:
            return f'TORRETA -> NIVEL {self.__level + 1}'
        
        return 'DESBLOQUEAR TORRETA'

    def __shoot_at_nearest_enemy(self, world: IGameWorld):
        if not world.monsters:
            return  # No monsters to shoot at

        # Find the nearest monster
        monster = min(
            world.monsters,
            key=lambda monster: (
                (monster.pos_x - world.player.pos_x) ** 2 + (monster.pos_y - world.player.pos_y) ** 2
            ),
        )

        # Create a bullet towards the nearest monster
        bullet = TurretBullet(
            world.player.pos_x, world.player.pos_y, monster.pos_x, monster.pos_y, self.speed, self.damage, self.health)
        
        world.add_bullet(bullet)

    def upgrade_amount(self):
        # Not possible to be implemented
        pass

class FollowingBulletFactory(IBulletFactory, IUpdatable):
    
    BASE_LEVEL_STATS = {
        1: {
            'COOLDOWN': 2000,
            'DAMAGE': 10,
            'SPEED': 5,
            'HEALTH': 2000
        },
        2: {
            'COOLDOWN': 5000,
            'DAMAGE': 10,
            'SPEED': 5,
            'HEALTH': 200
        }
    }

    def __init__(self, player: IPlayer):
        self.__level = 1
        self.__player = player
        self.__sprite = FollowingBulletSprite(0, 0)

        self.__cooldown_handler = CooldownHandler(self.cooldown)

    def load_cooldown(self, amount):
        self.__cooldown_handler.last_action_time = amount

    def to_json(self):
        return {
            'level': self.__level,
            'attack_cooldown': self.__cooldown_handler.last_action_time
        }

    @staticmethod
    def load_bullets(data, world: IGameWorld):
        for bullet_data in data:
            pos_x = bullet_data['pos_x']
            pos_y = bullet_data['pos_y']
            damage = bullet_data['damage']
            health = bullet_data['health']
            speed = bullet_data['speed']
            cooldown = bullet_data['despawn_cooldown']

            bullet = FollowingBullet(pos_x, pos_y, None, speed, damage, health, cooldown)
            world.add_bullet(bullet)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_nearest_enemy(world)
    
    def upgrade(self):
        if self.__level + 1 in FollowingBulletFactory.BASE_LEVEL_STATS.keys():
            self.__level += 1

    @property
    def sprite(self):
        return self.__sprite

    @property
    def upgradable(self):
        return self.__level != max(FollowingBulletFactory.BASE_LEVEL_STATS.keys())

    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__cooldown_handler.put_on_cooldown()
            self.create_bullet(world)

    @property
    def cooldown(self):
        return FollowingBulletFactory.BASE_LEVEL_STATS[self.__level]['COOLDOWN']

    @property
    def damage(self):
        return FollowingBulletFactory.BASE_LEVEL_STATS[self.__level]['DAMAGE'] * self.__player.damage_multiplier

    @property
    def speed(self):
        return FollowingBulletFactory.BASE_LEVEL_STATS[self.__level]['SPEED']
    
    @property
    def health(self):
        return FollowingBulletFactory.BASE_LEVEL_STATS[self.__level]['HEALTH']

    def __str__(self) -> str:
        if self in self.__player.inventory:
            return f'ARMA TELEDERIGIDA -> NIVEL {self.__level + 1}'
        
        return 'DESBLOQUEAR ARMA TELEDERIGIDA'

    def __shoot_at_nearest_enemy(self, world: IGameWorld):
        if not world.monsters:
            return

        monster = min(
            world.monsters,
            key=lambda monster: (
                (monster.pos_x - world.player.pos_x) ** 2 + (monster.pos_y - world.player.pos_y) ** 2
            ),
        )   

        try:
            bullet = FollowingBullet(world.player.pos_x, world.player.pos_y, monster, self.speed, self.damage, self.health)
        except Exception as error:
            print(error)

        world.add_bullet(bullet)

    def upgrade_amount(self):
        # Not possible to be implemented
        pass
