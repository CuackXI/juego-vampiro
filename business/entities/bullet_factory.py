from business.entities.interfaces import IBulletFactory, IPerk, IPlayer, IUpdatable
from business.entities.bullet import *
from business.handlers.cooldown_handler import CooldownHandler

class NormalBulletFactory(IBulletFactory, IPerk):
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

        self.__cooldown_handler = CooldownHandler(self.cooldown)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_nearest_enemy(world)
    
    def upgrade(self):
        if self.__level + 1 in NormalBulletFactory.BASE_LEVEL_STATS.keys():
            self.__level += 1
    
    @property
    def upgradable(self):
        return self.__level != 2

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
        bullet = Bullet(world.player.pos_x, world.player.pos_y, monster.pos_x, monster.pos_y, 
        self.speed, self.damage, self.health)
        world.add_bullet(bullet)

class TurretBulletFactory(IBulletFactory, IPerk, IUpdatable):

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

        self.__cooldown_handler = CooldownHandler(self.cooldown)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_nearest_enemy(world)
    
    def upgrade(self):
        if self.__level + 1 in TurretBulletFactory.BASE_LEVEL_STATS.keys():
            self.__level += 1

    @property
    def upgradable(self):
        return self.__level != 2

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
        bullet = TurretBullet(world.player.pos_x, world.player.pos_y, monster.pos_x, monster.pos_y, 
                              self.speed, self.damage, self.health)
        
        world.add_bullet(bullet)

class FollowingBulletFactory(IBulletFactory, IPerk):
    
    pass #bala que persiga a un monstruo