"""This python script is responsible for creating objects of Habitat Class that are present in cities."""

from data.building import Habitat, Cost
from data.classes_const import *
# Castle

Guardhouse = Habitat((Cost(500, 0, 10, 0, 0, 0, 0), Cost(1000, 0, 5, 0, 0, 0, 0)),
                     Pikeman, Halberdier, 14, Cost(60, 0, 0, 0, 0, 0, 0), Cost(75, 0, 0, 0, 0, 0, 0), 0, 0, "t1")

Archers_Tower = Habitat((Cost(1000, 5, 5, 0, 0, 0, 0), Cost(1000, 5, 5, 0, 0, 0, 0)),
                        Archer, Marksman, 9, Cost(100, 0, 0, 0, 0, 0, 0), Cost(150, 0, 0, 0, 0, 0, 0), 0, 0, "t2")

Griffin_Tower = Habitat((Cost(1000, 0, 5, 0, 0, 0, 0), Cost(1000, 0, 5, 0, 0, 0, 0)),
                        Griffin, Royal_Griffin, 7, Cost(200, 0, 0, 0, 0, 0, 0), Cost(240, 0, 0, 0, 0, 0, 0), 0, 0, "t3")

Barracks = Habitat((Cost(2000, 0, 5, 0, 0, 0, 0), Cost(2000, 0, 5, 0, 0, 5, 0)),
                   Swordsman, Crusader, 4, Cost(300, 0, 0, 0, 0, 0, 0), Cost(400, 0, 0, 0, 0, 0, 0), 0, 0, "t4")

Monastery = Habitat((Cost(3000, 5, 5, 2, 2, 2, 2), Cost(1000, 2, 2, 2, 2, 2, 2)),
                    Monk, Zealot, 3, Cost(400, 0, 0, 0, 0, 0, 0), Cost(450, 0, 0, 0, 0, 0, 0), 0, 0, "t5")

Training_Grounds = Habitat((Cost(5000, 20, 0, 0, 0, 0, 0), Cost(3000, 10, 0, 0, 0, 0, 0)),
                           Cavalier, Champion, 2, Cost(1000, 0, 0, 0, 0, 0, 0), Cost(1200, 0, 0, 0, 0, 0, 0), 0, 0, "t6")

Portal_of_Glory = Habitat((Cost(20000, 0, 0, 10, 10, 10, 10), Cost(20000, 0, 0, 10, 10, 10, 10)),
                          Angel, Archangel, 1, Cost(3000, 0, 0, 0, 0, 0, 1), Cost(5000, 0, 0, 0, 0, 0, 3), 0, 0, "t7")

# Rampart
Centaur_Stables = Habitat((Cost(500, 5, 0, 0, 0, 0, 0), Cost(1000, 5, 0, 0, 0, 0, 0)),
                          Centaur, Centaur_Captain, 14, Cost(70, 0, 0, 0, 0, 0, 0), Cost(90, 0, 0, 0, 0, 0, 0), 0, 0,
                          "t1")

Dwarf_Cottage = Habitat((Cost(1000, 5, 0, 0, 0, 0, 0), Cost(1000, 5, 0, 0, 0, 0, 0)),
                        Dwarf, Battle_Dwarf, 8, Cost(120, 0, 0, 0, 0, 0, 0), Cost(150, 0, 0, 0, 0, 0, 0), 0, 0,
                        "t2")

Homestead = Habitat((Cost(1500, 10, 0, 0, 0, 0, 0), Cost(1500, 10, 0, 0, 0, 0, 0)),
                    Wood_Elf, Grand_Elf, 7, Cost(200, 0, 0, 0, 0, 0, 0), Cost(225, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t3")

Enchanted_Spring = Habitat((Cost(2000, 0, 0, 0, 0, 10, 0), Cost(2000, 0, 0, 0, 0, 5, 0)),
                           Pegasus, Silver_Pegasus, 5, Cost(250, 0, 0, 0, 0, 0, 0), Cost(275, 0, 0, 0, 0, 0, 0), 0, 0,
                           "t4")

Dendroid_Arches = Habitat((Cost(2500, 0, 0, 0, 0, 0, 0), Cost(1500, 0, 0, 0, 0, 0, 0)),
                          Dendroid_Guard, Dendroid_Soldier, 3, Cost(350, 0, 0, 0, 0, 0, 0), Cost(425, 0, 0, 0, 0, 0, 0),
                          0, 0,
                          "t5")

Unicorn_Glade = Habitat((Cost(4000, 5, 5, 0, 0, 0, 10), Cost(3000, 0, 0, 0, 0, 0, 5)),
                        Unicorn, War_Unicorn, 2, Cost(850, 0, 0, 0, 0, 0, 0), Cost(950, 0, 0, 0, 0, 0, 0), 0, 0,
                        "t6")

Dragon_Cliffs = Habitat((Cost(10000, 0, 30, 0, 0, 20, 0), Cost(20000, 0, 30, 0, 0, 20, 0)),
                        Green_Dragon, Gold_Dragon, 1, Cost(2400, 0, 0, 0, 0, 1, 0), Cost(4000, 0, 0, 0, 0, 2, 0), 0, 0,
                        "t7")

# Tower
Workshop = Habitat((Cost(300, 5, 5, 0, 0, 0, 0), Cost(1000, 0, 0, 0, 0, 0, 0)),
                   Gremlin, Master_Gremlin, 16, Cost(30, 0, 0, 0, 0, 0, 0), Cost(40, 0, 0, 0, 0, 0, 0), 0, 0,
                   "t1")

Parapet = Habitat((Cost(1000, 0, 10, 0, 0, 0, 0), Cost(1500, 0, 5, 0, 0, 0, 0)),
                  Stone_Gargoyle, Obsidian_Gargoyle, 9, Cost(130, 0, 0, 0, 0, 0, 0), Cost(160, 0, 0, 0, 0, 0, 0), 0, 0,
                  "t2")

Golem_Factory = Habitat((Cost(2000, 5, 5, 0, 0, 0, 0), Cost(2000, 5, 5, 5, 0, 0, 0)),
                        Stone_Golem, Iron_Golem, 6, Cost(150, 0, 0, 0, 0, 0, 0), Cost(200, 0, 0, 0, 0, 0, 0), 0, 0,
                        "t3")

Mage_Tower = Habitat((Cost(2500, 5, 5, 5, 5, 5, 5), Cost(2000, 5, 0, 0, 0, 0, 0)),
                     Mage, Arch_Mage, 4, Cost(350, 0, 0, 0, 0, 0, 0), Cost(455, 0, 0, 0, 0, 0, 0), 0, 0,
                     "t4")

Altar_of_Wishes = Habitat((Cost(3000, 5, 5, 0, 0, 6, 6), Cost(2000, 5, 0, 0, 0, 0, 0)),
                          Genie, Master_Genie, 3, Cost(550, 0, 0, 0, 0, 0, 0), Cost(600, 0, 0, 0, 0, 0, 0), 0, 0,
                          "t5")

Golden_Pavilion = Habitat((Cost(4000, 5, 5, 2, 2, 2, 2), Cost(3000, 0, 0, 3, 3, 3, 3)),
                          Naga, Naga_Queen, 2, Cost(1100, 0, 0, 0, 0, 0, 0), Cost(1600, 0, 0, 0, 0, 0, 0), 0, 0,
                          "t6")

Cloud_Temple = Habitat((Cost(5000, 10, 10, 0, 0, 0, 10), Cost(25000, 5, 5, 0, 0, 0, 30)),
                       Giant, Titan, 1, Cost(2000, 0, 0, 0, 0, 0, 1), Cost(5000, 0, 0, 0, 0, 0, 2), 0, 0,
                       "t7")

# Inferno
Imp_Crucible = Habitat((Cost(300, 5, 5, 0, 0, 0, 0), Cost(1000, 0, 0, 0, 0, 0, 0)),
                       Imp, Familiar, 15, Cost(50, 0, 0, 0, 0, 0, 0), Cost(60, 0, 0, 0, 0, 0, 0), 0, 0,
                       "t1")

Hall_of_Sins = Habitat((Cost(1000, 0, 5, 0, 0, 0, 0), Cost(1000, 0, 0, 5, 0, 0, 0)),
                       Gog, Magog, 8, Cost(125, 0, 0, 0, 0, 0, 0), Cost(175, 0, 0, 0, 0, 0, 0), 0, 0,
                       "t2")

Kennels = Habitat((Cost(1500, 10, 0, 0, 0, 0, 0), Cost(1500, 0, 0, 0, 5, 0, 0)),
                  Hell_Hound, Cerberus, 5, Cost(200, 0, 0, 0, 0, 0, 0), Cost(250, 0, 0, 0, 0, 0, 0), 0, 0,
                  "t3")

Demon_Gate = Habitat((Cost(2000, 5, 5, 0, 0, 0, 0), Cost(2000, 5, 5, 0, 0, 0, 0)),
                     Demon, Horned_Demon, 4, Cost(250, 0, 0, 0, 0, 0, 0), Cost(270, 0, 0, 0, 0, 0, 0), 0, 0,
                     "t4")

Hell_Hole = Habitat((Cost(3000, 0, 0, 0, 0, 0, 0), Cost(3000, 0, 0, 5, 5, 0, 0)),
                    Pit_Fiend, Pit_Lord, 3, Cost(500, 0, 0, 0, 0, 0, 0), Cost(700, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t5")

Fire_Lake = Habitat((Cost(4000, 0, 10, 3, 3, 0, 3), Cost(3000, 0, 5, 5, 5, 0, 5)),
                    Efreeti, Efreet_Sultan, 2, Cost(900, 0, 0, 0, 0, 0, 0), Cost(1100, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t6")

Forsaken_Palace = Habitat((Cost(15000, 10, 10, 20, 0, 0, 0), Cost(20000, 5, 5, 20, 0, 0, 0)),
                          Devil, Arch_Devil, 1, Cost(2700, 0, 0, 1, 0, 0, 0), Cost(4500, 0, 0, 2, 0, 0, 0), 0, 0,
                          "t7")

# Necropolis
Cursed_Temple = Habitat((Cost(400, 5, 5, 0, 0, 0, 0), Cost(1000, 5, 5, 0, 0, 0, 0)),
                        Skeleton, Skeleton_Warrior, 12, Cost(60, 0, 0, 0, 0, 0, 0), Cost(70, 0, 0, 0, 0, 0, 0), 0, 0,
                        "t1")

Graveyard = Habitat((Cost(1000, 0, 5, 0, 0, 0, 0), Cost(1000, 5, 5, 0, 0, 0, 0)),
                    Walking_Dead, Zombie, 8, Cost(100, 0, 0, 0, 0, 0, 0), Cost(125, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t2")

Tomb_of_Souls = Habitat((Cost(1500, 5, 5, 0, 0, 0, 0), Cost(1500, 0, 0, 5, 0, 0, 0)),
                        Wight, Wraith, 7, Cost(200, 0, 0, 0, 0, 0, 0), Cost(230, 0, 0, 0, 0, 0, 0), 0, 0,
                        "t3")

Estate = Habitat((Cost(2000, 5, 5, 0, 0, 0, 0), Cost(2000, 10, 0, 0, 0, 10, 10)),
                 Vampire, Vampire_Lord, 4, Cost(360, 0, 0, 0, 0, 0, 0), Cost(500, 0, 0, 0, 0, 0, 0), 0, 0,
                 "t4")

Mausoleum = Habitat((Cost(2000, 0, 10, 0, 10, 0, 0), Cost(2000, 0, 5, 0, 5, 0, 0)),
                    Lich, Power_Lich, 3, Cost(550, 0, 0, 0, 0, 0, 0), Cost(600, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t5")

Hall_of_Darkness = Habitat((Cost(6000, 10, 10, 0, 0, 0, 0), Cost(3000, 5, 5, 2, 2, 2, 2)),
                           Black_Knight, Dread_Knight, 2, Cost(1200, 0, 0, 0, 0, 0, 0), Cost(1500, 0, 0, 0, 0, 0, 0), 0,
                           0,
                           "t6")

Dragon_Vault = Habitat((Cost(10000, 5, 5, 5, 5, 5, 5), Cost(15000, 5, 5, 20, 0, 0, 0)),
                       Bone_Dragon, Ghost_Dragon, 1, Cost(1800, 0, 0, 0, 0, 0, 0), Cost(3000, 0, 0, 1, 0, 0, 0), 0, 0,
                       "t7")

# Dungeon
Warren = Habitat((Cost(400, 10, 0, 0, 0, 0, 0), Cost(1000, 5, 0, 0, 0, 0, 0)),
                 Troglodyte, Infernal_Troglodyte, 14, Cost(50, 0, 0, 0, 0, 0, 0), Cost(65, 0, 0, 0, 0, 0, 0), 0, 0,
                 "t1")

Harpy_Loft = Habitat((Cost(1000, 0, 0, 0, 0, 0, 0), Cost(1000, 0, 0, 0, 2, 2, 0)),
                     Harpy, Harpy_Hag, 8, Cost(130, 0, 0, 0, 0, 0, 0), Cost(170, 0, 0, 0, 0, 0, 0), 0, 0,
                     "t2")

Pillar_of_Eyes = Habitat((Cost(1000, 1, 1, 1, 1, 1, 1), Cost(1000, 1, 1, 1, 1, 1, 1)),
                         Beholder, Evil_Eye, 7, Cost(250, 0, 0, 0, 0, 0, 0), Cost(280, 0, 0, 0, 0, 0, 0), 0, 0,
                         "t3")

Chapel_of_Stilled_Voices = Habitat((Cost(2000, 5, 10, 0, 0, 0, 0), Cost(2000, 5, 0, 0, 0, 0, 0)),
                                   Medusa, Medusa_Queen, 4, Cost(300, 0, 0, 0, 0, 0, 0), Cost(330, 0, 0, 0, 0, 0, 0), 0, 0, "t4")

Labyrinth = Habitat((Cost(4000, 0, 10, 0, 0, 0, 10), Cost(3000, 0, 5, 0, 0, 0, 5)),
                    Minotaur, Minotaur_King, 3, Cost(500, 0, 0, 0, 0, 0, 0), Cost(575, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t5")

Manticore_Lair = Habitat((Cost(5000, 5, 5, 5, 5, 0, 0), Cost(3000, 5, 5, 5, 5, 0, 0)),
                         Manticore, Scorpicore, 2, Cost(850, 0, 0, 0, 0, 0, 0), Cost(1050, 0, 0, 0, 0, 0, 0), 0, 0,
                         "t6")

Dragon_Cave = Habitat((Cost(15000, 15, 15, 0, 20, 0, 0), Cost(15000, 15, 15, 20, 0, 0, 0)),
                      Red_Dragon, Black_Dragon, 1, Cost(2500, 0, 0, 0, 1, 0, 0), Cost(4000, 0, 0, 0, 2, 0, 0), 0, 0,
                      "t7")

# Stronghold
Goblin_Barracks = Habitat((Cost(200, 5, 5, 0, 0, 0, 0), Cost(1000, 5, 5, 0, 0, 0, 0)),
                          Goblin, Hobgoblin, 15, Cost(40, 0, 0, 0, 0, 0, 0), Cost(50, 0, 0, 0, 0, 0, 0), 0, 0,
                          "t1")

Wolf_Pen = Habitat((Cost(1000, 10, 5, 0, 0, 0, 0), Cost(1000, 5, 5, 0, 0, 0, 0)),
                   Wolf_Rider, Wolf_Raider, 9, Cost(100, 0, 0, 0, 0, 0, 0), Cost(140, 0, 0, 0, 0, 0, 0), 0, 0,
                   "t2")

Orc_Tower = Habitat((Cost(1000, 5, 5, 0, 0, 0, 0), Cost(1000, 2, 2, 0, 0, 0, 0)),
                    Orc, Orc_Chieftain, 7, Cost(150, 0, 0, 0, 0, 0, 0), Cost(165, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t3")

Ogre_Fort = Habitat((Cost(2000, 20, 0, 0, 0, 0, 0), Cost(2000, 5, 5, 0, 0, 0, 5)),
                    Ogre, Ogre_Mage, 4, Cost(300, 0, 0, 0, 0, 0, 0), Cost(400, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t4")

Cliff_Nest = Habitat((Cost(2500, 0, 10, 0, 0, 0, 0), Cost(2000, 5, 5, 0, 0, 0, 0)),
                     Roc, Thunderbird, 3, Cost(600, 0, 0, 0, 0, 0, 0), Cost(700, 0, 0, 0, 0, 0, 0), 0, 0,
                     "t5")

Cyclops_Cave = Habitat((Cost(3500, 0, 20, 0, 0, 20, 0), Cost(3000, 5, 5, 0, 0, 0, 0)),
                       Cyclops, Cyclops_King, 2, Cost(750, 0, 0, 0, 0, 0, 0), Cost(1100, 0, 0, 0, 0, 0, 0), 0, 0,
                       "t6")

Behemoth_Lair = Habitat((Cost(10000, 10, 10, 0, 0, 10, 0), Cost(15000, 10, 10, 0, 0, 20, 0)),
                        Behemoth, Ancient_Behemoth, 1, Cost(1500, 0, 0, 0, 0, 0, 0), Cost(3000, 0, 0, 0, 0, 1, 0), 0, 0,
                        "t7")

# Fortress
Gnoll_Hut = Habitat((Cost(400, 10, 0, 0, 0, 0, 0), Cost(1000, 10, 0, 0, 0, 0, 0)),
                    Gnoll, Gnoll_Marauder, 12, Cost(50, 0, 0, 0, 0, 0, 0), Cost(70, 0, 0, 0, 0, 0, 0), 0, 0,
                    "t1")

Lizard_Den = Habitat((Cost(1000, 5, 0, 0, 0, 0, 0), Cost(1000, 5, 0, 0, 0, 0, 0)),
                     Lizardman, Lizard_Warrior, 9, Cost(110, 0, 0, 0, 0, 0, 0), Cost(140, 0, 0, 0, 0, 0, 0), 0, 0,
                     "t2")

Serpent_Fly_Hive = Habitat((Cost(1000, 5, 0, 2, 2, 0, 0), Cost(1000, 0, 0, 2, 2, 0, 0)),
                           Serpent_Fly, Dragon_Fly, 8, Cost(220, 0, 0, 0, 0, 0, 0), Cost(240, 0, 0, 0, 0, 0, 0), 0, 0,
                           "t3")

Basilisk_Pit = Habitat((Cost(2000, 5, 10, 0, 0, 0, 0), Cost(2000, 5, 5, 0, 0, 0, 0)),
                       Basilisk, Greater_Basilisk, 4, Cost(325, 0, 0, 0, 0, 0, 0), Cost(400, 0, 0, 0, 0, 0, 0), 0, 0,
                       "t4")

Gorgon_Lair = Habitat((Cost(2500, 10, 10, 5, 5, 0, 0), Cost(2000, 5, 5, 0, 0, 0, 0)),
                      Gorgon, Mighty_Gorgon, 3, Cost(525, 0, 0, 0, 0, 0, 0), Cost(600, 0, 0, 0, 0, 0, 0), 0, 0,
                      "t5")

Wyvern_Nest = Habitat((Cost(3500, 15, 0, 0, 0, 0, 0), Cost(3000, 10, 0, 10, 0, 0, 0)),
                      Wyvern, Wyvern_Monarch, 2, Cost(800, 0, 0, 0, 0, 0, 0), Cost(1100, 0, 0, 0, 0, 0, 0), 0, 0,
                      "t6")

Hydra_Pond = Habitat((Cost(10000, 10, 10, 0, 10, 0, 0), Cost(15000, 10, 10, 0, 20, 0, 0)),
                     Hydra, Chaos_Hydra, 1, Cost(2200, 0, 0, 0, 0, 0, 0), Cost(3500, 0, 0, 0, 1, 0, 0), 0, 0,
                     "t7")

# Conflux
Magic_Lantern = Habitat((Cost(300, 5, 5, 0, 0, 0, 0), Cost(1000, 0, 0, 0, 0, 0, 0)),
                        Pixie, Sprite, 20, Cost(25, 0, 0, 0, 0, 0, 0), Cost(30, 0, 0, 0, 0, 0, 0), 0, 0,
                        "t1")

Altar_of_Air = Habitat((Cost(1500, 0, 5, 0, 0, 0, 0), Cost(1500, 2, 0, 2, 0, 0, 2)),
                       Air_Elemental, Storm_Elemental, 6, Cost(250, 0, 0, 0, 0, 0, 0), Cost(275, 0, 0, 0, 0, 0, 0), 0,
                       0,
                       "t2")

Altar_of_Water = Habitat((Cost(1500, 0, 5, 0, 0, 0, 0), Cost(2000, 0, 5, 5, 0, 0, 0)),
                         Water_Elemental, Ice_Elemental, 6, Cost(300, 0, 0, 0, 0, 0, 0), Cost(375, 0, 0, 0, 0, 0, 0), 0,
                         0,
                         "t3")

Altar_of_Fire = Habitat((Cost(2000, 5, 5, 0, 0, 0, 0), Cost(2000, 0, 5, 5, 0, 0, 0)),
                        Fire_Elemental, Energy_Elemental, 5, Cost(350, 0, 0, 0, 0, 0, 0), Cost(400, 0, 0, 0, 0, 0, 0),
                        0, 0,
                        "t4")

Altar_of_Earth = Habitat((Cost(2000, 0, 10, 0, 0, 0, 0), Cost(1000, 0, 0, 0, 5, 0, 0)),
                         Earth_Elemental, Magma_Elemental, 4, Cost(400, 0, 0, 0, 0, 0, 0), Cost(500, 0, 0, 0, 0, 0, 0),
                         0, 0,
                         "t5")

Altar_of_Thought = Habitat((Cost(3000, 5, 5, 2, 2, 2, 2), Cost(3000, 0, 0, 3, 3, 3, 3)),
                           Psychic_Elemental, Magic_Elemental, 2, Cost(950, 0, 0, 0, 0, 0, 0),
                           Cost(1200, 0, 0, 0, 0, 0, 0), 0, 0,
                           "t6")

Pyre = Habitat((Cost(10000, 10, 10, 10, 0, 0, 0), Cost(15000, 10, 10, 20, 0, 0, 0)),
               Firebird, Phoenix, 2, Cost(2000, 0, 0, 0, 0, 0, 0), Cost(3000, 0, 0, 1, 0, 0, 0), 0, 0,
               "t7")

# Cove
Nymph_Waterfall = Habitat((Cost(300, 5, 5, 0, 0, 0, 0), Cost(1000, 0, 0, 0, 0, 0, 0)),
                          Nymph, Oceanid, 16, Cost(35, 0, 0, 0, 0, 0, 0), Cost(45, 0, 0, 0, 0, 0, 0), 0, 0,
                          "t1")

Shack = Habitat((Cost(1000, 10, 0, 0, 0, 0, 0), Cost(1000, 5, 0, 0, 0, 0, 0)),
                Crew_Mate, Seaman, 9, Cost(110, 0, 0, 0, 0, 0, 0), Cost(140, 0, 0, 0, 0, 0, 0), 0, 0,
                "t2")

Frigate = Habitat((Cost(1000, 10, 0, 0, 0, 0, 0), Cost(1500, 5, 0, 0, 0, 0, 0)),
                  Pirate, Corsair, 7, Cost(225, 0, 0, 0, 0, 0, 0), Cost(275, 0, 0, 0, 0, 0, 0), 0, 0,
                  "t3")

Nest = Habitat((Cost(2000, 0, 5, 0, 0, 2, 2), Cost(1500, 0, 0, 0, 0, 2, 2)),
               Stormbird, Ayssid, 4, Cost(275, 0, 0, 0, 0, 0, 0), Cost(325, 0, 0, 0, 0, 0, 0), 0, 0,
               "t4")

Tower_of_the_Seas = Habitat((Cost(3000, 5, 5, 0, 0, 5, 0), Cost(2000, 0, 0, 0, 0, 5, 0)),
                            Sea_Witch, Sorceress, 3, Cost(515, 0, 0, 0, 0, 0, 0), Cost(565, 0, 0, 0, 0, 0, 0), 0, 0,
                            "t5")

Nix_Fort = Habitat((Cost(4000, 5, 10, 0, 0, 0, 0), Cost(3000, 5, 5, 0, 5, 0, 0)),
                   Nix, Nix_Warrior, 2, Cost(1000, 0, 0, 0, 0, 0, 0), Cost(1300, 0, 0, 0, 0, 0, 0), 0, 0,
                   "t6")

Maelstrom = Habitat((Cost(15000, 15, 15, 0, 10, 0, 0), Cost(15000, 15, 15, 0, 20, 0, 0)),
                    Sea_Serpent, Haspid, 1, Cost(2200, 0, 0, 0, 1, 0, 0), Cost(4000, 0, 0, 0, 1, 0, 0), 0, 0,
                    "t7")
