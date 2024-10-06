"""Script containing resource class"""
import image_processing.screen_slicing as screen_slicing
from data.building import Cost


class Resource:
    def __init__(self, name: str, value: int, idx: int, quantity: int,minimal_quantity: Cost = Cost(0,0,0,0,0,0,0)):

        """
        Init funtion for resource

        :param name:
        :param value:
        :param idx:
        :param quantity:
        :param minimal_quantity: minimal value that resource stack can give
        """
        self.name = name
        self.index = idx
        self.value = value
        self.quantity = quantity
        self.minimal_quantity = minimal_quantity

    def __repr__(self):
        return self.name + f' value: ({str(self.value)})'

    def __str__(self):
        return self.name + f' value: ({str(self.value)})'
    # placeholders for end ow week/day function

    def end_day(self, player):
        pass

    def end_week(self, player):
        pass

    def action(self, player, hero):
        """
        function for giving us resources after picking up resource stack

        :param player: player object
        :param hero: hero object
        """
        ranges = ((player.wood-5,player.wood+10),(player.mercury-5,player.mercury+10),(player.ore-5,player.ore+10),(player.sulfur-5,player.sulfur+10),(player.crystal-5,player.crystal+10),(player.gems-5,player.gems+10),(player.gold-100,player.gold+1000))
        screen_slicing.check_resources(player,ranges,self.minimal_quantity,True,self.index)


Gold = Resource("Gold", 0, 6, 0,Cost(300,0,0,0,0,0,0))

Wood = Resource("Wood", 0, 0, 0,Cost(0,5,0,0,0,0,0))

Ore = Resource("Ore", 0, 2, 0,Cost(0,0,5,0,0,0,0))

Mercury = Resource("Mercury", 0, 1, 0,Cost(0,0,0,3,0,0,0))

Sulfur = Resource("Sulfur", 0, 3, 0,Cost(0,0,0,0,3,0,0))

Crystal = Resource("Crystal", 0, 4, 0,Cost(0,0,0,0,0,3,0))

Gems = Resource("Gems", 0, 5, 0,Cost(0,0,0,0,0,0,3))





