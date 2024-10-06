from enum import IntEnum


class IntGlobals(IntEnum):
    OBJECT_INVALID = -1
    HNULL = 0
    HNONE = 0xFF
    HNONETOWN = 0x1FF
    PLAYER_SUM = 8


class Version(IntEnum):
    ROE = 0x0E
    AB = 0x15
    SOD = 0x1C
    HOTA = 0x20
    WOG = 0x33


class Behaviour(IntEnum):
    Random = 0
    Warrior = 1
    Builder = 2
    Explorer = 3
    NoClue = 0xFF


class MapObjects(IntEnum):
    NONE = 0
    HERO = 1
    TOWN = 2
    MONSTER = 3


class MapSpecial(IntEnum):
    NONE = 0
    MINE = 1
    ARTIFACT = 2
    MONSTER = 3
    ANY = 4


class TileType(IntEnum):
    FREE = 0
    POSSIBLE = 1
    BLOCKED = 2
    USED = 3
    ACCESSIBLE = 1


class BlockMapBits(IntEnum):
    VISIBLE = 1
    VISITABLE = 2
    BLOCKED = 4
    COMBINED = 6


class TERRAIN(IntEnum):
    DIRT = 0
    SAND = 1
    GRASS = 2
    SNOW = 3
    SWAMP = 4
    ROUGH = 5
    SUBTERRANEAN = 6
    LAVA = 7
    WATER = 8
    ROCK = 9
    HIGHLANDS = 10
    WASTELAND = 11

    # blocked

    BLOCKED_DIRT = 20
    BLOCKED_SAND = 21
    BLOCKED_GRASS = 22
    BLOCKED_SNOW = 23
    BLOCKED_SWAMP = 24
    BLOCKED_ROUGH = 25
    BLOCKED_SUBTERRANEAN = 26
    BLOCKED_LAVA = 27
    BLOCKED_WATER = 28
    BLOCKED_ROCK = 29
    BLOCKED_HIGHLANDS = 30
    BLOCKED_WASTELAND = 31

    # players

    RED = 40
    BLUE = 41
    TAN = 42
    GREEN = 43
    ORANGE = 44
    PURPLE = 45
    TEAL = 46
    PINK = 47
    NEUTRAL = 48

    # special

    NONE = 50
    MINE = 51
    ARTIFACT = 52
    MONSTER = 53
    ANY = 54

    # offsets

    OFFSET_BLOCKED = 200
    OFFSET_PLAYERS = 40
    OFFSET_SPECIAL = 50

    # count

    TERRAIN_NUMBER = 12


class Victory(IntEnum):
    ARTIFACT = 0
    ACCUMULATE_CREATURES = 1
    ACCUMULATE_RESOURCES = 2
    UPGRADE_TOWN = 3
    BUILD_GRAIL = 4
    DEFEAT_HERO = 5
    CAPTURE_TOWN = 6
    KILL_MONSTER = 7
    FLAG_DWELLINGS = 8
    FLAG_MINES = 9
    TRANSPORT_ARTIFACT = 10
    ELIMINATE_MONSTERS = 11
    SURVIVE_TIME = 12
    NONE = 0xFF


class Loss(IntEnum):
    TOWN = 0
    HERO = 1
    TIME = 2
    NONE = 0xFF


class Objects(IntEnum):
    NO_OBJECT = -1
    ALTAR_OF_SACRIFICE = 2
    ANCHOR_PO = 3
    ARENA = 4
    ARTIFACT = 5
    PANDORAS_BOX = 6
    BLACK_MARKET = 7
    BOAT = 8
    BORDER_GUARD = 9
    KEY_MASTER = 10
    BUOY = 11
    CAMPFIRE = 12
    CARTOGRAPHER = 13
    SWAN_POND = 14
    COVER_OF_DARKNESS = 15
    CREATURE_BANK = 16
    CREATURE_GENERATOR1 = 17
    CREATURE_GENERATOR2 = 18
    CREATURE_GENERATOR3 = 19
    CREATURE_GENERATOR4 = 20
    CURSED_GROUND1 = 21
    CORPSE = 22
    MARLETTO_TOWER = 23
    DERELICT_SHIP = 24
    DRAGON_UTOPIA = 25
    EVENT = 26
    EYE_OF_MAGI = 27
    FAERIE_RING = 28
    FLOTSAM = 29
    FOUNTAIN_OF_FORTUNE = 30
    FOUNTAIN_OF_YOUTH = 31
    GARDEN_OF_REVELATION = 32
    GARRISON = 33
    HERO = 34
    HILL_FORT = 35
    GRAIL = 36
    HUT_OF_MAGI = 37
    IDOL_OF_FORTUNE = 38
    LEAN_TO = 39
    LIBRARY_OF_ENLIGHTENMENT = 41
    LIGHTHOUSE = 42
    MONOLITH_ONE_WAY_ENTRANCE = 43
    MONOLITH_ONE_WAY_EXIT = 44
    MONOLITH_TWO_WAY = 45
    MAGIC_PLAINS1 = 46
    SCHOOL_OF_MAGIC = 47
    MAGIC_SPRING = 48
    MAGIC_WELL = 49
    MERCENARY_CAMP = 51
    MERMAID = 52
    MINE = 53
    MONSTER = 54
    MYSTICAL_GARDEN = 55
    OASIS = 56
    OBELISK = 57
    REDWOOD_OBSERVATORY = 58
    OCEAN_BOTTLE = 59
    PILLAR_OF_FIRE = 60
    STAR_AXIS = 61
    PRISON = 62
    PYRAMID = 63
    WOG_OBJECT = 63
    RALLY_FLAG = 64
    RANDOM_ART = 65
    RANDOM_TREASURE_ART = 66
    RANDOM_MINOR_ART = 67
    RANDOM_MAJOR_ART = 68
    RANDOM_RELIC_ART = 69
    RANDOM_HERO = 70
    RANDOM_MONSTER = 71
    RANDOM_MONSTER_L1 = 72
    RANDOM_MONSTER_L2 = 73
    RANDOM_MONSTER_L3 = 74
    RANDOM_MONSTER_L4 = 75
    RANDOM_RESOURCE = 76
    RANDOM_TOWN = 77
    REFUGEE_CAMP = 78
    RESOURCE = 79
    SANCTUARY = 80
    SCHOLAR = 81
    SEA_CHEST = 82
    SEER_HUT = 83
    CRYPT = 84
    SHIPWRECK = 85
    SHIPWRECK_SURVIVOR = 86
    SHIPYARD = 87
    SHRINE_OF_MAGIC_INCANTATION = 88
    SHRINE_OF_MAGIC_GESTURE = 89
    SHRINE_OF_MAGIC_THOUGHT = 90
    SIGN = 91
    SIRENS = 92
    SPELL_SCROLL = 93
    STABLES = 94
    TAVERN = 95
    TEMPLE = 96
    DEN_OF_THIEVES = 97
    TOWN = 98
    TRADING_POST = 99
    LEARNING_STONE = 100
    TREASURE_CHEST = 101
    TREE_OF_KNOWLEDGE = 102
    SUBTERRANEAN_GATE = 103
    UNIVERSITY = 104
    WAGON = 105
    WAR_MACHINE_FACTORY = 106
    SCHOOL_OF_WAR = 107
    WARRIORS_TOMB = 108
    WATER_WHEEL = 109
    WATERING_HOLE = 110
    WHIRLPOOL = 111
    WINDMILL = 112
    WITCH_HUT = 113
    HOLE = 124
    RANDOM_MONSTER_L5 = 162
    RANDOM_MONSTER_L6 = 163
    RANDOM_MONSTER_L7 = 164
    BORDER_GATE = 212
    FREELANCERS_GUILD = 213
    HERO_PLACEHOLDER = 214
    QUEST_GUARD = 215
    RANDOM_DWELLING = 216
    RANDOM_DWELLING_LVL = 217
    RANDOM_DWELLING_FACTION = 218
    GARRISON2 = 219
    ABANDONED_MINE = 220
    TRADING_POST_SNOW = 221
    CLOVER_FIELD = 222
    CURSED_GROUND2 = 223
    EVIL_FOG = 224
    FAVORABLE_WINDS = 225
    FIERY_FIELDS = 226
    HOLY_GROUNDS = 227
    LUCID_POOLS = 228
    MAGIC_CLOUDS = 229
    MAGIC_PLAINS2 = 230
    ROCKLANDS = 231


class RewardType(IntEnum):
    NOTHING = 0
    EXPERIENCE = 1
    MANA_POINTS = 2
    MORALE_BONUS = 3
    LUCK_BONUS = 4
    RESOURCES = 5
    PRIMARY_SKILL = 6
    SECONDARY_SKILL = 7
    ARTIFACT = 8
    SPELL = 9
    CREATURE = 10


class QuestMission(IntEnum):
    NONE = 0
    LEVEL = 1
    PRIMARY_STAT = 2
    KILL_HERO = 3
    KILL_CREATURE = 4
    ART = 5
    ARMY = 6
    RESOURCES = 7
    HERO = 8
    PLAYER = 9
    KEYMASTER = 10
    HOTA_EXTRA = 10
    HOTA_CLASS = 0
    HOTA_NOTBEFORE = 1


class HeroesConstants:
    PlayersColors = {0: 'Red',
                     1: 'Blue',
                     2: 'Tan',
                     3: 'Green',
                     4: 'Orange',
                     5: 'Purple', 
                     6: 'Teal',
                     7: 'Pink',
                     0xFF: 'Neutral'}

    PrimarySkill = {0: 'Attack',
                    1: 'Defense',
                    2: 'SpellPower',
                    3: 'Knowledge',
                    4: 'Experience'}

    SecondarySkill = {-1: 'Default',
                      0: 'Pathfinding',
                      1: 'Archery',
                      2: 'Logistics',
                      3: 'Scouting',
                      4: 'Diplomacy',
                      5: 'Navigation',
                      6: 'Leadership',
                      7: 'Wisdom',
                      8: 'Mysticism',
                      9: 'Luck',
                      10: 'Ballistics',
                      11: 'EagleEye',
                      12: 'Necromancy',
                      13: 'Estates',
                      14: 'FireMagic',
                      15: 'AirMagic',
                      16: 'WaterMagic',
                      17: 'EarthMagic',
                      18: 'Scholar',
                      19: 'tactics',
                      20: 'Artillery',
                      21: 'Learning',
                      22: 'Offense',
                      23: 'Armorer',
                      24: 'Intelligence',
                      25: 'Sorcery',
                      26: 'Resistance',
                      27: 'FirstAid'}

    Alignment = {0: 'Good',
                 1: 'Evil',
                 2: 'Neutral'}

    TownType = {-1: 'Any',
                0: 'Castle',
                1: 'Rampart',
                2: 'Tower',
                3: 'Inferno',
                4: 'Necropolis',
                5: 'Dungeon',
                6: 'Stronghold',
                7: 'Fortress',
                8: 'Conflux',
                9: 'Neutral/Cove'}

    AiTactics = {-1: 'None',
                 0: 'Random',
                 1: 'Warrior',
                 2: 'Builder',
                 3: 'Explorer'}

    TileType = {TileType.FREE: 'Free',
                TileType.POSSIBLE: 'Possible',
                TileType.BLOCKED: 'Blocked',
                TileType.USED: 'Used'}

    SecSkillLevel = {0: 'None',
                     1: 'Basic',
                     2: 'Advanced',
                     3: 'Expert'}

    TerrainType = {0: 'Dirt',
                   1: 'Sand',
                   2: 'Grass',
                   3: 'Snow',
                   4: 'Swamp',
                   5: 'Rough',
                   6: 'Subterranean',
                   7: 'Lava',
                   8: 'Water',
                   9: 'Rock',
                   10: 'Highlands',
                   11: 'Wasteland'}

    RoadType ={0: 'None',
               1: 'Dirt road',
               2: 'Gravel road',
               3: 'Cobblestone road'}

    ArtifactPosition = {-2: 'First available',
                        -1: 'Pre first',  # Sometimes used as error or first free in backpack
                        0: 'Head',
                        1: 'Shoulders',
                        2: 'Neck',
                        3: 'Right hand',
                        4: 'Left hand',
                        5: 'Torso',
                        6: 'Right ring',
                        7: 'Left ring',
                        8: 'Feet',
                        9: 'Misc1',
                        10: 'Misc2',
                        11: 'Misc3',
                        12: 'Misc4',
                        13: 'Mach1',
                        14: 'Mach2',
                        15: 'Mach3',
                        16: 'Mach4',
                        17: 'Spellbook',
                        18: 'Misc5',
                        19: 'Backpack'}

    SpellID = {-2: 'Preset',
               -1: 'None',
               0: 'Summon Boat',
               1: 'Scuttle Boat',
               2: 'Visions',
               3: 'View Earth',
               4: 'Disguise',
               5: 'View Air',
               6: 'Fly',
               7: 'Water Walk',
               8: 'Dimension Door',
               9: 'Town Portal',
               10: 'Quicksand',
               11: 'Land Mine',
               12: 'Force Field',
               13: 'Fire Wall',
               14: 'Earthquake',
               15: 'Magic Arrow',
               16: 'Ice Bolt',
               17: 'Lightning Bolt',
               18: 'Implosion',
               19: 'Chain Lightning',
               20: 'Frost Ring',
               21: 'Fireball',
               22: 'Inferno',
               23: 'Meteor Shower',
               24: 'Death Ripple',
               25: 'Destroy Undead',
               26: 'Armageddon',
               27: 'Shield',
               28: 'Air Shield',
               29: 'Fire Shield',
               30: 'Protection From Air',
               31: 'Protection From Fire',
               32: 'Protection From Water',
               33: 'Protection From Earth',
               34: 'Anti Magic',
               35: 'Dispel',
               36: 'Magic Mirror',
               37: 'Cure',
               38: 'Resurrection',
               39: 'Animate Dead',
               40: 'Sacrifice',
               41: 'Bless',
               42: 'Curse',
               43: 'Bloodlust',
               44: 'Precision',
               45: 'Weakness',
               46: 'Stone Skin',
               47: 'Disrupting Ray',
               48: 'Prayer',
               49: 'Mirth',
               50: 'Sorrow',
               51: 'Fortune',
               52: 'Misfortune',
               53: 'Haste',
               54: 'Slow',
               55: 'Slayer',
               56: 'Frenzy',
               57: 'Titans Lightning Bolt',
               58: 'Counterstrike',
               59: 'Berserk',
               60: 'Hypnotize',
               61: 'Forgetfulness',
               62: 'Blind',
               63: 'Teleport',
               64: 'Remove Obstacle',
               65: 'Clone',
               66: 'Summon Fire Elemental',
               67: 'Summon Earth Elemental',
               68: 'Summon Water Elemental',
               69: 'Summon Air Elemental',
               70: 'First Non Spell',
               71: 'Poison',
               72: 'Bind',
               73: 'Disease',
               74: 'Paralyze',
               75: 'Age',
               76: 'Death Cloud',
               77: 'Thunderbolt',
               78: 'Dispel Helpful Spells',
               79: 'Death Stare',
               80: 'Acid Breath Defense',
               81: 'Acid Breath Damage',
               82: 'After Last',
               }

    Monster = {0: 'Pikeman',
               1: 'Halberdier',
               2: 'Archer',
               3: 'Marksman',
               4: 'Griffin',
               5: 'Royal Griffin',
               6: 'Swordsman',
               7: 'Crusader',
               8: 'Monk',
               9: 'Zealot',
               10: 'Cavalier',
               11: 'Champion',
               12: 'Angel',
               13: 'Archangel',
               14: 'Centaur',
               15: 'Centaur Captain',
               16: 'Dwarf',
               17: 'Battle Dwarf',
               18: 'Wood Elf',
               19: 'Grand Elf',
               20: 'Pegasus',
               21: 'Silver Pegasus',
               22: 'Dendroid Guard',
               23: 'Dendroid Soldier',
               24: 'Unicorn',
               25: 'War Unicorn',
               26: 'Green Dragon',
               27: 'Gold Dragon',
               28: 'Gremlin',
               29: 'Master Gremlin',
               30: 'Stone Gargoyle',
               31: 'Obsidian Gargoyle',
               32: 'Stone Golem',
               33: 'Iron Golem',
               34: 'Mage',
               35: 'Arch Mage',
               36: 'Genie',
               37: 'Master Genie',
               38: 'Naga',
               39: 'Naga Queen',
               40: 'Giant',
               41: 'Titan',
               42: 'Imp',
               43: 'Familiar',
               44: 'Gog',
               45: 'Magog',
               46: 'Hell Hound',
               47: 'Cerberus',
               48: 'Demon',
               49: 'Horned Demon',
               50: 'Pit Fiend',
               51: 'Pit Lord',
               52: 'Efreeti',
               53: 'Efreet Sultan',
               54: 'Devil',
               55: 'Arch Devil',
               56: 'Skeleton',
               57: 'Skeleton Warrior',
               58: 'Walking Dead',
               59: 'Zombie',
               60: 'Wight',
               61: 'Wraith',
               62: 'Vampire',
               63: 'Vampire Lord',
               64: 'Lich',
               65: 'Power Lich',
               66: 'Black Knight',
               67: 'Dread Knight',
               68: 'Bone Dragon',
               69: 'Ghost Dragon',
               70: 'Troglodyte',
               71: 'Infernal Troglodyte',
               72: 'Harpy',
               73: 'Harpy Hag',
               74: 'Beholder',
               75: 'Evil Eye',
               76: 'Medusa',
               77: 'Medusa Queen',
               78: 'Minotaur',
               79: 'Minotaur King',
               80: 'Manticore',
               81: 'Scorpicore',
               82: 'Red Dragon',
               83: 'Black Dragon',
               84: 'Goblin',
               85: 'Hobgoblin',
               86: 'Wolf Rider',
               87: 'Wolf Raider',
               88: 'Orc',
               89: 'Orc Chieftain',
               90: 'Ogre',
               91: 'Ogre Mage',
               92: 'Roc',
               93: 'Thunderbird',
               94: 'Cyclops',
               95: 'Cyclops King',
               96: 'Behemoth',
               97: 'Ancient Behemoth',
               98:  'Gnoll',
               99: 'Gnoll Marauder',
               100: 'Lizardman',
               101: 'Lizard Warrior',
               102: 'Gorgon',
               103: 'Mighty Gorgon',
               104: 'Serpent Fly',
               105: 'Dragon Fly',
               106: 'Basilisk',
               107: 'Greater Basilisk',
               108: 'Wyvern',
               109: 'Wyvern Monarch',
               110: 'Hydra',
               111: 'Chaos Hydra',
               112: 'Air Elemental',
               113: 'Earth Elemental',
               114: 'Fire Elemental',
               115: 'Water Elemental',
               116: 'Gold Golem',
               117: 'Diamond Golem',
               118: 'Pixie',
               119: 'Sprite',
               120: 'Psychic Elemental',
               121: 'Magic Elemental',
               122: 'NOT USED (attacker)',
               123: 'Ice Elemental',
               124: 'NOT USED (defender)',
               125: 'Magma Elemental',
               126: 'NOT USED (3)',
               127: 'Storm Elemental',
               128: 'NOT USED (4)',
               129: 'Energy Elemental',
               130: 'Firebird',
               131: 'Phoenix',
               132: 'Azure Dragon',
               133: 'Crystal Dragon',
               134: 'Faerie Dragon',
               135: 'Rust Dragon',
               136: 'Enchanter',
               137: 'Sharpshooter',
               138: 'Halfling',
               139: 'Peasant',
               140: 'Boar',
               141: 'Mummy',
               142: 'Nomad',
               143: 'Rogue',
               144: 'Troll',
               145: 'Catapult (specialty X1)',
               146: 'Ballista (specialty X1)',
               147: 'First Aid Tent (specialty X1)',
               148: 'Ammo Cart (specialty X1)',
               149: 'Arrow Towers (specialty X1)',
               # HOTA
               151: 'Sea Dog',
               153: 'Nymph',
               154: 'Oceanid',
               155: 'Crew Mate',
               156: 'Seaman',
               157: 'Pirate',
               158: 'Corsair',
               159: 'Stormbird',
               160: 'Ayssid',
               161: 'Sea Witch',
               162: 'Sorceress',
               163: 'Nix',
               164: 'Nix Warrior',
               165: 'Sea Serpent',
               166: 'Haspid',
               167: 'Leprechaun',
               168: 'Satyr',
               169: 'Steel Golem',
               170: 'Fangarm',
               255: 'Random'}

    MonsterWOG = {150: 'Supreme Archangel',
                  151: 'Diamond Dragon',
                  152: 'Lord of Thunder',
                  153: 'Antichrist',
                  154: 'Blood Dragon',
                  155: 'Darkness Dragon',
                  156: 'Ghost Behemoth',
                  157: 'Hell Hydra',
                  158: 'Sacred Phoenix',
                  159: 'Ghost',
                  160: 'Emissary of War',
                  161: 'Emissary of Peace',
                  162: 'Emissary of Mana',
                  163: 'Emissary of Lore',
                  164: 'Fire Messenger',
                  165: 'Earth Messenger',
                  166: 'Air Messenger',
                  167: 'Water Messenger',
                  168: 'Gorynych',
                  169: 'War zealot',
                  170: 'Arctic Sharpshooter',
                  171: 'Lava Sharpshooter',
                  172: 'Nightmare',
                  173: 'Santa Gremlin',
                  174: 'Paladin (attacker)',
                  175: 'Hierophant (attacker)',
                  176: 'Temple Guardian (attacker)',
                  177: 'Succubus (attacker)',
                  178: 'Soul Eater (attacker)',
                  179: 'Brute (attacker)',
                  180: 'Ogre Leader (attacker)',
                  181: 'Shaman (attacker)',
                  182: 'Astral Spirit (attacker)',
                  183: 'Paladin (defender)',
                  184: 'Hierophant (defender)',
                  185: 'Temple Guardian (defender)',
                  186: 'Succubus (defender)',
                  187: 'Soul Eater (defender)',
                  188: 'Brute (defender)',
                  189: 'Ogre Leader (defender)',
                  190: 'Shaman (defender)',
                  191: 'Astral Spirit (defender)',
                  192: 'Sylvan Centaur',
                  193: 'Sorceress',
                  194: 'Werewolf',
                  195: 'Hell Steed',
                  196: 'Dracolich',
                  1000: 'Random lvl 1',
                  1001: 'Random lvl 1 Upg',
                  1002: 'Random lvl 2',
                  1003: 'Random lvl 2 Upg',
                  1004: 'Random lvl 3',
                  1005: 'Random lvl 3 Upg',
                  1006: 'Random lvl 4',
                  1007: 'Random lvl 4 Upg',
                  1008: 'Random lvl 5',
                  1009: 'Random lvl 5 Upg',
                  1010: 'Random lvl 6',
                  1011: 'Random lvl 6 Upg',
                  1012: 'Random lvl 7',
                  1013: 'Random lvl 7 Upg'}

    MonChar = {0: 'Always join',
               1: 'Likely join',
               2: 'May join',
               3: 'Unlikely to join',
               4: 'Never join'}

    Objects = {0: 'None',
               1: 'None',
               2: 'Altar of Sacrifice',
               3: 'Anchor Point',
               4: 'Arena',
               5: 'Artifact',
               6: 'Pandoras Box',
               7: 'Black Market',
               8: 'Boat',
               9: 'Borderguard',
               10: 'Keymasters Tent',
               11: 'Buoy',
               12: 'Campfire',
               13: 'Cartographer',
               14: 'Swan Pond',
               15: 'Cover of Darkness',
               16: 'Creature Bank',
               17: 'Creature Generator 1',
               18: 'Creature Generator 2',
               19: 'Creature Generator 3',
               20: 'Creature Generator 4',
               21: 'Cursed Ground',
               22: 'Corpse',
               23: 'Marletto Tower',
               24: 'Derelict Ship',
               25: 'Dragon Utopia',
               26: 'Event',
               27: 'Eye of the Magi',
               28: 'Faerie Ring',
               29: 'Flotsam',
               30: 'Fountain of Fortune',
               31: 'Fountain of Youth',
               32: 'Garden of Revelation',
               33: 'Garrison',
               34: 'Hero',
               35: 'Hill Fort',
               36: 'Grail',
               37: 'Hut of the Magi',
               38: 'Idol of Fortune',
               39: 'Lean To',
               40: '<blank>',
               41: 'Library of Enlightenment',
               42: 'Lighthouse',
               43: 'Monolith One Way Entrance',
               44: 'Monolith One Way Exit',
               45: 'Monolith Two Way',
               46: 'Magic Plains',
               47: 'School of Magic',
               48: 'Magic Spring',
               49: 'Magic Well',
               50: '<blank>',
               51: 'Mercenary Camp',
               52: 'Mermaid',
               53: 'Mine',
               54: 'Monster',
               55: 'Mystical Garden',
               56: 'Oasis',
               57: 'Obelisk',
               58: 'Redwood Observatory',
               59: 'Ocean Bottle',
               60: 'Pillar of Fire',
               61: 'Star Axis',
               62: 'Prison',
               63: 'Pyramid',
               64: 'Rally Flag',
               65: 'Random Artifact',
               66: 'Random Treasure Artifact',
               67: 'Random Minor Artifact',
               68: 'Random Major Artifact',
               69: 'Random Relic',
               70: 'Random Hero',
               71: 'Random Monster',
               72: 'Random Monster 1',
               73: 'Random Monster 2',
               74: 'Random Monster 3',
               75: 'Random Monster 4',
               76: 'Random Resource',
               77: 'Random Town',
               78: 'Refugee Camp',
               79: 'Resource',
               80: 'Sanctuary',
               81: 'Scholar',
               82: 'Sea Chest',
               83: 'Seers Hut',
               84: 'Crypt',
               85: 'Shipwreck',
               86: 'Shipwreck Survivor',
               87: 'Shipyard',
               88: 'Shrine of Magic Incantation',
               89: 'Shrine of Magic Gesture',
               90: 'Shrine of Magic Thought',
               91: 'Sign',
               92: 'Sirens',
               93: 'Spell Scroll',
               94: 'Stables',
               95: 'Tavern',
               96: 'Temple',
               97: 'Den of Thieves',
               98: 'Town',
               99: 'Trading Post',
               100: 'Learning Stone',
               101: 'Treasure Chest',
               102: 'Tree of Knowledge',
               103: 'Subterranean Gate',
               104: 'University',
               105: 'Wagon',
               106: 'War Machine Factory',
               107: 'School of War',
               108: 'Warriors Tomb',
               109: 'Water Wheel',
               110: 'Watering Hole',
               111: 'Whirlpool',
               112: 'Windmill',
               113: 'Witch Hut',
               114: 'Brush',
               115: 'Bush',
               116: 'Cactus',
               117: 'Canyon',
               118: 'Crater',
               119: 'Dead Vegetation',
               120: 'Flowers',
               121: 'Frozen Lake',
               122: 'Hedge',
               123: 'Hill',
               124: 'Hole',
               125: 'Kelp',
               126: 'Lake',
               127: 'Lava Flow',
               128: 'Lava Lake',
               129: 'Mushrooms',
               130: 'Log',
               131: 'Mandrake',
               132: 'Moss',
               133: 'Mound',
               134: 'Mountain',
               135: 'Oak Trees',
               136: 'Outcropping',
               137: 'Pine Trees',
               138: 'Plant',
               143: 'River Delta',
               147: 'Rock',
               148: 'Sand Dune',
               149: 'Sand Pit',
               150: 'Shrub',
               151: 'Skull',
               152: 'Stalagmite',
               153: 'Stump',
               154: 'Tar Pit',
               155: 'Trees',
               156: 'Vine',
               157: 'Volcanic Vent',
               158: 'Volcano',
               159: 'Willow Trees',
               160: 'Yucca Trees',
               161: 'Reef',
               162: 'Random Monster 5',
               163: 'Random Monster 6',
               164: 'Random Monster 7',
               165: 'Brush',
               166: 'Bush',
               167: 'Cactus',
               168: 'Canyon',
               169: 'Crater',
               170: 'Dead Vegetation',
               171: 'Flowers',
               172: 'Frozen Lake',
               173: 'Hedge',
               174: 'Hill',
               175: 'Hole',
               176: 'Kelp',
               177: 'Lake',
               178: 'Lava Flow',
               179: 'Lava Lake',
               180: 'Mushrooms',
               181: 'Log',
               182: 'Mandrake',
               183: 'Moss',
               184: 'Mound',
               185: 'Mountain',
               186: 'Oak Trees',
               187: 'Outcropping',
               188: 'Pine Trees',
               189: 'Plant',
               190: 'River Delta',
               191: 'Rock',
               192: 'Sand Dune',
               193: 'Sand Pit',
               194: 'Shrub',
               195: 'Skull',
               196: 'Stalagmite',
               197: 'Stump',
               198: 'Tar Pit',
               199: 'Trees',
               200: 'Vine',
               201: 'Volcanic Vent',
               202: 'Volcano',
               203: 'Willow Trees',
               204: 'Yucca Trees',
               205: 'Reef',
               206: 'Desert Hills',
               207: 'Dirt Hills',
               208: 'Grass Hills',
               209: 'Rough Hills',
               210: 'Subterranean Rocks',
               211: 'Swamp Foliage',
               212: 'Border Gate',
               213: 'Freelancers Guild',
               214: 'Hero Placeholder',
               215: 'Quest Guard',
               216: 'Random Dwelling',
               217: 'Random dwelling with no home castle type',
               218: 'Random dwelling with home castle type',
               219: 'Garrison',
               220: 'Abandoned Mine',
               221: 'Trading Post',
               222: 'Clover Field',
               223: 'Cursed Ground',
               224: 'Evil Fog',
               225: 'Favourable Winds',
               226: 'Fiery Fields',
               227: 'Holy Ground',
               228: 'Lucid Pools',
               229: 'Magic Clouds',
               230: 'Magic Plains',
               231: 'Rocklands'}

    Mines = {0: 'Sawmill',
             1: 'Alchemists Lab',
             2: 'Ore Pit',
             3: 'Sulfur Dune',
             4: 'Crystal Cavern',
             5: 'Gem Pond',
             6: 'Gold Mine',
             7: 'Abandoned Mine'}

    Resources = {0: 'Wood',
                 1: 'Mercury',
                 2: 'Ore',
                 3: 'Sulfur',
                 4: 'Crystal',
                 5: 'Gems',
                 6: 'Gold',
                 253: 'Wood and Ore',
                 254: 'Mercury, Sulfur, Crystal and Gems'}

    Artifacts = {0: 'Spell book',
                 1: 'Spell Scroll',
                 2: 'Grail',
                 3: 'Catapult',
                 4: 'Ballista',
                 5: 'Ammo Cart',
                 6: 'First Aid Tent',
                 7: 'Centaur Axe',
                 8: 'Blackshard of the Dead Knight',
                 9: 'Greater Gnoll\'s Flail',
                 10: 'Ogre\'s Club of Havoc',
                 11: 'Sword of Hellfire',
                 12: 'Titan\'s Gladius',
                 13: 'Shield of the Dwarven Lords',
                 14: 'Shield of the Yawning Dead',
                 15: 'Buckler of the Gnoll King',
                 16: 'Targ of the Rampaging Ogre',
                 17: 'Shield of the Damned',
                 18: 'Sentinel\'s Shield',
                 19: 'Helm of the Alabaster Unicorn',
                 20: 'Skull Helmet',
                 21: 'Helm of Chaos',
                 22: 'Crown of the Supreme Magi',
                 23: 'Hellstorm Helmet',
                 24: 'Thunder Helmet',
                 25: 'Breastplate of Petrified Wood',
                 26: 'Rib Cage',
                 27: 'Scales of the Greater Basilisk',
                 28: 'Tunic of the Cyclops King',
                 29: 'Breastplate of Brimstone',
                 30: 'Titan\'s Cuirass',
                 31: 'Armor of Wonder',
                 32: 'Sandals of the Saint',
                 33: 'Celestial Necklace of Bliss',
                 34: 'Lion\'s Shield of Courage',
                 35: 'Sword of Judgement',
                 36: 'Helm of Heavenly Enlightenment',
                 37: 'Quiet Eye of the Dragon',
                 38: 'Red Dragon Flame Tongue',
                 39: 'Dragon Scale Shield',
                 40: 'Dragon Scale Armor',
                 41: 'Dragonbone Greaves',
                 42: 'Dragon Wing Tabard',
                 43: 'Necklace of Dragonteeth',
                 44: 'Crown of Dragontooth',
                 45: 'Still Eye of the Dragon',
                 46: 'Clover of Fortune',
                 47: 'Cards of Prophecy',
                 48: 'Ladybird of Luck',
                 49: 'Badge of Courage',
                 50: 'Crest of Valor',
                 51: 'Glyph of Gallantry',
                 52: 'Speculum',
                 53: 'Spyglass',
                 54: 'Amulet of the Undertaker',
                 55: 'Vampire\'s Cowl',
                 56: 'Dead Man\'s Boots',
                 57: 'Garniture of Interference',
                 58: 'Surcoat of Counterpoise',
                 59: 'Boots of Polarity',
                 60: 'Bow of Elven Cherrywood',
                 61: 'Bowstring of the Unicorn\'s Mane',
                 62: 'Angel Feather Arrows',
                 63: 'Bird of Perception',
                 64: 'Stoic Watchman',
                 65: 'Emblem of Cognizance',
                 66: 'Statesman\'s Medal',
                 67: 'Diplomat\'s Ring',
                 68: 'Ambassador\'s Sash',
                 69: 'Ring of the Wayfarer',
                 70: 'Equestrian\'s Gloves',
                 71: 'Necklace of Ocean Guidance',
                 72: 'Angel Wings',
                 73: 'Charm of Mana',
                 74: 'Talisman of Mana',
                 75: 'Mystic Orb of Mana',
                 76: 'Collar of Conjuring',
                 77: 'Ring of Conjuring',
                 78: 'Cape of Conjuring',
                 79: 'Orb of the Firmament',
                 80: 'Orb of Silt',
                 81: 'Orb of Tempestuous Fire',
                 82: 'Orb of Driving Rain',
                 83: 'Recanter\'s Cloak',
                 84: 'Spirit of Oppression',
                 85: 'Hourglass of the Evil Hour',
                 86: 'Tome of Fire Magic',
                 87: 'Tome of Air Magic',
                 88: 'Tome of Water Magic',
                 89: 'Tome of Earth Magic',
                 90: 'Boots of Levitation',
                 91: 'Golden Bow',
                 92: 'Sphere of Permanence',
                 93: 'Orb of Vulnerability',
                 94: 'Ring of Vitality',
                 95: 'Ring of Life',
                 96: 'Vial of Lifeblood',
                 97: 'Necklace of Swiftness',
                 98: 'Boots of Speed',
                 99: 'Cape of Velocity',
                 100: 'Pendant of Dispassion',
                 101: 'Pendant of Second Sight',
                 102: 'Pendant of Holiness',
                 103: 'Pendant of Life',
                 104: 'Pendant of Death',
                 105: 'Pendant of Free Will',
                 106: 'Pendant of Negativity',
                 107: 'Pendant of Total Recall',
                 108: 'Pendant of Courage',
                 109: 'Everflowing Crystal Cloak',
                 110: 'Ring of Infinite Gems',
                 111: 'Everpouring Vial of Mercury',
                 112: 'Inexhaustible Cart of Ore',
                 113: 'Eversmoking Ring of Sulfur',
                 114: 'Inexhaustible Cart of Lumber',
                 115: 'Endless Sack of Gold',
                 116: 'Endless Bag of Gold',
                 117: 'Endless Purse of Gold',
                 118: 'Legs of Legion',
                 119: 'Loins of Legion',
                 120: 'Torso of Legion',
                 121: 'Arms of Legion',
                 122: 'Head of Legion',
                 123: 'Sea Captain\'s Hat',
                 124: 'Spellbinder\'s Hat',
                 125: 'Shackles of War',
                 126: 'Orb of Inhibition',
                 127: 'Vial of Dragon Blood',
                 128: 'Armageddon\'s Blade',
                 129: 'Angelic Alliance',
                 130: 'Cloak of the Undead King',
                 131: 'Elixir of Life',
                 132: 'Armor of the Damned',
                 133: 'Statue of Legion',
                 134: 'Power of the Dragon Father',
                 135: 'Titan\'s Thunder',
                 136: 'Admiral\'s Hat',
                 137: 'Bow of the Sharpshooter',
                 138: 'Wizard\'s Well',
                 139: 'Ring of the Magi',
                 140: 'Cornucopia',
                 # WOG
                 141: 'Magic Wand *',
                 142: 'Gold Tower Arrow *',
                 143: 'Monster\'s Power *',
                 144: 'Highlighted Slot **',
                 145: 'Artifact Lock **',
                 146: 'Axe of Smashing ***',
                 147: 'Mithril Mail ***',
                 148: 'Sword of Sharpness ***',
                 149: 'Helm of Immortality ***',
                 150: 'Pendant of Sorcery ***',
                 151: 'Boots of Haste ***',
                 152: 'Bow of Seeking ***',
                 153: 'Dragon Eye Ring ***',
                 154: 'Hardened Shield ***',
                 155: 'Slava\'s Ring of Power ***',
                 156: 'Warlord\'s banner *',
                 157: 'Crimson Shield of Retribution *',
                 158: 'Barbarian Lord\'s Axe of Ferocity *',
                 159: 'Dragonheart *',
                 160: 'Gate Key *',
                 161: 'Blank Helmet ****',
                 162: 'Blank Sword ****',
                 163: 'Blank Shield ****',
                 164: 'Blank Horned Ring ****',
                 165: 'Blank Gemmed Ring ****',
                 166: 'Blank Neck Broach ****',
                 167: 'Blank Armor ****',
                 168: 'Blank Surcoat ****',
                 169: 'Blank Boots ****',
                 170: 'Blank Horn ****'}

    HeroClass = {0: 'Knight',
                 1: 'Knight',
                 2: 'Cleric',
                 3: 'Ranger',
                 4: 'Druid',
                 5: 'Alchemist',
                 6: 'Wizard',
                 7: 'Demoniac',
                 8: 'Heretic',
                 9: 'Death Knight',
                 10: 'Necromancer',
                 11: 'Overlord',
                 12: 'Warlock',
                 13: 'Barbarian',
                 14: 'Battle Mage',
                 15: 'Beastmaster',
                 16: 'Witch',
                 17: 'PlanesWalker',
                 18: 'Elementalist',
                 19: 'additional heroes 2',
                 20: 'additional heroes 1',
                 21: 'Captain',
                 22: 'Navigator',
                 31: 'HOTA extra'}

    Heroes = {
              # Knights
              0: 'Orrin',
              1: 'Valeska',
              2: 'Edric',
              3: 'Sylvia',
              4: 'Lord Haart',
              5: 'Sorsha',
              6: 'Christian',
              7: 'Tyris',
              #  Clerics
              8: 'Rion',
              9: 'Adela',
              10: 'Cuthbert',
              11: 'Adelaide',
              12: 'Ingham',
              13: 'Sanya',
              14: 'Loynis',
              15: 'Caitlin',
              #  Rangers
              16: 'Mephala',
              17: 'Ufretin',
              18: 'Jenova',
              19: 'Ryland',
              20: 'Thorgrim',
              21: 'Ivor',
              22: 'Clancy',
              23: 'Kyrre',
              #  Druids
              24: 'Coronius',
              25: 'Uland',
              26: 'Elleshar',
              27: 'Gem',
              28: 'Malcom',
              29: 'Melodia',
              30: 'Alagar',
              31: 'Aeris',
              #  Alchemists
              32: 'Piquedram',
              33: 'Thane',
              34: 'Josephine',
              35: 'Neela',
              36: 'Torosar',
              37: 'Fafner',
              38: 'Rissa',
              39: 'Iona',
              #  Wizards
              40: 'Astral',
              41: 'Halon',
              42: 'Serena',
              43: 'Daremyth',
              44: 'Theodorus',
              45: 'Solmyr',
              46: 'Cyra',
              47: 'Aine',
              #  Draoniacs
              48: 'Fiona',
              49: 'Rashka',
              50: 'Marius',
              51: 'Ignatius',
              52: 'Octavia',
              53: 'Calh',
              54: 'Pyre',
              55: 'Nymus',
              #  Heretics
              56: 'Ayden',
              57: 'Xyron',
              58: 'Axsis',
              59: 'Olema',
              60: 'Calid',
              61: 'Ash',
              62: 'Zydar',
              63: 'Xarfax',
              #  Death Knights
              64: 'Straker',
              65: 'Vokial',
              66: 'Moandor',
              67: 'Charna',
              68: 'Tamika',
              69: 'Isra',
              70: 'Clavius',
              71: 'Galthran',
              #  Necromancers
              72: 'Septienna',
              73: 'Aislinn',
              74: 'Sandro',
              75: 'Nimbus',
              76: 'Thant',
              77: 'Xsi',
              78: 'Vidomina',
              79: 'Nagash',
              #  Overlords
              80: 'Lorelei',
              81: 'Arlach',
              82: 'Dace',
              83: 'Ajit',
              84: 'Damacon',
              85: 'Gunnar',
              86: 'Synca',
              87: 'Shakti',
              #  Warlocks
              88: 'Alamar',
              89: 'Jaegar',
              90: 'Malekith',
              91: 'Jeddite',
              92: 'Geon',
              93: 'Deemer',
              94: 'Sephinroth',
              95: 'Darkstorn',
              #  Barbarians
              96: 'Yog',
              97: 'Gurnisson',
              98: 'Jabarkas',
              99: 'Shiva',
              100: 'Gretchin',
              101: 'Krellion',
              102: 'Crag Hack',
              103: 'Tyraxor',
              #  Battle Mages
              104: 'Gird',
              105: 'Vey',
              106: 'Dessa',
              107: 'Terek',
              108: 'Zubin',
              109: 'Gundula',
              110: 'Oris',
              111: 'Saurug',
              #  Beastmasters
              112: 'Bron',
              113: 'Drakon',
              114: 'Wystan',
              115: 'Tazar',
              116: 'Alkin',
              117: 'Korbac',
              118: 'Gerwulf',
              119: 'Broghild',
              #  Witches
              120: 'Mirlanda',
              121: 'Rosic',
              122: 'Voy',
              123: 'Verdish',
              124: 'Merist',
              125: 'Styg',
              126: 'Andra',
              127: 'Tiva',
              #  Planeswalkers
              128: 'Pasis',
              129: 'Thunar',
              130: 'Ignissa',
              131: 'Lacus',
              132: 'Monere',
              133: 'Erdamon',
              134: 'Fiur',
              135: 'Kalt',
              #  Elementalists
              136: 'Luna',
              137: 'Brissa',
              138: 'Ciele',
              139: 'Labetha',
              140: 'Inteus',
              141: 'Aenain',
              142: 'Gelare',
              143: 'Grindan',
              #  Extension Heroes
              144: 'Sir Mullich',
              145: 'Adrienne',
              146: 'Catherine',
              147: 'Dracon',
              148: 'Gelu',
              149: 'Kilgor',
              150: 'Lord Haart',
              151: 'Mutare',
              152: 'Roland',
              153: 'Mutare Drake',
              154: 'Boragus',
              155: 'Xeron',
              #  HOTA
              156: 'Corkes',
              157: 'Jeremy',
              158: 'Illor',
              159: 'Derek',
              160: 'Leena',
              161: 'Anabel',
              162: 'Cassiopeia',
              163: 'Miriam',
              164: 'Bidley',
              165: 'Tark',
              166: 'Elmore',
              167: 'Casmetra',
              168: 'Manfred',
              169: 'Spint',
              170: 'Andal',
              171: 'Dargem',
              172: 'Zilare',
              173: 'Astra',
              174: 'Eovacius',
              175: 'Beatrice',
              176: 'Kinkeria',
              177: 'Ranloo',
              255: 'Random',
              65533: 'Most powerful hero'}

    Buildings = {0: 'Town hall',
                 1: 'City hall',
                 2: 'Capitol',
                 3: 'Fort',
                 4: 'Citadel',
                 5: 'Castle',
                 6: 'Tavern',
                 7: 'Blacksmith',
                 8: 'Marketplace',
                 9: 'Resource silo',

                 11:  'Mages guild 1',
                 12:  'Mages guild 2',
                 13:  'Mages guild 3',
                 14:  'Mages guild 4',
                 15:  'Mages guild 5',
                 16:  'Shipyard',
                 17:  'Grail',
                 18:  'Special 1',
                 19:  'Special 2',  # ?
                 20:  'Special 3',
                 21:  'Special 4',
                 22:  'Dwelling lvl 1',
                 23:  'Dwelling lvl 1 upg',
                 24:  'Horde lvl 1',
                 25:  'Dwelling lvl 2',
                 26:  'Dwelling lvl 2 upg',
                 27:  'Horde lvl 2',
                 28:  'Dwelling lvl 3',
                 29:  'Dwelling lvl 3 upg',
                 30:  'Horde lvl 3',
                 31:  'Dwelling lvl 4',
                 32:  'Dwelling lvl 4 upg',
                 33:  'Horde lvl 4',
                 34:  'Dwelling lvl 5',
                 35:  'Dwelling lvl 5 upg',
                 36:  'Horde lvl 5',
                 37:  'Dwelling lvl 6',
                 38:  'Dwelling lvl 6 upg',
                 39:  'Dwelling lvl 7',
                 40:  'Dwelling lvl 7 upg'}

    Experience = {1: 0,
                  2: 1000,
                  3: 2000,
                  4: 3200,
                  5: 4600,
                  6: 6200,
                  7: 8000,
                  8: 10000,
                  9: 12200,
                  10:  14700,
                  11:  17500,
                  12:  20600,
                  13:  24320,
                  14:  28784,
                  15:  34140,
                  16:  40567,
                  17:  48279,
                  18:  57533,
                  19:  68637,
                  20:  81961,
                  21:  97949,
                  22:  117134,
                  23:  140156,
                  24:  167782,
                  25:  200933,
                  26:  240714,
                  27:  288451,
                  28:  345735,
                  29:  414475,
                  30:  496963,
                  31:  595948,
                  32:  714730,
                  33:  857268,
                  34:  1028313,
                  35:  1233567,
                  36:  1479871,
                  37:  1775435,
                  38:  2130111,
                  39:  2555722,
                  40:  3066455,
                  41:  3679334,
                  42:  4414788,
                  43:  5297332,
                  44:  6356384,
                  45:  7627246,
                  46:  9152280,
                  47:  10982320,
                  48:  13178368,
                  49:  15813625,
                  50:  18975933,
                  51:  22770702,
                  52:  27324424,
                  53:  32788890,
                  54:  39346249,
                  55:  47215079,
                  56:  56657675,
                  57:  67988790,
                  58:  81586128,
                  59:  97902933,
                  60:  117483099,
                  61:  140979298,
                  62:  169174736,
                  63:  203009261,
                  64:  243610691,
                  65:  292332407,
                  66:  350798466,
                  67:  420957736,
                  68:  505148860,
                  69:  606178208,
                  70:  727413425,
                  71:  872895685,
                  72:  1047474397,
                  73:  1256968851,
                  74:  1508362195,
                  75:  1810034207,
                  76:  0x100000000}

    ObjectColors = {0: 'Blue',
                    1: 'Green',
                    2: 'Red',
                    3: 'Dark Blue',
                    4: 'Tan',
                    5: 'Purple',
                    6: 'White',
                    7: 'Black'}

    BlockMapBits = {BlockMapBits.VISIBLE: 'Visible',
                    BlockMapBits.VISITABLE: 'Visitable',
                    BlockMapBits.BLOCKED: 'Blocked',
                    BlockMapBits.COMBINED: 'Combined'}

    RewardType = {RewardType.NOTHING: 'Nothing',
                  RewardType.EXPERIENCE: 'Experience',
                  RewardType.MANA_POINTS: 'Mana points',
                  RewardType.MORALE_BONUS: 'Morale bonus',
                  RewardType.LUCK_BONUS: 'Luck bonus',
                  RewardType.RESOURCES: 'Resources',
                  RewardType.PRIMARY_SKILL: 'Primary skill',
                  RewardType.SECONDARY_SKILL: 'Secondary skill',
                  RewardType.ARTIFACT: 'Artifact',
                  RewardType.SPELL: 'Spell',
                  RewardType.CREATURE: 'Creature'}

    QuestMission = {QuestMission.NONE: 'None',
                    QuestMission.LEVEL: 'Level',
                    QuestMission.PRIMARY_STAT: 'Primary stat',
                    QuestMission.KILL_HERO: 'Kill hero',
                    QuestMission.KILL_CREATURE: 'Kill creature',
                    QuestMission.ART: 'Artifact',
                    QuestMission.ARMY: 'Army',
                    QuestMission.RESOURCES: 'Resources',
                    QuestMission.HERO: 'Hero',
                    QuestMission.PLAYER: 'Player',
                    QuestMission.KEYMASTER: 'Keymaster'}

    Victory = {Victory.NONE: 'Default',
               Victory.ARTIFACT: 'Acquire a specific artifact',
               Victory.ACCUMULATE_CREATURES: 'Accumulate creatures',
               Victory.ACCUMULATE_RESOURCES: 'Accumulate resources',
               Victory.UPGRADE_TOWN: 'Upgrade a specific town',
               Victory.BUILD_GRAIL: 'Build the grail',
               Victory.DEFEAT_HERO: 'Defeat a specific hero',
               Victory.CAPTURE_TOWN: 'Capture a specific town',
               Victory.KILL_MONSTER: 'Defeat a specific monster',
               Victory.FLAG_DWELLINGS: 'Flag all creature dwellings',
               Victory.FLAG_MINES: 'Flag all mines',
               Victory.TRANSPORT_ARTIFACT: 'Transport a specific artifact',
               Victory.ELIMINATE_MONSTERS: 'Eliminate all monsters',
               Victory.SURVIVE_TIME: 'Survive for certain time'}

    Loss = {Loss.NONE: 'None',
            Loss.TOWN: 'Lose a specific town',
            Loss.HERO: 'Lose a specific hero',
            Loss.TIME: 'Time'}
