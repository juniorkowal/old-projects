"""Script containing dataclass Guard Reward and Creature Bank class and objects and also reward class"""

import time

import GUI_handling.AdventureGUI
from data.building import *
from data.classes_const import *
from data.hero import Slots, Slot
from dataclasses import dataclass
from image_processing.detecting_window import execute_detecting


class Reward(Cost):
    def __init__(self, cost: Cost, xp: int, units: Slots):
        """
        Init function of the Reward for the creature bank class

        :param cost:
        :param xp:
        :param units:
        """
        super().__init__(cost.gold, cost.wood,cost.ore,cost.mercury,cost.sulfur,cost.crystal,cost.gems)
        self.xp = xp
        self.units = units


@dataclass
class Guard_Reward:
    guard: Slots
    reward: Reward


class Creature_Bank:
    def __init__(self, value: int, name: str, visited: bool = False, *pair: Guard_Reward):
        """
        Init function of the Creature Bank Class.

        :param value: Value assigned to Creature Bank
        :param name: Name of the creature bank
        :param visited: Boolean. Visited -> True else False
        :param pair:
        """
        self.value = value
        self.name = name
        self.visited = visited
        self.guard_reward = pair

    def __repr__(self):
        return self.name + f' value: ({str(self.value)})'

    def __str__(self):
        return self.name + f' value: ({str(self.value)})'
    # placeholders for end ow week/day function
    def end_day(self, player):
        """
        end day buffer function

        :param player: player object
        """
        pass

    def end_week(self, player):
        """
        end day buffer function

        :param player: player object
        """
        pass

    def action(self,player,hero, okvalue):
        """
        Action function assosiated with handling creature banks window

        :param player: player object
        :param hero: hero object
        """
        GUI_handling.AdventureGUI.accept_offer()
        time.sleep(0.1)
        execute_detecting(hero)
        time.sleep(0.1)
        GUI_handling.AdventureGUI.accept_offer() # temporary solution



Crypt = Creature_Bank(1000, "Crypt", False,
                      Guard_Reward(Slots(Slot(Skeleton, 30), Slot(Walking_Dead, 20)), Reward(Cost(1500, 0, 0, 0, 0, 0, 0), 480, Slots())),
                      Guard_Reward(Slots(Slot(Skeleton, 25), Slot(Walking_Dead, 20), Slot(Wight, 5)), Reward(Cost(2000, 0, 0, 0, 0, 0, 0), 540, Slots())),
                      Guard_Reward(Slots(Slot(Skeleton, 20), Slot(Walking_Dead, 20), Slot(Wight, 10),Slot(Vampire, 5)), Reward(Cost(2500, 0, 0, 0, 0, 0, 0), 750, Slots())),
                      Guard_Reward(Slots(Slot(Skeleton, 20), Slot(Walking_Dead, 20), Slot(Wight, 10),Slot(Vampire, 10)), Reward(Cost(5000, 0, 0, 0, 0, 0, 0), 900, Slots())))

Cyclops_Stockpile = Creature_Bank(3000, "Cyclops_Stockpile", False,
                                Guard_Reward(Slots(Slot(Cyclops,16),Slot(Cyclops_King,4)),Reward(Cost(0, 4, 4, 4, 4, 4, 4), 1400, Slots())),
                                Guard_Reward(Slots(Slot(Cyclops,24),Slot(Cyclops_King,6)),Reward(Cost(0, 6, 6, 6, 6, 6, 6), 2100, Slots())),
                                Guard_Reward(Slots(Slot(Cyclops,32),Slot(Cyclops_King,8)),Reward(Cost(0, 8, 8, 8, 8, 8, 8), 2800, Slots())),
                                Guard_Reward(Slots(Slot(Cyclops,40),Slot(Cyclops_King,10)),Reward(Cost(0, 10, 10, 10, 10, 10, 10), 3500, Slots())))

Derelict_Ship = Creature_Bank(4000, "Derelict_Ship", False,
                                Guard_Reward(Slots(Slot(Water_Elemental,20)),Reward(Cost(3000, 0, 0, 0, 0, 0, 0), 600, Slots())),
                                Guard_Reward(Slots(Slot(Water_Elemental,30)),Reward(Cost(3000, 0, 0, 0, 0, 0, 0), 900, Slots())),
                                Guard_Reward(Slots(Slot(Water_Elemental,40)),Reward(Cost(4000, 0, 0, 0, 0, 0, 0), 1200, Slots())),
                                Guard_Reward(Slots(Slot(Water_Elemental,60)),Reward(Cost(6000, 0, 0, 0, 0, 0, 0), 1800, Slots())))


Dragon_Fly_Hive = Creature_Bank(9000, "Dragon_Fly_Hive", False,
                                Guard_Reward(Slots(Slot(Dragon_Fly,30)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 600, Slots(Slot(Wyvern,4)))),
                                Guard_Reward(Slots(Slot(Dragon_Fly,45)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 900, Slots(Slot(Wyvern,6)))),
                                Guard_Reward(Slots(Slot(Dragon_Fly,60)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1200, Slots(Slot(Wyvern,8)))),
                                Guard_Reward(Slots(Slot(Dragon_Fly,90)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1800, Slots(Slot(Wyvern,12)))))


Dragon_Utopia = Creature_Bank(10000, "Dragon_Utopia", False,
                Guard_Reward(Slots(Slot(Green_Dragon,8),Slot(Red_Dragon,5),Slot(Gold_Dragon,2),Slot(Black_Dragon,1)),Reward(Cost(20000, 0, 0, 0, 0, 0, 0), 3140, Slots())),
                Guard_Reward(Slots(Slot(Green_Dragon,8),Slot(Red_Dragon,6),Slot(Gold_Dragon,3),Slot(Black_Dragon,2)),Reward(Cost(30000, 0, 0, 0, 0, 0, 0), 3870, Slots())),
                Guard_Reward(Slots(Slot(Green_Dragon,8),Slot(Red_Dragon,6),Slot(Gold_Dragon,4),Slot(Black_Dragon,3)),Reward(Cost(40000, 0, 0, 0, 0, 0, 0), 4420, Slots())),
                Guard_Reward(Slots(Slot(Green_Dragon,8),Slot(Red_Dragon,7),Slot(Gold_Dragon,6),Slot(Black_Dragon,5)),Reward(Cost(50000, 0, 0, 0, 0, 0, 0), 5700, Slots())))


Dwarven_Treasury = Creature_Bank(2000, "Dwarven_Treasury", False,
                    Guard_Reward(Slots(Slot(Dwarf,40),Slot(Battle_Dwarf,10)),Reward(Cost(2500, 0, 0, 0, 0, 2, 0), 1000, Slots())),
                    Guard_Reward(Slots(Slot(Dwarf,60),Slot(Battle_Dwarf,15)),Reward(Cost(4000, 0, 0, 0, 0, 3, 0), 1500, Slots())),
                    Guard_Reward(Slots(Slot(Dwarf,80),Slot(Battle_Dwarf,20)),Reward(Cost(5000, 0, 0, 0, 0, 5, 0), 2000, Slots())),
                    Guard_Reward(Slots(Slot(Dwarf,40),Slot(Battle_Dwarf,10)),Reward(Cost(7500, 0, 0, 0, 0, 10, 0), 3000, Slots())))


Griffin_Conservatory = Creature_Bank(2000, "Griffin_Conservatory", False,
                        Guard_Reward(Slots(Slot(Griffin,40),Slot(Royal_Griffin,10)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1250, Slots(Slot(Angel,1)))),
                        Guard_Reward(Slots(Slot(Griffin,80),Slot(Royal_Griffin,20)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 2500, Slots(Slot(Angel,2)))),
                        Guard_Reward(Slots(Slot(Griffin,120),Slot(Royal_Griffin,30)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 3750, Slots(Slot(Angel,3)))),
                        Guard_Reward(Slots(Slot(Griffin,160),Slot(Royal_Griffin,40)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 5000, Slots(Slot(Angel,4)))))


Imp_Cache = Creature_Bank(5000, "Imp_Cache", False,
                            Guard_Reward(Slots(Slot(Imp,80),Slot(Familiar,20)),Reward(Cost(1000, 0, 0, 2, 0, 0, 0), 400, Slots())),
                            Guard_Reward(Slots(Slot(Imp,120),Slot(Familiar,30)),Reward(Cost(1500, 0, 0, 3, 0, 0, 0), 600, Slots())),
                            Guard_Reward(Slots(Slot(Imp,160),Slot(Familiar,40)),Reward(Cost(2000, 0, 0, 4, 0, 0, 0), 800, Slots())),
                            Guard_Reward(Slots(Slot(Imp,240),Slot(Familiar,60)),Reward(Cost(3000, 0, 0, 6, 0, 0, 0), 1200, Slots())))


Medusa_Stores = Creature_Bank(1500, "Medusa_Stores", False,
                                Guard_Reward(Slots(Slot(Medusa,16),Slot(Medusa_Queen,4)),Reward(Cost(2000, 0, 0, 0, 5, 0, 0), 500, Slots())),
                                Guard_Reward(Slots(Slot(Medusa,24),Slot(Medusa_Queen,6)),Reward(Cost(3000, 0, 0, 0, 6, 0, 0), 750, Slots())),
                                Guard_Reward(Slots(Slot(Medusa,32),Slot(Medusa_Queen,8)),Reward(Cost(4000, 0, 0, 0, 8, 0, 0), 1000, Slots())),
                                Guard_Reward(Slots(Slot(Medusa,40),Slot(Medusa_Queen,10)),Reward(Cost(5000, 0, 0, 0, 10, 0, 0), 1250, Slots())))


Naga_Bank = Creature_Bank(3000, "Naga_Bank", False,
                            Guard_Reward(Slots(Slot(Naga,8),Slot(Naga_Queen,2)),Reward(Cost(4000, 0, 0, 0, 0, 0, 8), 1100, Slots())),
                            Guard_Reward(Slots(Slot(Naga,12),Slot(Naga_Queen,3)),Reward(Cost(6000, 0, 0, 0, 0, 0, 12), 1650, Slots())),
                            Guard_Reward(Slots(Slot(Naga,16),Slot(Naga_Queen,4)),Reward(Cost(8000, 0, 0, 0, 0, 0, 16), 2200, Slots())),
                            Guard_Reward(Slots(Slot(Naga,24),Slot(Naga_Queen,6)),Reward(Cost(12000, 0, 0, 0, 0, 0, 24), 3300, Slots())))


Shipwreck = Creature_Bank(2000, "Shipwreck", False,
                            Guard_Reward(Slots(Slot(Wight,10)),Reward(Cost(2000, 0, 0, 0, 0, 0, 0), 180, Slots())),
                            Guard_Reward(Slots(Slot(Wight,15)),Reward(Cost(3000, 0, 0, 0, 0, 0, 0), 270, Slots())),
                            Guard_Reward(Slots(Slot(Wight,25)),Reward(Cost(4000, 0, 0, 0, 0, 0, 0), 450, Slots())),
                            Guard_Reward(Slots(Slot(Wight,50)),Reward(Cost(5000, 0, 0, 0, 0, 0, 0), 900, Slots())))


# Hota cb

Beholders_Sanctuary = Creature_Bank(2500, "Beholders_Sanctuary", False,
                                    Guard_Reward(Slots(Slot(Beholder,40),Slot(Evil_Eye,10)),Reward(Cost(3000, 0, 0, 0, 0, 0, 0), 1100, Slots())),
                                    Guard_Reward(Slots(Slot(Beholder,60),Slot(Evil_Eye,15)),Reward(Cost(5000, 0, 0, 0, 0, 0, 0), 1650, Slots())),
                                    Guard_Reward(Slots(Slot(Beholder,80),Slot(Evil_Eye,20)),Reward(Cost(6000, 0, 0, 0, 0, 0, 0), 2200, Slots())),
                                    Guard_Reward(Slots(Slot(Beholder,120),Slot(Evil_Eye,30)),Reward(Cost(9000, 0, 0, 0, 0, 0, 0), 3300, Slots())))


Black_Tower = Creature_Bank(1500, "Black_Tower", False,
                            Guard_Reward(Slots(Slot(Green_Dragon,1)),Reward(Cost(2000, 0, 0, 0, 0, 0, 0), 180, Slots())),
                            Guard_Reward(Slots(Slot(Red_Dragon,1)),Reward(Cost(2250, 0, 0, 0, 0, 0, 0), 180, Slots())),
                            Guard_Reward(Slots(Slot(Gold_Dragon,1)),Reward(Cost(3500, 0, 0, 0, 0, 0, 0), 250, Slots())),
                            Guard_Reward(Slots(Slot(Black_Dragon,1)),Reward(Cost(3750, 0, 0, 0, 0, 0, 0), 300, Slots())))


Churchyard = Creature_Bank(1500, "Churchyard", False,
                            Guard_Reward(Slots(Slot(Zombie,90)),Reward(Cost(2500, 0, 0, 0, 0, 0, 0), 1800, Slots())),
                            Guard_Reward(Slots(Slot(Zombie,90)),Reward(Cost(2500, 0, 0, 0, 0, 0, 0), 1800, Slots())),
                            Guard_Reward(Slots(Slot(Zombie,90)),Reward(Cost(2500, 0, 0, 0, 0, 0, 0), 1800, Slots())),
                            Guard_Reward(Slots(Slot(Zombie,90)),Reward(Cost(2500, 0, 0, 0, 0, 0, 0), 1800, Slots())))


Experimental_Shop = Creature_Bank(3500, "Experimental_Shop", False,
                                Guard_Reward(Slots(Slot(Steel_Golem,25)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1125, Slots(Slot(Giant,1)))),
                                Guard_Reward(Slots(Slot(Steel_Golem,50)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 2250, Slots(Slot(Giant,2)))),
                                Guard_Reward(Slots(Slot(Steel_Golem,75)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 3375, Slots(Slot(Giant,3)))),
                                Guard_Reward(Slots(Slot(Steel_Golem,100)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 4500, Slots(Slot(Giant,4)))))


Ivory_Tower = Creature_Bank(7000, "Ivory_Tower", False,
                                Guard_Reward(Slots(Slot(Arch_Mage,35)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1050, Slots(Slot(Enchanter,3)))),
                                Guard_Reward(Slots(Slot(Arch_Mage,50)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1500, Slots(Slot(Enchanter,6)))),
                                Guard_Reward(Slots(Slot(Arch_Mage,65)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1950, Slots(Slot(Enchanter,9)))),
                                Guard_Reward(Slots(Slot(Arch_Mage,80)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 2400, Slots(Slot(Enchanter,12)))))


Mansion = Creature_Bank(5000, "Mansion", False,
                        Guard_Reward(Slots(Slot(Vampire_Lord,40)),Reward(Cost(2500, 0, 0, 2, 2, 2, 2), 1600, Slots())),
                        Guard_Reward(Slots(Slot(Vampire_Lord,60)),Reward(Cost(5000, 0, 0, 3, 3, 3, 3), 2400, Slots())),
                        Guard_Reward(Slots(Slot(Vampire_Lord,80)),Reward(Cost(7500, 0, 0, 4, 4, 4, 4), 3200, Slots())),
                        Guard_Reward(Slots(Slot(Vampire_Lord,100)),Reward(Cost(10000, 0, 0, 5, 5, 5, 5), 4000, Slots())))


Pirate_Cavern = Creature_Bank(3500, "Pirate_Cavern", False,
                                Guard_Reward(Slots(Slot(Pirate,20),Slot(Corsair,20)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 600, Slots(Slot(Sea_Serpent,1)))),
                                Guard_Reward(Slots(Slot(Pirate,40),Slot(Corsair,40)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1200, Slots(Slot(Sea_Serpent,2)))),
                                Guard_Reward(Slots(Slot(Pirate,60),Slot(Corsair,60)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1800, Slots(Slot(Sea_Serpent,3)))),
                                Guard_Reward(Slots(Slot(Pirate,80),Slot(Corsair,80)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 2400, Slots(Slot(Sea_Serpent,4)))))


Red_Tower = Creature_Bank(4000, "Red_Tower", False,
                            Guard_Reward(Slots(Slot(Fire_Elemental,35)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1225, Slots(Slot(Firebird,1)))),
                            Guard_Reward(Slots(Slot(Fire_Elemental,70)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 2450, Slots(Slot(Firebird,2)))),
                            Guard_Reward(Slots(Slot(Fire_Elemental,105)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 3675, Slots(Slot(Firebird,3)))),
                            Guard_Reward(Slots(Slot(Fire_Elemental,140)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 4900, Slots(Slot(Firebird,4)))))


Ruins = Creature_Bank(1000, "Ruins", False,
            Guard_Reward(Slots(Slot(Skeleton,20),Slot(Wight,3),Slot(Wraith,3),Slot(Skeleton_Warrior,10),Slot(Power_Lich,1)),Reward(Cost(1000, 0, 0, 0, 0, 0, 0), 328, Slots())),
            Guard_Reward(Slots(Slot(Skeleton,30),Slot(Wight,5),Slot(Wraith,5),Slot(Skeleton_Warrior,10),Slot(Power_Lich,1)),Reward(Cost(2000, 0, 0, 0, 0, 0, 0), 460, Slots())),
            Guard_Reward(Slots(Slot(Skeleton,40),Slot(Wight,7),Slot(Wraith,7),Slot(Skeleton_Warrior,20),Slot(Power_Lich,2)),Reward(Cost(3000, 0, 0, 0, 0, 0, 0), 692, Slots())),
            Guard_Reward(Slots(Slot(Skeleton,50),Slot(Wight,9),Slot(Wraith,9),Slot(Skeleton_Warrior,20),Slot(Power_Lich,3)),Reward(Cost(4000, 0, 0, 0, 0, 0, 0), 864, Slots())))


Spit = Creature_Bank(1500, "Spit", False,
                        Guard_Reward(Slots(Slot(Basilisk,16)),Reward(Cost(3000, 0, 0, 0, 0, 0, 0), 560, Slots())),
                        Guard_Reward(Slots(Slot(Basilisk,24)),Reward(Cost(4500, 0, 0, 0, 0, 0, 0), 840, Slots())),
                        Guard_Reward(Slots(Slot(Basilisk,32)),Reward(Cost(6000, 0, 0, 0, 0, 0, 0), 1120, Slots())),
                        Guard_Reward(Slots(Slot(Basilisk,48)),Reward(Cost(9000, 0, 0, 0, 0, 0, 0), 1680, Slots())))


Temple_of_the_Sea = Creature_Bank(10000, "Temple_of_the_Sea", False,
                                Guard_Reward(Slots(Slot(Hydra,8),Slot(Sea_Serpent,6),Slot(Chaos_Hydra,3),Slot(Haspid,2)),Reward(Cost(10000, 0, 0, 0, 0, 0, 0), 3830, Slots())),
                                Guard_Reward(Slots(Slot(Hydra,8),Slot(Sea_Serpent,7),Slot(Chaos_Hydra,4),Slot(Haspid,3)),Reward(Cost(15000, 0, 0, 0, 0, 0, 0), 4560, Slots())),
                                Guard_Reward(Slots(Slot(Hydra,8),Slot(Sea_Serpent,7),Slot(Chaos_Hydra,5),Slot(Haspid,4)),Reward(Cost(20000, 0, 0, 0, 0, 0, 0), 5110, Slots())),
                                Guard_Reward(Slots(Slot(Hydra,10),Slot(Sea_Serpent,9),Slot(Chaos_Hydra,6),Slot(Haspid,5)),Reward(Cost(30000, 0, 0, 0, 0, 0, 0), 6370, Slots())))


Wolf_Raider_Picket = Creature_Bank(9500, "Wolf_Raider_Picket", False,
                                    Guard_Reward(Slots(Slot(Wolf_Raider,50)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 500, Slots(Slot(Cyclops,4)))),
                                    Guard_Reward(Slots(Slot(Wolf_Raider,75)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 750, Slots(Slot(Cyclops,6)))),
                                    Guard_Reward(Slots(Slot(Wolf_Raider,100)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1000, Slots(Slot(Cyclops,8)))),
                                    Guard_Reward(Slots(Slot(Wolf_Raider,150)),Reward(Cost(0, 0, 0, 0, 0, 0, 0), 1500, Slots(Slot(Cyclops,12)))))