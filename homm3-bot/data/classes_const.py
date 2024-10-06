"""Script containing all of the creatures object"""
from data.creature import Creature

# Castle
Pikeman = Creature("Pikeman", 1, 4, 5, (1, 3), 10, 4, 80, 1, 0, False, False, "Castle", ("Immune to jousting",), ["Grass"])
Halberdier = Creature("Halberdier", 1, 6, 5, (2, 3), 10, 5, 115, 1, 0, False, True, "Castle", ("Immune to jousting",), ["Grass"])

Archer = Creature("Archer", 2, 6, 3, (2, 3), 10, 4, 126, 1, 12, False, False, "Castle", ("None",), ["Grass"])
Marksman = Creature("Marksman", 2, 6, 3, (2, 3), 10, 6, 184, 1, 24, False, True, "Castle", ("Double attack",), ["Grass"])

Griffin = Creature("Griffin", 3, 8, 8, (3, 6), 25, 6, 351, 2, 0, True, False, "Castle", ("2 retaliations",), ["Grass"])
Royal_Griffin = Creature("Royal_Griffin", 3, 9, 9, (3, 6), 25, 9, 448, 2, 0, True, True, "Castle", ("Unlimited retaliations",), ["Grass"])

Swordsman = Creature("Swordsman", 4, 10, 12, (6, 9), 35, 5, 445, 1, 0, False, False, "Castle", ("None",), ["Grass"])
Crusader = Creature("Crusader", 4, 12, 12, (7, 10), 35, 6, 588, 1, 0, False, True, "Castle", ("Double attack",), ["Grass"])

Monk = Creature("Monk", 5, 12, 7, (10, 12), 30, 5, 582, 1, 12, False, False, "Castle", ("None",), ["Grass"])
Zealot = Creature("Zealot", 5, 12, 10, (10, 12), 30, 7, 750, 1, 24, False, True, "Castle", ("No melee penalty",), ["Grass"])

Cavalier = Creature("Cavalier", 6, 15, 15, (15, 25), 100, 7, 1946, 2, 0, False, False, "Castle", ("Jousting",), ["Grass"])
Champion = Creature("Champion", 6, 16, 16, (20, 25), 100, 9, 2100, 2, 0, False, True, "Castle", ("Jousting",), ["Grass"])

Angel = Creature("Angel", 7, 20, 20, (50, 50), 200, 12, 5019, 1, 0, True, False, "Castle", ("Hates devils", "Morale+1"), ["Grass"])
Archangel = Creature("Archangel", 7, 30, 30, (50, 50), 250, 18, 8776, 2, 0, True, True, "Castle",
                     ("Hates devils", "Resurrection", "Morale+1"), ["Grass"])

# Rampart
Centaur = Creature("Centaur", 1, 5, 3, (2, 3), 8, 6, 100, 2, 0, False, False, "Rampart", ("None",), ["Grass"])
Centaur_Captain = Creature("Centaur_Captain", 1, 6, 3, (2, 3), 10, 8, 138, 2, 0, False, True, "Rampart", ("None",), ["Grass"])

Dwarf = Creature("Dwarf", 2, 6, 7, (2, 4), 20, 3, 138, 1, 0, False, False, "Rampart", ("Resistance +20%",), ["Grass"])
Battle_Dwarf = Creature("Battle_Dwarf", 2, 7, 7, (2, 4), 20, 5, 209, 1, 0, False, True, "Rampart", ("Resistance +40%",), ["Grass"])

Wood_Elf = Creature("Wood_Elf", 3, 9, 5, (3, 5), 15, 6, 234, 1, 24, False, False, "Rampart", ("None",), ["Grass"])
Grand_Elf = Creature("Grand_Elf", 3, 9, 5, (3, 5), 15, 7, 331, 1, 24, False, True, "Rampart", ("Double attack",), ["Grass"])

Pegasus = Creature("Pegasus", 4, 9, 8, (5, 9), 30, 8, 518, 2, 0, True, False, "Rampart", ("Magic damper",), ["Grass"])
Silver_Pegasus = Creature("Silver_Pegasus", 4, 9, 10, (5, 9), 30, 12, 532, 2, 0, True, True, "Rampart", ("Magic damper",), ["Grass"])

Dendroid_Guard = Creature("Dendroid_Guard", 5, 9, 12, (10, 14), 55, 3, 517, 1, 0, False,  False, "Rampart", ("Binding",), ["Grass"])
Dendroid_Soldier = Creature("Dendroid_Soldier", 5, 9, 12, (10, 14), 65, 4, 803, 1, 0, False, True, "Rampart", ("Binding",), ["Grass"])

Unicorn = Creature("Unicorn", 6, 15, 14, (18, 22), 90, 7, 1806, 2, 0, False, False, "Rampart", ("Blind", "Aura of Resistance + 20%"), ["Grass"])
War_Unicorn = Creature("War_Unicorn", 6, 15, 14, (18, 22), 110, 9, 2030, 2, 0, False, True, "Rampart", ("Blind", "Aura of Resistance + 20%"), ["Grass"])

Green_Dragon = Creature("Green_Dragon", 7, 18, 18, (40, 50), 180, 10, 4872, 2, 0, True, False, "Rampart",
                        ("Dragon", "Breath attack", "1-3 lvl spells immunity"), ["Grass"])
Gold_Dragon = Creature("Gold_Dragon", 7, 27, 27, (40, 50), 250, 16, 8613, 2, 0, True, True, "Rampart",
                       ("Dragon", "Breath attack", "1-4 lvl spells immunity"), ["Grass"])

# Tower
Gremlin = Creature("Gremlin", 1, 3, 3, (1, 2), 4, 4, 44, 1, 0, False, False, "Tower", ("None",), ["Snow"])
Master_Gremlin = Creature("Master_Gremlin", 1, 4, 4, (1, 2), 4, 5, 66, 1, 8, False, True, "Tower", ("None",), ["Snow"])

Stone_Gargoyle = Creature("Stone_Gargoyle", 2, 6, 6, (2, 3), 16, 6, 165, 1, 0, True, False, "Tower", ("Unliving",), ["Snow"])
Obsidian_Gargoyle = Creature("Obsidian_Gargoyle", 2, 7, 7, (2, 3), 16, 9, 201, 1, 0, True, True, "Tower", ("Unliving",), ["Snow"])

Stone_Golem = Creature("Stone_Golem", 3, 7, 10, (4, 5), 30, 3, 250, 1, 0, False, False, "Tower", ("Unliving", "Spell Damage Resistance +50%"), ["Snow"])
Iron_Golem = Creature("Iron_Golem", 3, 9, 10, (4, 5), 35, 5, 412, 1, 0, False, True, "Tower", ("Unliving", "Spell Damage Resistance +75%"), ["Snow"])

Mage = Creature("Mage", 4, 11, 8, (7, 9), 25, 5, 570, 1, 24, False, False, "Tower",
                ("No melee penalty", "No obstacle penalty", "Spells cost -2sp"), ["Snow"])
Arch_Mage = Creature("Arch_Mage", 4, 12, 9, (7, 9), 30, 7, 680, 1, 24, False, True, "Tower",
                     ("No melee penalty", "No obstacle penalty", "Spells cost -2sp"), ["Snow"])

Genie = Creature("Genie", 5, 12, 12, (13, 16), 40, 7, 884, 1, 0, True, False, "Tower", ("Hates Efreet and Efreet Sultans",), ["Snow"])
Master_Genie = Creature("Master_Genie", 5, 12, 12, (13, 16), 40, 11, 942, 1, 0, True, True, "Tower",
                        ("Spellcaster", "Hates Efreet and Efreet Sultans"), ["Snow"])

Naga = Creature("Naga", 6, 16, 13, (20, 20), 110, 5, 2016, 2, 0, False, False, "Tower", ("No enemy retaliation",), ["Snow"])
Naga_Queen = Creature("Naga_Queen", 6, 16, 13, (30, 30), 110, 7, 2840, 2, 0, False, True, "Tower", ("No enemy retaliation",), ["Snow"])

Giant = Creature("Giant", 7, 19, 16, (40, 60), 150, 7, 3718, 1, 0, False, False, "Tower", ("Immunity to Mind spells",), ["Snow"])
Titan = Creature("Titan", 7, 24, 24, (40, 60), 300, 11, 7500, 1, 24, False, True, "Tower",
                 ("No melee penalty", "Immunity to Mind spells", "Hates Black Dragons"), ["Snow"])

# Inferno
Imp = Creature("Imp", 1, 2, 3, (1, 2), 4, 5, 50, 1, 0, False, False, "Inferno", ("None",), ["Lava"])
Familiar = Creature("Familiar", 1, 4, 4, (1, 2), 4, 7, 60, 1, 0, False, True, "Inferno", ("Magic channel",), ["Lava"])

Gog = Creature("Gog", 2, 6, 4, (2, 4), 13, 4, 159, 1, 12, False, False, "Inferno", ("None",), ["Lava"])
Magog = Creature("Magog", 2, 7, 4, (2, 4), 13, 6, 240, 1, 24, False, True, "Inferno", ("Fireball attack",), ["Lava"])

Hell_Hound = Creature("Hell_Hound", 3, 10, 6, (2, 7), 25, 7, 357, 2, 0, False, False, "Inferno", ("None",), ["Lava"])
Cerberus = Creature("Cerberus", 3, 10, 8, (2, 7), 25, 8, 392, 2, 0, False, True, "Inferno", ("No enemy retaliation", "3-headed attack"), ["Lava"])

Demon = Creature("Demon", 4, 10, 10, (7, 9), 35, 5, 445, 1, 0, False, False, "Inferno", ("None",), ["Lava"])
Horned_Demon = Creature("Horned_Demon", 4, 10, 10, (7, 9), 40, 6, 480, 1, 0, False, True, "Inferno", ("None",), ["Lava"])

Pit_Fiend = Creature("Pit_Fiend", 5, 13, 13, (13, 17), 45, 6, 765, 1, 0, False, False, "Inferno", ("None",), ["Lava"])
Pit_Lord = Creature("Pit_Lord", 5, 13, 13, (13, 17), 45, 7, 1224, 1, 0, False, True, "Inferno", ("Summon demons",), ["Lava"])

Efreeti = Creature("Efreeti", 6, 16, 12, (16, 24), 90, 9, 1670, 1, 0, True, False, "Inferno", ("Fire immunity", "Hates Genies"), ["Lava"])
Efreet_Sultan = Creature("Efreet_Sultan", 6, 16, 14, (16, 24), 90, 13, 2343, 1, 0, True, True, "Inferno",
                         ("Fire shield", "Fire immunity", "Hates Genies"), ["Lava"])

Devil = Creature("Devil", 7, 19, 21, (30, 40), 160, 11, 5101, 1, 0, True, False, "Inferno",
                 ("No enemy retaliation", "Luck -1", "Hates Angels"), ["Lava"])
Arch_Devil = Creature("Arch_Devil", 7, 26, 28, (30, 40), 200, 17, 7115, 1, 0, True, True, "Inferno",
                      ("No enemy retaliation", "Luck -2", "Hates Angels"), ["Lava"])

# Necropolis
Skeleton = Creature("Skeleton", 1, 5, 4, (1, 3), 6, 4, 60, 1, 0, False, False, "Necropolis", ("Undead",), ["Dirt"])
Skeleton_Warrior = Creature("Skeleton_Warrior", 1, 6, 6, (1, 3), 6, 5, 85, 1, 0, False, True, "Necropolis", ("Undead",), ["Dirt"])

Walking_Dead = Creature("Walking_Dead", 2, 5, 5, (2, 3), 15, 3, 98, 1, 0, False, False, "Necropolis", ("Undead",), ["Dirt"])
Zombie = Creature("Zombie", 2, 5, 5, (2, 3), 20, 4, 128, 1, 0, False, True, "Necropolis", ("Undead", "Disease"), ["Dirt"])

Wight = Creature("Wight", 3, 7, 7, (3, 5), 18, 5, 252, 1, 0, True, False, "Necropolis", ("Undead", "Regeneration"), ["Dirt"])
Wraith = Creature("Wraith", 3, 7, 7, (3, 5), 18, 7, 315, 1, 0, True, True, "Necropolis", ("Undead", "Regeneration", "Mana drain"), ["Dirt"])

Vampire = Creature("Vampire", 4, 10, 9, (5, 8), 30, 6, 555, 1, 0, True, False, "Necropolis", ("Undead", "No enemy retaliation"), ["Dirt"])
Vampire_Lord = Creature("Vampire_Lord", 4, 10, 10, (5, 8), 40, 9, 783, 1, 0, True, True, "Necropolis",
                        ("Undead", "No enemy retaliation", "Life drain"), ["Dirt"])

Lich = Creature("Lich", 5, 13, 10, (11, 13), 30, 6, 848, 1, 12, False, False, "Necropolis", ("Undead", "Death cloud"), ["Dirt"])
Power_Lich = Creature("Power_Lich", 5, 13, 10, (11, 15), 40, 7, 1079, 1, 24, False, True, "Necropolis", ("Undead", "Death cloud"), ["Dirt"])

Black_Knight = Creature("Black_Knight", 6, 16, 16, (15, 30), 120, 7, 2087, 2, 0, False, False, "Necropolis", ("Undead", "Curse"), ["Dirt"])
Dread_Knight = Creature("Dread_Knight", 6, 18, 18, (15, 30), 120, 9, 2382, 2, 0, False, True, "Necropolis", ("Undead", "Curse", "Death blow"), ["Dirt"])

Bone_Dragon = Creature("Bone_Dragon", 7, 17, 15, (25, 50), 150, 9, 3388, 2, 0, True, False, "Necropolis", ("Dragon", "Undead", "Morale -1"), ["Dirt"])
Ghost_Dragon = Creature("Ghost_Dragon", 7, 19, 17, (25, 50), 200, 14, 4696, 2, 0, True, True, "Necropolis",
                        ("Dragon", "Undead", "Morale -1", "Aging"), ["Dirt"])

# Dungeon
Troglodyte = Creature("Troglodyte", 1, 4, 3, (1, 3), 5, 4, 59, 1, 0, False, False, "Dungeon", ("Immune to Blinding",), ["Subterranean"])
Infernal_Troglodyte = Creature("Infernal_Troglodyte", 1, 5, 4, (1, 3), 6, 5, 84, 1, 0, False, True, "Dungeon", ("Immune to Blinding",), ["Subterranean"])

Harpy = Creature("Harpy", 2, 6, 5, (1, 4), 14, 6, 154, 1, 0, True, False, "Dungeon", ("Strike and return",), ["Subterranean"])
Harpy_Hag = Creature("Harpy_Hag", 2, 6, 6, (1, 4), 14, 9, 238, 1, 0, True, True, "Dungeon", ("Strike and return", "No enemy retaliation"), ["Subterranean"])

Beholder = Creature("Beholder", 3, 9, 7, (3, 5), 22, 5, 336, 1, 12, False, False, "Dungeon", ("No melee penalty",), ["Subterranean"])
Evil_Eye = Creature("Evil_Eye", 3, 10, 8, (3, 5), 22, 7, 367, 1, 24, False, True, "Dungeon", ("No melee penalty",), ["Subterranean"])

Medusa = Creature("Medusa", 4, 9, 9, (6, 8), 25, 5, 517, 2, 4, False, False, "Dungeon", ("No melee penalty", "Petrify"), ["Subterranean"])
Medusa_Queen = Creature("Medusa_Queen", 4, 10, 10, (6, 8), 30, 6, 577, 2, 8, False, True, "Dungeon",
                        ("No melee penalty", "Petrify"), ["Subterranean"])

Minotaur = Creature("Minotaur", 5, 14, 12, (12, 20), 50, 6, 835, 1, 0, False, False, "Dungeon", ("Positive Morale",), ["Subterranean"])
Minotaur_King = Creature("Minotaur_King", 5, 15, 15, (12, 20), 50, 8, 1068, 1, 0, False, True, "Dungeon", ("Positive Morale",), ["Subterranean"])

Manticore = Creature("Manticore", 6, 15, 13, (14, 20), 80, 7, 1547, 2, 0, True, False, "Dungeon", ("None",), ["Subterranean"])
Scorpicore = Creature("Scorpicore", 6, 16, 14, (14, 20), 80, 11, 1589, 2, 0, True, True, "Dungeon", ("Paralyze",), ["Subterranean"])

Red_Dragon = Creature("Red_Dragon", 7, 19, 19, (40, 50), 180, 11, 4702, 2, 0, True, False, "Dungeon",
                      ("Dragon", "Breath attack", "1-3 lvl spells immunity"), ["Subterranean"])
Black_Dragon = Creature("Black_Dragon", 7, 25, 25, (40, 50), 300, 15, 8721, 2, 0, True, True, "Dungeon",
                        ("Dragon", "Breath attack", "Magic immunity", "Hates Titans"), ["Subterranean"])

# Stronghold
Goblin = Creature("Goblin", 1, 4, 2, (1, 2), 5, 5, 60, 1, 0, False, False, "Stronghold", ("None",), ["Rough"])
Hobgoblin = Creature("Hobgoblin", 1, 5, 3, (1, 2), 5, 7, 78, 1, 0, False, True, "Stronghold", ("None",), ["Rough"])

Wolf_Rider = Creature("Wolf_Rider", 2, 7, 5, (2, 4), 10, 6, 130, 2, 0, False, False, "Stronghold", ("None",), ["Rough"])
Wolf_Raider = Creature("Wolf_Raider", 2, 8, 5, (3, 4), 10, 8, 203, 2, 0, False, True, "Stronghold", ("Double attack",), ["Rough"])

Orc = Creature("Orc", 3, 8, 4, (2, 5), 15, 4, 192, 1, 12, False, False, "Stronghold", ("None",), ["Rough"])
Orc_Chieftain = Creature("Orc_Chieftain", 3, 8, 4, (2, 5), 20, 5, 240, 1, 24, False, True, "Stronghold", ("None",), ["Rough"])

Ogre = Creature("Ogre", 4, 13, 7, (6, 12), 40, 4, 416, 1, 0, False, False, "Stronghold", ("None",), ["Rough"])
Ogre_Mage = Creature("Ogre_Mage", 4, 13, 7, (6, 12), 60, 5, 672, 1, 0, False, True, "Stronghold", ("Cast Bloodlust x3",), ["Rough"])

Roc = Creature("Roc", 5, 13, 11, (11, 15), 60, 7, 1027, 2, 0, True, False, "Stronghold", ("None",), ["Rough"])
Thunderbird = Creature("Thunderbird", 5, 13, 11, (11, 15), 60, 11, 1106, 2, 0, True, True, "Stronghold", ("Lightning strike",), ["Rough"])

Cyclops = Creature("Cyclops", 6, 15, 12, (16, 20), 70, 6, 1266, 1, 16, False, False, "Stronghold", ("Can attack siege walls",), ["Rough"])
Cyclops_King = Creature("Cyclops_King", 6, 17, 13, (16, 20), 70, 8, 1443, 1, 24, False, True, "Stronghold", ("Can attack siege walls",), ["Rough"])

Behemoth = Creature("Behemoth", 7, 17, 17, (30, 50), 160, 6, 3162, 2, 0, False, False, "Stronghold", ("Defense - 40% to enemy target",), ["Rough"])
Ancient_Behemoth = Creature("Ancient_Behemoth", 7, 19, 19, (30, 50), 300, 9, 6168, 2, 0, False, True, "Stronghold", ("Defense - 80% to enemy target",), ["Rough"])

# Fortress
Gnoll = Creature("Gnoll", 1, 3, 5, (2, 3), 6, 4, 56, 1, 0, False, False, "Fortress", ("None",), ["Swamp"])
Gnoll_Marauder = Creature("Gnoll_Marauder", 1, 4, 6, (2, 3), 6, 5, 90, 1, 0, False, True, "Fortress", ("None",), ["Swamp"])

Lizardman = Creature("Lizardman", 2, 5, 6, (2, 3), 14, 4, 126, 1, 12, False, False, "Fortress", ("None",), ["Swamp"])
Lizard_Warrior = Creature("Lizard_Warrior", 2, 6, 8, (2, 5), 15, 5, 156, 1, 24, False, True, "Fortress", ("None",), ["Swamp"])

Serpent_Fly = Creature("Serpent_Fly", 3, 7, 9, (2, 5), 20, 9, 268, 1, 0, True, False, "Fortress", ("Dispel",), ["Swamp"])
Dragon_Fly = Creature("Dragon_Fly", 3, 8, 10, (2, 5), 20, 13, 312, 1, 0, True, True, "Fortress", ("Dispel", "Weakness"), ["Swamp"])

Basilisk = Creature("Basilisk", 4, 11, 11, (6, 10), 35, 5, 552, 2, 0, False, False, "Fortress", ("Petrify",), ["Swamp"])
Greater_Basilisk = Creature("Greater_Basilisk", 4, 12, 12, (6, 10), 40, 7, 714, 2, 0, False, True, "Fortress", ("Petrify",), ["Swamp"])

Gorgon = Creature("Gorgon", 5, 10, 14, (12, 16), 70, 5, 890, 2, 0, False, False, "Fortress", ("None",), ["Swamp"])
Mighty_Gorgon = Creature("Mighty_Gorgon", 5, 11, 16, (12, 16), 70, 6, 1028, 2, 0, False, True, "Fortress", ("Death stare 10% chance/unit",), ["Swamp"])

Wyvern = Creature("Wyvern", 6, 14, 14, (14, 18), 70, 7, 1350, 2, 0, True, False, "Fortress", ("None",), ["Swamp"])
Wyvern_Monarch = Creature("Wyvern_Monarch", 6, 14, 14, (18, 22), 70, 11, 1518, 2, 0, True, True, "Fortress", ("Poison",), ["Swamp"])

Hydra = Creature("Hydra", 7, 16, 18, (25, 45), 175, 5, 4120, 2, 0, False, False, "Fortress", ("No enemy retaliation", "Attack all adjecent enemies"), ["Swamp"])
Chaos_Hydra = Creature("Chaos_Hydra", 7, 18, 20, (25, 45), 250, 7, 5931, 2, 0, False, True, "Fortress",
                       ("No enemy retaliation", "Attack all adjecent enemies"), ["Swamp"])

# Conflux
Pixie = Creature("Pixie", 1, 2, 2, (1, 2), 3, 7, 55, 1, 0, True, False, "Conflux", ("Flying",), ["Highlands"])
Sprite = Creature("Sprite", 1, 2, 2, (1, 3), 3, 9, 95, 1, 0, True, True, "Conflux", ("Flying", "No enemy retaliation"), ["Highlands"])

Air_Elemental = Creature("Air_Elemental", 2, 9, 9, (2, 8), 25, 7, 356, 1, 0, False, False, "Conflux", ("Elemental",
                                                                        "Lightning and Armageddon vulnerability",
                                                                        "Immune to Meteor Shower",
                                                                        "+100% to basic damage to Earth and Magma Elementals"), ["Highlands"])
Storm_Elemental = Creature("Storm_Elemental", 2, 9, 9, (2, 8), 25, 8, 486, 1, 24, False, True, "Conflux", ("Elemental",
                                                                            "Lightning and Armageddon vulnerability",
                                                                            "Immune to Meteor Shower",
                                                                            "+100% to basic damage to Earth and Magma Elementals",
                                                                            "Casts Protection from Air"), ["Highlands"])

Water_Elemental = Creature("Water_Elemental", 3, 8, 10, (3, 7), 30, 5, 315, 2, 0, False, False, "Conflux", ("Elemental",
                                                                             "Ice immunity",
                                                                             "Vulnerable to Fireball, Inferno and Armageddon",
                                                                             "+100% to basic damage to Fire and Energy Elementals"), ["Highlands"])
Ice_Elemental = Creature("Ice_Elemental", 3, 8, 10, (3, 7), 30, 6, 380, 2, 24, False, True, "Conflux", ("Elemental",
                                                                         "Ice immunity",
                                                                         "Vulnerable to Fireball, Inferno and Armageddon",
                                                                         "+100% to basic damage to Fire and Energy Elementals",
                                                                         "Casts Protection from Water"), ["Highlands"])

Fire_Elemental = Creature("Fire_Elemental", 4, 10, 8, (4, 6), 35, 6, 345, 1, 0, False, False, "Conflux", ("Elemental",
                                                                           "Ice vulnerability",
                                                                           "Fire immunity",
                                                                           "+100% to basic damage to Water and Ice Elementals"), ["Highlands"])
Energy_Elemental = Creature("Energy_Elemental", 4, 12, 8, (4, 6), 35, 8, 470, 1, 0, True, True, "Conflux", ("Elemental",
                                                                               "Ice vulnerability",
                                                                               "Fire immunity",
                                                                               "+100% to basic damage to Water and Ice Elementals",
                                                                               "Casts Protection from Fire"), ["Highlands"])

Earth_Elemental = Creature("Earth_Elemental", 5, 10, 10, (4, 8), 40, 4, 330, 1, 0, False, False, "Conflux", ("Elemental",
                                                                              " Meteor Shower vulnerability",
                                                                              "Lightning and Armageddon immunity",
                                                                              "+100% to basic damage to Air and Storm Elementals"), ["Highlands"])
Magma_Elemental = Creature("Magma_Elemental", 5, 11, 11, (6, 10), 40, 6, 490, 1, 0, False, True, "Conflux", ("Elemental",
                                                                               "Meteor Shower vulnerability",
                                                                               "Lightning and Armageddon immunity",
                                                                               "+100% to basic damage to Air and Storm Elementals",
                                                                               "Casts Protection from Earth"), ["Highlands"])

Psychic_Elemental = Creature("Psychic_Elemental", 6, 15, 13, (10, 20), 75, 7, 1669, 1, 0, False, False, "Conflux", ("Elemental",
                                                                                     "Attacks all adjacent enemies without retaliation",
                                                                                     "-50% damage to creatures with Mind immunity"), ["Highlands"])
Magic_Elemental = Creature("Magic_Elemental", 6, 15, 13, (15, 25), 80, 9, 2012, 1, 0, False, True, "Conflux", ("Elemental",
                                                                                 "Attacks all adjacent enemies without retaliation",
                                                                                 "Magic immunity",
                                                                                 "-50% damage to creatures with Magic immunity"), ["Highlands"])

Firebird = Creature("Firebird", 7, 18, 18, (30, 40), 150, 15, 4336, 2, 0, True, False, "Conflux", ("Breath attack", "50% fire resistance"), ["Highlands"])
Phoenix = Creature("Phoenix", 7, 21, 18, (30, 40), 200, 21, 6721, 2, 0, True, True, "Conflux",
                   ("Breath attack", "Fire immunity", "Rebirth"), ["Highlands"])

# Cove
Nymph = Creature("Nymph", 1, 5, 2, (1, 2), 4, 6, 57, 1, 0, True, False, "Cove", ("Immune to ice",), ["Swamp"])
Oceanid = Creature("Oceanid", 1, 6, 2, (1, 3), 4, 8, 75, 1, 0, True, True, "Cove", ("Immune to ice",), ["Swamp"])

Crew_Mate = Creature("Crew_Mate", 2, 7, 4, (2, 4), 15, 5, 155, 1, 0, False, False, "Cove", ("None",), ["Swamp"])
Seaman = Creature("Seaman", 2, 8, 6, (3, 4), 15, 6, 174, 1, 0, False, True, "Cove", ("None",), ["Swamp"])

Pirate = Creature("Pirate", 3, 8, 6, (3, 7), 15, 6, 312, 1, 4, False, False, "Cove", ("No melee penalty",), ["Swamp"])
Corsair = Creature("Corsair", 3, 10, 8, (3, 7), 15, 7, 407, 1, 4, False, True, "Cove", ("No melee penalty", "No enemy retaliation"), ["Swamp"])
Sea_Dog = Creature("Sea_Dog", 3, 12, 11, (3, 7), 15, 8, 602, 2, 12, False, True, "Cove",
                   ("No melee penalty", "No enemy retaliation", "Accurate Shot"), ["Swamp"])

Stormbird = Creature("Stormbird", 4, 10, 8, (6, 9), 30, 9, 502, 2, 0, True, False, "Cove", ("None",), ["Swamp"])
Ayssid = Creature("Ayssid", 4, 11, 8, (6, 10), 30, 11, 645, 2, 0, True, True, "Cove", ("Ferocity",), ["Swamp"])

Sea_Witch = Creature("Sea_Witch", 5, 12, 7, (10, 14), 35, 6, 790, 1, 12, False, False, "Cove", (" Cast Weakness/Disrupting Ray",), ["Swamp"])
Sorceress = Creature("Sorceress", 5, 12, 9, (10, 16), 35, 7, 852, 1, 12, False, True, "Cove", (" Cast Weakness/Disrupting Ray",), ["Swamp"])

Nix = Creature("Nix", 6, 13, 16, (18, 22), 80, 6, 1415, 1, 0, False, False, "Cove", ("Ignores 30% of enemy attack value",), ["Swamp"])
Nix_Warrior = Creature("Nix_Warrior", 6, 14, 17, (18, 22), 90, 7, 2116, 1, 0, False, True, "Cove", ("Ignores 60% of enemy attack value",), ["Swamp"])

Sea_Serpent = Creature("Sea_Serpent", 7, 22, 16, (30, 55), 180, 9, 3953, 2, 0, False, False, "Cove", ("Poisonous",), ["Swamp"])
Haspid = Creature("Haspid", 7, 29, 20, (30, 55), 300, 12, 7220, 2, 0, False, True, "Cove", ("Poisonous", "Revenge"), ["Swamp"])

# Neutral
Peasant = Creature("Peasant", 1, 1, 1, (1, 1), 1, 3, 15, 1, 0, False, False, "Neutral", ("None",), [])
Halfling = Creature("Halfling", 1, 4, 2, (1, 3), 4, 5, 75, 1, 24, False, False, "Neutral", ("Always have +1 luck",), [])

Rogue = Creature("Rogue", 2, 8, 3, (2, 4), 10, 6, 135, 1, 0, False, False, "Neutral", ("Spying",), [])
Boar = Creature("Boar", 2, 6, 5, (2, 3), 15, 6, 145, 2, 0, False, False, "Neutral", ("None",), [])
Leprechaun = Creature("Leprechaun", 2, 8, 5, (3, 5), 15, 5, 208, 1, 0, False, False, "Neutral", ("Doubles friendly unit Luck chance", "Casts Fortune"), [])

Nomad = Creature("Nomad", 3, 9, 8, (2, 6), 30, 7, 345, 2, 0, False, False, "Neutral", ("Sandwalker",), [])
Mummy = Creature("Mummy", 3, 7, 7, (3, 5), 30, 5, 270, 1, 0, False, False, "Neutral", ("Undead", "Curses enemies"), [])

Sharpshooter = Creature("Sharpshooter", 4, 12, 10, (8, 10), 15, 9, 585*5, 1, 32, False, False, "Neutral",
                        ("No range penalty", "No obstacle penalty"), [])
Satyr = Creature("Satyr", 4, 10, 11, (6, 10), 35, 7, 518, 1, 0, False, False, "Neutral", ("Casts mirth",), [])
Steel_Golem = Creature("Steel_Golem", 4, 10, 11, (6, 8), 45, 6, 597, 1, 0, False, False, "Neutral", ("Spell damage resistance 80%", "Non-living"), [])

Troll = Creature("Troll", 5, 14, 7, (10, 15), 40, 7, 1024, 1, 0, False, False, "Neutral", ("Regenerating",), [])
Gold_Golem = Creature("Gold_Golem", 5, 11, 12, (8, 10), 50, 5, 600, 1, 0, False, False, "Neutral", ("Spell damage resistance 85%", "Non-living"), [])
Fangarm = Creature("Fangarm", 5, 12, 12, (8, 12), 50, 6, 929, 1, 0, True, False, "Neutral",
                   ("Mind spell immunity", "Unlimited retaliation", "Hypnotize"), [])

Diamond_Golem = Creature("Diamond_Golem", 6, 13, 12, (10, 14), 60, 5, 775, 1, 0, False, False, "Neutral",
                         ("Spell damage resistance 95%", "Non-living"), [])
Enchanter = Creature("Enchanter", 6, 17, 12, (14, 14), 30, 9, 1210, 1, 32, False, False, "Neutral",
                     ("No melee penalty", "Spellcaster", "No obstacle penalty"), [])

Faerie_Dragon = Creature("Faerie_Dragon", 7, 20, 20, (20, 30), 500, 15, 19580, 2, 0, True, False, "Neutral",
                         ("Dragon", "Spellcaster", "Natural Magic Mirror"), [])
Rust_Dragon = Creature("Rust_Dragon", 7, 30, 30, (50, 50), 750, 17, 26433, 2, 0, True, False, "Neutral",
                       ("Acid breath", "Breath attack", "Dragon"), [])
Crystal_Dragon = Creature("Crystal_Dragon", 7, 40, 40, (60, 75), 800, 16, 39338, 2, 0, False, False, "Neutral",
                          ("Dragon", "Crystal generation", "Magic resistance +20%"), [])
Azure_Dragon = Creature("Azure_Dragon", 7, 50, 50, (70, 80), 1000, 19, 78845, 2, 0, True, False, "Neutral",
                        ("Breath attack", "Dragon", "Fear", "Immune to lvl 1-3 spells", "Immune to Fear"), [])

Ballista = Creature("Ballista", 1, 10, 10, (2, 3), 250, 1, 126, 1, 24, True, False, "Neutral", ("None",), [])
# moves only after the arrow towers
Catapult = Creature("Catapult", 1, 10, 10, (2, 3), 1000, 30, 126, 1, 24, True, False, "Neutral", ("None",), [])

FirstAid = Creature("FirstAid", 1, 0, 0, (0, 0), 75, 0, 300, 1, 0, True, False, "Neutral", ("None",), [])