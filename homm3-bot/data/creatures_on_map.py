"""Script containing classes representing creatures on map"""
from data.creature import Creature


class Unit:
    def __init__(self, unit: Creature = Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, ("", "")), amount=0):
        """
        Class representing singular unit -> creature object

        :param unit: Creature object
        :param amount: (Int) amount of given unit
        """
        self.unit = unit
        self.amount = amount
        self.value = unit.value


class Units:
    def __init__(self, s1: Unit = Unit(), s2: Unit = Unit(), s3: Unit = Unit(), s4: Unit = Unit(), s5: Unit = Unit(),
                 s6: Unit = Unit(), s7: Unit = Unit()):
        """
        Class representing units. Unit can have up to 7 unit classes

        :param s1: Unit in slot 1
        :param s2: Unit in slot 2
        :param s3: Unit in slot 3
        :param s4: Unit in slot 4
        :param s5: Unit in slot 5
        :param s6: Unit in slot 6
        :param s7: Unit in slot 7
        """
        self.slots = [s1, s2, s3, s4, s5, s6, s7]
