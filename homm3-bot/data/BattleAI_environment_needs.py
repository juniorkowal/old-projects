"""Script containing creature box class"""
import copy
from colorama import Fore
from data.classes_const import *


# Data structure which contains information about specific creature at specific hex and its
# membership (in which team the creature is) and quantity
# It could be useful in the other parts of BattleAI code (queue, reward function,
# function which tells us about possible moves)
class CreatureBox:
    def __init__(self, creatureType: Creature, hexField: tuple, quantity: int, allied: bool = True,spells = []):
        """
        Class which describes specific unit at the battle view in BattleAI environment. It contains information about
        creature type (Archer, Goblin, Skeleton etc.), about its position at the battlefield, its quantity and
        membership

        :param creatureType: (Creature class) Archer, Goblin, Skeleton etc.
        :param hexField: (tuple) position at the battlefield
        :param quantity: (int) how many units there are
        :param allied: (bool) whether it is allied or hostile creature
        """
        self.type = copy.deepcopy(creatureType)
        self.field = hexField
        self.quantity = int(float(quantity))
        self.ally = allied
        self.stackHP = self.quantity * self.type.hp
        self.prevHP = self.quantity * self.type.hp
        self.waited = False
        self.spells = spells

    def __eq__(self, other):
        if not isinstance(other, CreatureBox):
            return False
        return self.type.name == other.type.name and self.field == other.field and self.quantity == other.quantity \
               and self.ally == other.ally

    def __hash__(self):
        return hash(self.field)

    def __repr__(self):
        return f"{Fore.LIGHTYELLOW_EX}{self.type},{self.field},{self.ally},{self.quantity}\n{Fore.RESET}"

    # For 2hex size units
    def eqLeft(self, other):
        """
        Function which checks position of the 2 hex unit on the battlefield. It tests orientation of the unit.

        :param other: object on the left from the original self object
        :return bool: True if object on the left is the same objects as original self object
        """
        if not isinstance(other, CreatureBox):
            return False
        return self.type.name == other.type.name and self.field[0] - 1 == other.field[0] \
               and self.field[1] == other.field[1] and self.quantity == other.quantity and self.ally == other.ally

    def eqRight(self, other):
        """
        Function which checks position of the 2 hex unit on the battlefield. It tests orientation of the unit.

        :param other: object on the right from the original self object
        :return bool: True if object on the left is the same objects as original self object
        """
        if not isinstance(other, CreatureBox):
            return False
        return self.type.name == other.type.name and self.field[0] + 1 == other.field[0] \
               and self.field[1] == other.field[1] and self.quantity == other.quantity and self.ally == other.ally

    def returnFeatures(self):
        """
        Function which returns list with the most important features of the class instance.

        :return list: list with normalized features (quantity of the unit, its attack, health points, speed, ammunition)
        """
        features = [self.quantity/200,
                    self.type.attack/50,
                    self.type.hp/1000,
                    self.type.speed/21,
                    int(bool(self.type.ammo))]
        return features


# Obstacles (hexes in our environment we cannot move on)
class Obstacle:
    def __init__(self, hexField: tuple):
        """
        Simple class which describes obstacle on the battlefield.

        :param hexField: location of the obstacle
        """
        self.field = hexField
