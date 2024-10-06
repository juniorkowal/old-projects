"""Script containing creature class"""


class Creature:
    def __init__(self,
                 name: str,
                 lvl: int,
                 atc: int,
                 defense: int,
                 dmg: tuple,
                 hp: int,
                 spd: int,
                 value: int,
                 size: int,
                 ammo: int,
                 fly: bool,
                 upgraded: bool,
                 town: str = '',
                 abilities: tuple = None,
                 native_terrain: list = None):
        """
        Class representing creature object.

        :param name: Name of the creature
        :param lvl: level of the creature
        :param atc: Attack attribute
        :param defense: Defense attribute
        :param dmg: Damage of the creature
        :param hp: Health points of the creature
        :param spd: Speed of the creature
        :param value: Value of the creature
        :param size: Size of the unit
        :param ammo: Ammo
        :param fly: Boolean whether it flies or not
        :param upgraded: Boolean whether it is upgraded creature or not
        :param abilities: Tuple containing certain abilities
        """
        self.name = name
        self.lvl = lvl
        self.attack = atc
        self.defense = defense
        self.damage = dmg
        self.hp = hp
        self.value = value
        self.speed = spd
        self.abilities = abilities
        self.ammo = ammo
        self.size = size
        self.fly = fly
        self.native_terrain = native_terrain
        self.ranged = bool(ammo)
        self.upgraded = upgraded
        self.town = town

    def __eq__(self,other):
        if isinstance(other, Creature):
            return self.name == other.name
        else:
            return False

    def __repr__(self):
        return self.name + f' size:({str(self.size)}, value: {str(self.value)})'

    def __str__(self):
        return self.name + f' size:({str(self.size)}, value: {str(self.value)})'


