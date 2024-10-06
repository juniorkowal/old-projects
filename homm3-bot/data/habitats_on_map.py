"""Script containing Habitat_On_Map class and objects belonging to that class"""

import time

import image_processing.detecting_window
from GUI_handling import AdventureGUI as GUI
from GUI_handling.AdventureGUI import accept_offer
from data.building import *
from data.classes_const import *
from data.hero import Slots, Slot


# Tower golemy do poprawy :)
class Habitat_On_Map:
    def __init__(self, name: str, unit: Creature, guards: Slots, unit_cost: Cost, total_cost: Cost, growth: int,
                 number: int, value, entrance: str, free=False):
        """
        Init function for Habitat_On_Map class representing habitat objects which are present on adventure map

        :param name: Name of the habitat
        :param unit: The unit habitat holds
        :param guards: Guards (Slot Class)
        :param unit_cost: Single unit cost
        :param total_cost: Cost of the whole stack of units
        :param growth: Per week growth in the habitat
        :param number:
        :param value: Adventure Map functions
        :param entrance:
        :param free: boolean whether units are free or we need to pay for them
        :param x: x position of habitat
        :param y: y position of habitat
        """
        self.name = name
        self.unit = unit
        self.guards = guards
        self.total_cost = total_cost
        self.unit_cost = unit_cost
        self.growth = growth
        self.number_of_units = growth
        self.value = value
        self.free = free
        self.entrance = entrance
        self.number = 0
        self.x = 0
        self.y = 0

    def __repr__(self):
        return self.name + f' value: ({str(self.value)})'

    def __str__(self):
        return self.name + f' value: ({str(self.value)})'

    def __eq__(self, other):
        if isinstance(other,Habitat_On_Map):
            return self.name == other.name and self.x == other.x and self.y == other.y
        else:
            return False

    def end_day(self, player):
        """
        Crucial function that doesnt do anything

        :param player: player object
        """
        pass

    def end_week(self, player):
        """
        Sums up number of units in habitat and growth

        :param player: player object
        """
        self.number = self.number_of_units + self.growth

    def action(self, player, hero, okay=0):
        """
        Checking amount of gold an buying maximum amount of units available
        and buying units in habitat only if we can add them to our army

        :param player: player object
        :param hero: hero object
        :param okay: unused parameter
        """
        # we are checking amount of gold an buying maximum amount of units available
        # we are buying units in habitat only if we can add them to our army
        if self not in player.captured_habitats:
            if self.unit.lvl > 4 or self.name == "Golem_Factory":
                accept_offer()
                time.sleep(1)
                image_processing.detecting_window.execute_detecting(hero)
                time.sleep(1)
            player.captured_habitats.append(self)
        slot = -1
        for i, x in enumerate(hero.slots.slots):
            if x.unit.name == self.unit.name:
                slot = i
        if slot == -1:
            for i, x in enumerate(hero.slots.slots):
                if x.unit.name == "":
                    if slot == -1:
                        slot = i
        if slot != -1:
            if self.free:
                GUI.accept_offer()
                amount = self.number_of_units
                self.number_of_units = 0
                time.sleep(0.04)
                GUI.accept_offer()

            else:
                cost = 0
                amount = 0
                while player.gold > cost and amount < self.number_of_units:  # only gold because most units cost only gold
                    amount += 1
                    cost += self.unit_cost.gold
                player.gold -= cost
                GUI.accept_offer()
                time.sleep(0.04)
                GUI.max_unit_buy()
                time.sleep(0.04)
                GUI.accept_offer()
                self.number_of_units -= amount
            hero.slots.slots[slot].amount = amount + hero.slots.slots[slot].amount
            hero.slots.slots[slot].unit = self.unit
        else:
            GUI.leave_screen()


# Castle                                                        unit cost  total cost
Guardhouse_on_Map = Habitat_On_Map("Guardhouse", Pikeman, Slots(), Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0),
                                   14, 0, 100, "right", True)
Archers_Tower_on_Map = Habitat_On_Map("Archers_Tower", Archer, Slots(), Cost(100, 0, 0, 0, 0, 0, 0),
                                      Cost(900, 0, 0, 0, 0, 0, 0), 9, 0, 200, "left")
Griffin_Tower_on_Map = Habitat_On_Map("Griffin_Tower", Griffin, Slots(), Cost(200, 0, 0, 0, 0, 0, 0),
                                      Cost(1400, 0, 0, 0, 0, 0, 0), 7, 0, 300, "right")
Barracks_on_Map = Habitat_On_Map("Barracks", Swordsman, Slots(), Cost(300, 0, 0, 0, 0, 0, 0),
                                 Cost(1200, 0, 0, 0, 0, 0, 0), 4, 0, 400, "right")

Monastery_on_Map = Habitat_On_Map("Monastery", Monk, Slots(Slot(Monk, 9)), Cost(400, 0, 0, 0, 0, 0, 0),
                                  Cost(1200, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Training_Grounds_on_Map = Habitat_On_Map("Training_Grounds", Cavalier, Slots(Slot(Cavalier, 6)),
                                         Cost(1000, 0, 0, 0, 0, 0, 0), Cost(2000, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Portal_of_Glory_on_Map = Habitat_On_Map("Portal_of_Glory", Angel, Slots(Slot(Angel, 3)), Cost(3000, 0, 0, 0, 0, 0, 1),
                                        Cost(3000, 0, 0, 0, 0, 0, 1), 1, 0, 700, "right")

# Rampart
Centaur_Stables_on_Map = Habitat_On_Map("Centaur_Stables", Centaur, Slots(), Cost(0, 0, 0, 0, 0, 0, 0),
                                        Cost(0, 0, 0, 0, 0, 0, 0), 14, 0, 100, "right", True)
Dwarf_Cottage_on_Map = Habitat_On_Map("Dwarf_Cottage", Dwarf, Slots(), Cost(120, 0, 0, 0, 0, 0, 0),
                                      Cost(960, 0, 0, 0, 0, 0, 0), 8, 0, 200, "left")
Homestead_on_Map = Habitat_On_Map("Homestead", Wood_Elf, Slots(), Cost(200, 0, 0, 0, 0, 0, 0),
                                  Cost(1400, 0, 0, 0, 0, 0, 0), 7, 0, 300, "left")
Enchanted_Spring_on_Map = Habitat_On_Map("Enchanted_Spring", Pegasus, Slots(), Cost(250, 0, 0, 0, 0, 0, 0),
                                         Cost(1250, 0, 0, 0, 0, 0, 0), 5, 0, 400, "right")

Dendroid_Arches_on_Map = Habitat_On_Map("Dendroid_Arches", Dendroid_Guard, Slots(Slot(Dendroid_Guard, 9)),
                                        Cost(350, 0, 0, 0, 0, 0, 0), Cost(1050, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Unicorn_Glade_on_Map = Habitat_On_Map("Unicorn_Glade", Unicorn, Slots(Slot(Unicorn, 6)), Cost(850, 0, 0, 0, 0, 0, 0),
                                      Cost(1700, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Dragon_Cliffs_on_Map = Habitat_On_Map("Dragon_Cliffs", Green_Dragon, Slots(Slot(Green_Dragon, 3)),
                                      Cost(2400, 0, 0, 0, 0, 1, 0), Cost(2400, 0, 0, 0, 0, 1, 0), 1, 0, 700, "right")

# Tower
Workshop_on_Map = Habitat_On_Map("Workshop", Gremlin, Slots(), Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0), 16,
                                 0, 100, "right", True)
Parapet_on_Map = Habitat_On_Map("Parapet", Stone_Gargoyle, Slots(), Cost(130, 0, 0, 0, 0, 0, 0),
                                Cost(1170, 0, 0, 0, 0, 0, 0), 9, 0, 200, "right")
Golem_Factory_on_Map = Habitat_On_Map("Golem_Factory", Stone_Golem, Slots(Slot(Diamond_Golem, 5), Slot(Gold_Golem, 5)),
                                      Cost(150, 0, 0, 0, 0, 0, 0), Cost(900, 0, 0, 0, 0, 0, 0), 6, 0, 300,
                                      "right")  # COS JEST NIE TAK
Mage_Tower_on_Map = Habitat_On_Map("Mage_Tower", Mage, Slots(), Cost(350, 0, 0, 0, 0, 0, 0),
                                   Cost(1400, 0, 0, 0, 0, 0, 0), 4, 0, 400, "right")

Altar_of_Wishes_on_Map = Habitat_On_Map("Altar_of_Wishes", Genie, Slots(Slot(Genie, 9)), Cost(550, 0, 0, 0, 0, 0, 0),
                                        Cost(1650, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Golden_Pavilion_on_Map = Habitat_On_Map("Golden_Pavilion", Naga, Slots(Slot(Naga, 6)), Cost(1100, 0, 0, 0, 0, 0, 0),
                                        Cost(2200, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Cloud_Temple_on_Map = Habitat_On_Map("Cloud_Temple", Giant, Slots(Slot(Giant, 3)), Cost(2000, 0, 0, 0, 0, 0, 1),
                                     Cost(2000, 0, 0, 0, 0, 0, 1), 1, 0, 700, "right")

# Inferno
Imp_Crucible_on_Map = Habitat_On_Map("Imp_Crucible", Imp, Slots(), Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0),
                                     15, 0, 100, "right", True)
Hall_of_Sins_on_Map = Habitat_On_Map("Hall_of_Sins", Gog, Slots(), Cost(125, 0, 0, 0, 0, 0, 0),
                                     Cost(1000, 0, 0, 0, 0, 0, 0), 8, 0, 200, "left")
Kennels_on_Map = Habitat_On_Map("Kennels", Hell_Hound, Slots(), Cost(200, 0, 0, 0, 0, 0, 0),
                                Cost(1000, 0, 0, 0, 0, 0, 0), 5, 0, 300, "right")
Demon_Gate_on_Map = Habitat_On_Map("Demon_Gate", Demon, Slots(), Cost(250, 0, 0, 0, 0, 0, 0),
                                   Cost(1000, 0, 0, 0, 0, 0, 0), 4, 0, 400, "right")

Hell_Hole_on_Map = Habitat_On_Map("Hell_Hole", Pit_Fiend, Slots(Slot(Pit_Fiend, 9)), Cost(500, 0, 0, 0, 0, 0, 0),
                                  Cost(1500, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Fire_Lake_on_Map = Habitat_On_Map("Fire_Lake", Efreeti, Slots(Slot(Efreeti, 6)), Cost(900, 0, 0, 0, 0, 0, 0),
                                  Cost(1800, 0, 0, 0, 0, 0, 0), 2, 0, 600, "left")
Forsaken_Palace_on_Map = Habitat_On_Map("Forsaken_Palace", Devil, Slots(Slot(Devil, 3)), Cost(2700, 0, 0, 1, 0, 0, 0),
                                        Cost(2700, 0, 0, 1, 0, 0, 0), 1, 0, 700, "right")

# Necropolis
Cursed_Temple_on_Map = Habitat_On_Map("Cursed_Temple", Skeleton, Slots(), Cost(0, 0, 0, 0, 0, 0, 0),
                                      Cost(0, 0, 0, 0, 0, 0, 0), 12, 0, 100, "right", True)
Graveyard_on_Map = Habitat_On_Map("Graveyard", Walking_Dead, Slots(), Cost(100, 0, 0, 0, 0, 0, 0),
                                  Cost(800, 0, 0, 0, 0, 0, 0), 8, 0, 200, "right")
Tomb_of_Souls_on_Map = Habitat_On_Map("Tomb_of_Souls", Wight, Slots(), Cost(200, 0, 0, 0, 0, 0, 0),
                                      Cost(1400, 0, 0, 0, 0, 0, 0), 7, 0, 300, "left")
Estate_on_Map = Habitat_On_Map("Estate", Vampire, Slots(), Cost(360, 0, 0, 0, 0, 0, 0), Cost(1440, 0, 0, 0, 0, 0, 0), 4,
                               0, 400, "left")

Mausoleum_on_Map = Habitat_On_Map("Mausoleum", Lich, Slots(Slot(Lich, 9)), Cost(550, 0, 0, 0, 0, 0, 0),
                                  Cost(1650, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Hall_of_Darkness_on_Map = Habitat_On_Map("Hall_of_Darkness", Black_Knight, Slots(Slot(Black_Knight, 6)),
                                         Cost(1200, 0, 0, 0, 0, 0, 0), Cost(2400, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Dragon_Vault_on_Map = Habitat_On_Map("Dragon_Vault", Bone_Dragon, Slots(Slot(Bone_Dragon, 3)),
                                     Cost(1800, 0, 0, 0, 0, 0, 0), Cost(1800, 0, 0, 0, 0, 0, 0), 1, 0, 700, "left")

# Dungeon
Warren_on_Map = Habitat_On_Map("Warren", Troglodyte, Slots(), Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0), 14,
                               0, 100, "right", True)
Harpy_Loft_on_Map = Habitat_On_Map("Harpy_Loft", Harpy, Slots(), Cost(130, 0, 0, 0, 0, 0, 0),
                                   Cost(1040, 0, 0, 0, 0, 0, 0), 8, 0, 200, "right")
Pillar_of_Eyes_on_Map = Habitat_On_Map("Pillar_of_Eyes", Beholder, Slots(), Cost(250, 0, 0, 0, 0, 0, 0),
                                       Cost(1750, 0, 0, 0, 0, 0, 0), 7, 0, 300, "left")
Chapel_of_Stilled_Voices_on_Map = Habitat_On_Map("Chapel_of_Stilled_Voices", Medusa, Slots(),
                                                 Cost(300, 0, 0, 0, 0, 0, 0), Cost(1200, 0, 0, 0, 0, 0, 0), 4, 0, 400,
                                                 "right")

Labyrinth_on_Map = Habitat_On_Map("Labyrinth", Minotaur, Slots(Slot(Minotaur, 9)), Cost(500, 0, 0, 0, 0, 0, 0),
                                  Cost(1500, 0, 0, 0, 0, 0, 0), 3, 0, 500, "left")
Manticore_Lair_on_Map = Habitat_On_Map("Manticore_Lair", Manticore, Slots(Slot(Manticore, 6)),
                                       Cost(850, 0, 0, 0, 0, 0, 0), Cost(1700, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Dragon_Cave_on_Map = Habitat_On_Map("Dragon_Cave", Red_Dragon, Slots(Slot(Red_Dragon, 3)), Cost(2500, 0, 0, 0, 1, 0, 0),
                                    Cost(2500, 0, 0, 0, 1, 0, 0), 1, 0, 700, "left")

# Stronghold
Goblin_Barracks_on_Map = Habitat_On_Map("Goblin_Barracks", Goblin, Slots(), Cost(0, 0, 0, 0, 0, 0, 0),
                                        Cost(0, 0, 0, 0, 0, 0, 0), 15, 0, 100, "right", True)
Wolf_Pen_on_Map = Habitat_On_Map("Wolf_Pen", Wolf_Rider, Slots(), Cost(100, 0, 0, 0, 0, 0, 0),
                                 Cost(900, 0, 0, 0, 0, 0, 0), 9, 0, 200, "right")
Orc_Tower_on_Map = Habitat_On_Map("Orc_Tower", Orc, Slots(), Cost(150, 0, 0, 0, 0, 0, 0), Cost(1050, 0, 0, 0, 0, 0, 0),
                                  7, 0, 300, "right")
Ogre_Fort_on_Map = Habitat_On_Map("Ogre_Fort", Ogre, Slots(), Cost(300, 0, 0, 0, 0, 0, 0), Cost(1200, 0, 0, 0, 0, 0, 0),
                                  4, 0, 400, "right")

Cliff_Nest_on_Map = Habitat_On_Map("Cliff_Nest", Roc, Slots(Slot(Roc, 9)), Cost(600, 0, 0, 0, 0, 0, 0),
                                   Cost(1800, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Cyclops_Cave_on_Map = Habitat_On_Map("Cyclops_Cave", Cyclops, Slots(Slot(Cyclops, 6)), Cost(750, 0, 0, 0, 0, 0, 0),
                                     Cost(1500, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Behemoth_Lair_on_Map = Habitat_On_Map("Behemoth_Lair", Behemoth, Slots(Slot(Behemoth, 3)), Cost(1500, 0, 0, 0, 0, 0, 0),
                                      Cost(1500, 0, 0, 0, 0, 0, 0), 1, 0, 700, "right")

# Fortress
Gnoll_Hut_on_Map = Habitat_On_Map("Gnoll_Hut", Gnoll, Slots(), Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0), 12,
                                  0, 100, "right", True)
Lizard_Den_on_Map = Habitat_On_Map("Lizard_Den", Lizardman, Slots(), Cost(110, 0, 0, 0, 0, 0, 0),
                                   Cost(990, 0, 0, 0, 0, 0, 0), 9, 0, 200, "right")
Serpent_Fly_Hive_on_Map = Habitat_On_Map("Serpent_Fly_Hive", Serpent_Fly, Slots(), Cost(220, 0, 0, 0, 0, 0, 0),
                                         Cost(1760, 0, 0, 0, 0, 0, 0), 8, 0, 300, "right")
Basilisk_Pit_on_Map = Habitat_On_Map("Basilisk_Pit", Basilisk, Slots(), Cost(325, 0, 0, 0, 0, 0, 0),
                                     Cost(1300, 0, 0, 0, 0, 0, 0), 4, 0, 400, "right")

Gorgon_Lair_on_Map = Habitat_On_Map("Gorgon_Lair", Gorgon, Slots(Slot(Gorgon, 9)), Cost(525, 0, 0, 0, 0, 0, 0),
                                    Cost(1575, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Wyvern_Nest_on_Map = Habitat_On_Map("Wyvern_Nest", Wyvern, Slots(Slot(Wyvern, 6)), Cost(800, 0, 0, 0, 0, 0, 0),
                                    Cost(1600, 0, 0, 0, 0, 0, 0), 2, 0, 600, "left")
Hydra_Pond_on_Map = Habitat_On_Map("Hydra_Pond", Hydra, Slots(Slot(Hydra, 3)), Cost(2200, 0, 0, 0, 0, 0, 0),
                                   Cost(2200, 0, 0, 0, 0, 0, 0), 1, 0, 700, "left")

# Conflux
Magic_Lantern_on_Map = Habitat_On_Map("Magic_Lantern", Pixie, Slots(), Cost(0, 0, 0, 0, 0, 0, 0),
                                      Cost(0, 0, 0, 0, 0, 0, 0), 20, 0, 100, "right", True)
Altar_of_Air_on_Map = Habitat_On_Map("Altar_of_Air", Air_Elemental, Slots(), Cost(250, 0, 0, 0, 0, 0, 0),
                                     Cost(1500, 0, 0, 0, 0, 0, 0), 6, 0, 200, "right")
Air_Elemental_Conflux_on_Map = Habitat_On_Map("Altar_of_Air", Air_Elemental, Slots(), Cost(250, 0, 0, 0, 0, 0, 0),
                                              Cost(1500, 0, 0, 0, 0, 0, 0), 6, 0, 200, "right")
Altar_of_Water_on_Map = Habitat_On_Map("Altar_of_Water", Water_Elemental, Slots(), Cost(300, 0, 0, 0, 0, 0, 0),
                                       Cost(1800, 0, 0, 0, 0, 0, 0), 6, 0, 300, "right")
Water_Elemental_Conflux_on_Map = Habitat_On_Map("Altar_of_Water", Water_Elemental, Slots(), Cost(300, 0, 0, 0, 0, 0, 0),
                                                Cost(1800, 0, 0, 0, 0, 0, 0), 6, 0, 300, "right")
Altar_of_Fire_on_Map = Habitat_On_Map("Altar_of_Fire", Fire_Elemental, Slots(), Cost(350, 0, 0, 0, 0, 0, 0),
                                      Cost(1750, 0, 0, 0, 0, 0, 0), 5, 0, 400, "right")
Fire_Elemental_Conflux_on_Map = Habitat_On_Map("Altar_of_Fire", Fire_Elemental, Slots(), Cost(350, 0, 0, 0, 0, 0, 0),
                                               Cost(1750, 0, 0, 0, 0, 0, 0), 5, 0, 400, "right")

Altar_of_Earth_on_Map = Habitat_On_Map("Altar_of_Earth", Earth_Elemental, Slots(Slot(Earth_Elemental, 12)),
                                       Cost(400, 0, 0, 0, 0, 0, 0), Cost(1600, 0, 0, 0, 0, 0, 0), 4, 0, 500, "right")
Earth_Elemental_Conflux_on_Map = Habitat_On_Map("Altar_of_Earth", Earth_Elemental, Slots(Slot(Earth_Elemental, 12)),
                                                Cost(400, 0, 0, 0, 0, 0, 0), Cost(1600, 0, 0, 0, 0, 0, 0), 4, 0, 500,
                                                "right")
# Elemental_Conflux problem
Altar_of_Thought_on_Map = Habitat_On_Map("Altar_of_Thought", Psychic_Elemental, Slots(Slot(Psychic_Elemental, 6)),
                                         Cost(950, 0, 0, 0, 0, 0, 0), Cost(1900, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Pyre_on_Map = Habitat_On_Map("Pyre", Firebird, Slots(Slot(Firebird, 3)), Cost(2000, 0, 0, 0, 0, 0, 0),
                             Cost(2000, 0, 0, 0, 0, 0, 0), 1, 0, 700, "right")

# Cove
Nymph_Waterfall_on_Map = Habitat_On_Map("Nymph_Waterfall", Nymph, Slots(), Cost(0, 0, 0, 0, 0, 0, 0),
                                        Cost(0, 0, 0, 0, 0, 0, 0), 16, 0, 100, "right", True)
Shack_on_Map = Habitat_On_Map("Shack", Crew_Mate, Slots(), Cost(110, 0, 0, 0, 0, 0, 0), Cost(990, 0, 0, 0, 0, 0, 0), 9,
                              0, 200, "left")
Frigate_on_Map = Habitat_On_Map("Frigate", Pirate, Slots(), Cost(225, 0, 0, 0, 0, 0, 0), Cost(1575, 0, 0, 0, 0, 0, 0),
                                7, 0, 300, "left")
Nest_on_Map = Habitat_On_Map("Nest", Stormbird, Slots(), Cost(275, 0, 0, 0, 0, 0, 0), Cost(1100, 0, 0, 0, 0, 0, 0), 4,
                             0, 400, "right")

Tower_of_the_Seas_on_Map = Habitat_On_Map("Tower_of_the_Seas", Sea_Witch, Slots(Slot(Sea_Witch, 9)),
                                          Cost(515, 0, 0, 0, 0, 0, 0), Cost(1545, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Nix_Fort_on_Map = Habitat_On_Map("Nix_Fort", Nix, Slots(Slot(Nix, 6)), Cost(1000, 0, 0, 0, 0, 0, 0),
                                 Cost(2000, 0, 0, 0, 0, 0, 0), 2, 0, 600, "left")
Maelstrom_on_Map = Habitat_On_Map("Maelstrom", Sea_Serpent, Slots(Slot(Sea_Serpent, 3)), Cost(2200, 0, 0, 0, 1, 0, 0),
                                  Cost(2200, 0, 0, 0, 1, 0, 0), 1, 0, 700, "left")

# Neutral

Hovel = Habitat_On_Map("Hovel", Peasant, Slots(), Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0), 25, 0, 25,
                       "right", True)
Thatched_Hut = Habitat_On_Map("Thatched_Hut", Halfling, Slots(), Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0),
                              15, 0, 50, "right", True)
Rogue_Cavern = Habitat_On_Map("Rogue_Cavern", Rogue, Slots(), Cost(100, 0, 0, 0, 0, 0, 0), Cost(800, 0, 0, 0, 0, 0, 0),
                              8, 0, 200, "right")
Alehouse = Habitat_On_Map("Alehouse", Leprechaun, Slots(), Cost(100, 0, 0, 0, 0, 0, 0), Cost(900, 0, 0, 0, 0, 0, 0), 9,
                          0, 150, "left")
Boar_Glen = Habitat_On_Map("Boar_Glen", Boar, Slots(), Cost(150, 0, 0, 0, 0, 0, 0), Cost(1200, 0, 0, 0, 0, 0, 0), 8, 0,
                           200, "right")
Nomad_Tent = Habitat_On_Map("Nomad_Tent", Nomad, Slots(), Cost(200, 0, 0, 0, 0, 0, 0), Cost(1400, 0, 0, 0, 0, 0, 0), 7,
                            0, 200, "right")
Tomb_of_Curses = Habitat_On_Map("Tomb_of_Curses", Mummy, Slots(), Cost(300, 0, 0, 0, 0, 0, 0),
                                Cost(2100, 0, 0, 0, 0, 0, 0), 7, 0, 200, "left")
Wineyard = Habitat_On_Map("Wineyard", Satyr, Slots(), Cost(300, 0, 0, 0, 0, 0, 0), Cost(1200, 0, 0, 0, 0, 0, 0), 4, 0,
                          300, "left")
Treetop_Tower = Habitat_On_Map("Treetop_Tower", Sharpshooter, Slots(), Cost(400, 0, 0, 0, 0, 0, 0),
                               Cost(1600, 0, 0, 0, 0, 0, 0), 4, 0, 500, "right")
Troll_Bridge = Habitat_On_Map("Troll_Bridge", Troll, Slots(Slot(Troll, 9)), Cost(500, 0, 0, 0, 0, 0, 0),
                              Cost(1500, 0, 0, 0, 0, 0, 0), 3, 0, 400, "right")
Ziggurat = Habitat_On_Map("Ziggurat", Fangarm, Slots(Slot(Fangarm, 9)), Cost(600, 0, 0, 0, 0, 0, 0),
                          Cost(1800, 0, 0, 0, 0, 0, 0), 3, 0, 500, "right")
Enchanters_Hollow = Habitat_On_Map("Enchanters_Hollow", Enchanter, Slots(Slot(Enchanter, 6)),
                                   Cost(750, 0, 0, 0, 0, 0, 0), Cost(1500, 0, 0, 0, 0, 0, 0), 2, 0, 600, "right")
Magic_Forest = Habitat_On_Map("Magic_Forest", Faerie_Dragon, Slots(Slot(Faerie_Dragon, 3)),
                              Cost(10000, 0, 0, 0, 0, 0, 8), Cost(10000, 0, 0, 0, 0, 0, 8), 1, 0, 1000, "right")
Sulfurous_Lair = Habitat_On_Map("Sulfurous_Lair", Rust_Dragon, Slots(Slot(Rust_Dragon, 3)),
                                Cost(15000, 0, 0, 0, 14, 0, 0), Cost(15000, 0, 0, 0, 14, 0, 0), 1, 0, 1000, "right")
Crystal_Cave = Habitat_On_Map("Crystal_Cave", Crystal_Dragon, Slots(Slot(Crystal_Dragon, 3)),
                              Cost(20000, 0, 0, 0, 0, 10, 0), Cost(20000, 0, 0, 0, 0, 10, 0), 1, 0, 1000, "right")
Frozen_Cliffs = Habitat_On_Map("Frozen_Cliffs", Azure_Dragon, Slots(Slot(Azure_Dragon, 3)),
                               Cost(30000, 0, 0, 20, 0, 0, 0), Cost(30000, 0, 0, 20, 0, 0, 0), 1, 0, 1000, "right")
