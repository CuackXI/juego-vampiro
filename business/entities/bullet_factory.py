from business.entities.interfaces import IBulletFactory, IPerk, IPlayer
from business.entities.bullet import *
from business.handlers.cooldown_handler import CooldownHandler

class NormalBulletFactory(IBulletFactory, IPerk):
    BASE_COOLDOWN = 1000
    BASE_DAMAGE = 5
    BASE_SPEED = 4
    BASE_HEALTH = 100

    def __init__(self, player: IPlayer):
        self.__damage = NormalBulletFactory.BASE_DAMAGE
        self.__speed = NormalBulletFactory.BASE_SPEED
        self.__cooldown = NormalBulletFactory.BASE_COOLDOWN
        self.__health = NormalBulletFactory.BASE_HEALTH
        self.__player = player

        self.__cooldown_handler = CooldownHandler(self.__cooldown)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_nearest_enemy(world)
    
    def upgrade(self):
        return super().upgrade()
    
    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__cooldown_handler.put_on_cooldown()
            self.create_bullet(world)

    @property
    def damage_amount(self):
        return self.__damage * self.__player.damage_multiplier

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
        bullet = Bullet(world.player.pos_x, world.player.pos_y, monster.pos_x, monster.pos_y, self.__speed, self.damage_amount,
                        self.__health)
        world.add_bullet(bullet)

class TurretBulletFactory(IBulletFactory, IPerk):
    BASE_COOLDOWN = 250
    BASE_DAMAGE = 1
    BASE_SPEED = 10
    BASE_HEALTH = 5

    def __init__(self, player: IPlayer):
        self.__damage = TurretBulletFactory.BASE_DAMAGE
        self.__speed = TurretBulletFactory.BASE_SPEED
        self.__cooldown = TurretBulletFactory.BASE_COOLDOWN
        self.__health = TurretBulletFactory.BASE_HEALTH
        self.__player = player

        self.__cooldown_handler = CooldownHandler(self.__cooldown)

    def create_bullet(self, world: IGameWorld):
        self.__shoot_at_nearest_enemy(world)
    
    def upgrade(self):
        return super().upgrade()
    
    def update(self, world: IGameWorld):
        if self.__cooldown_handler.is_action_ready():
            self.__cooldown_handler.put_on_cooldown()
            self.create_bullet(world)

    @property
    def damage_amount(self):
        return self.__damage * self.__player.damage_multiplier

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
        bullet = TurretBullet(world.player.pos_x, world.player.pos_y, monster.pos_x, monster.pos_y, self.__speed, self.damage_amount,
                        self.__health)
        world.add_bullet(bullet)