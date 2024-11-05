"""Module for item factory for a certain world."""

from business.entities.items.interfaces import IItemFactory
from business.entities.items.experience_gem import *
from business.entities.items.guaymallen import *
from business.world.interfaces import IGameWorld

class ItemFactory(IItemFactory):
    """Item factory that creates instances of all the possible items."""

    COMMON_GEM = "CommonGem"
    RED_GEM = "RedGem"
    GREEN_GEM = "GreenGem"
    BLUE_GEM = "BlueGem"
    GUAYMALLEN = "Guaymallen"

    @staticmethod
    def create_item(type: str, entity: Entity, world: IGameWorld, xp_amount = None):

        if type == ItemFactory.COMMON_GEM:
            world.add_item(ExperienceGem(entity.pos_x, entity.pos_y, xp_amount))

        elif type == ItemFactory.RED_GEM:
            world.add_item(RedExperienceGem(entity.pos_x, entity.pos_y, xp_amount))

        elif type == ItemFactory.GREEN_GEM:
            world.add_item(GreenExperienceGem(entity.pos_x, entity.pos_y, xp_amount))

        elif type == ItemFactory.BLUE_GEM:
            world.add_item(BlueExperienceGem(entity.pos_x, entity.pos_y, xp_amount))

        elif type == ItemFactory.GUAYMALLEN:
            world.add_item(Guaymallen(entity.pos_x, entity.pos_y))

    @staticmethod
    def load_items(world: IGameWorld, saved_data: dict):
        saved_data = saved_data.get('items')

        for item_type in saved_data:
            if 'experience_gem.ExperienceGem' in item_type:
                for gem_data in saved_data[item_type]:
                    pos_x = gem_data['pos_x']
                    pos_y = gem_data['pos_y']
                    amount = gem_data['amount']
                    cooldown = gem_data['despawn_cooldown']

                    world.add_item(ExperienceGem(pos_x, pos_y, amount, cooldown))
            elif 'Red' in item_type:
                for gem_data in saved_data[item_type]:
                    pos_x = gem_data['pos_x']
                    pos_y = gem_data['pos_y']
                    amount = gem_data['amount']
                    cooldown = gem_data['despawn_cooldown']

                    world.add_item(RedExperienceGem(pos_x, pos_y, amount, cooldown))
            elif 'Green' in item_type:
                for gem_data in saved_data[item_type]:
                    pos_x = gem_data['pos_x']
                    pos_y = gem_data['pos_y']
                    amount = gem_data['amount']
                    cooldown = gem_data['despawn_cooldown']

                    world.add_item(GreenExperienceGem(pos_x, pos_y, amount, cooldown))
            elif 'Blue' in item_type:
                for gem_data in saved_data[item_type]:
                    pos_x = gem_data['pos_x']
                    pos_y = gem_data['pos_y']
                    amount = gem_data['amount']
                    cooldown = gem_data['despawn_cooldown']

                    world.add_item(BlueExperienceGem(pos_x, pos_y, amount, cooldown))

            elif 'Guaymallen' in item_type:
                for gem_data in saved_data[item_type]:
                    pos_x = gem_data['pos_x']
                    pos_y = gem_data['pos_y']

                    world.add_item(Guaymallen(pos_x, pos_y))               