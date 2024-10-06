"""Script containing Hero class and other classes associated with Hero.
   Also, all the objects representing secondary skills"""
from colorama import Fore

from data.creature import Creature
from data.magic import Spells
import numpy as np
from image_processing.detecting_window import execute_detecting
import GUI_handling
import time


class Slot:
    def __init__(self, unit: Creature = Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False,"None", ("", "")), amount: int = 0):
        """
        Class representing a single slot

        :param unit: Creature object
        :param amount: (int) amount of the creature
        """
        self.name = "Slot"
        self.unit = unit
        self.amount = amount
        self.number = amount

    def end_day(self, player):
        """
        End day buffer function

        :param player: player object
        """
        pass

    def end_week(self, player):
        """
        End week function that calculates again the number of creatures.

        :param player: player object
        """
        # units on map are growing by 10% each week rounded down but
        # real value of growth is stored and used in later weeks
        self.number = self.number * 1.1
        self.amount = int(np.floor(self.number))

    def action(self, player, hero, okey):
        """
        Action method that leads to the execution of the whole program

        :param player: Player object
        :param hero: Hero object
        :param okey: okay parameter - associated with window handling
        """
        execute_detecting(hero)


class Slots:
    def __init__(self, s1: Slot = Slot(), s2: Slot = Slot(), s3: Slot = Slot(), s4: Slot = Slot(), s5: Slot = Slot(),
                 s6: Slot = Slot(), s7: Slot = Slot()):
        """
        Class representing slots.

        :param s1: Unit in slot 1
        :param s2: Unit in slot 2
        :param s3: Unit in slot 3
        :param s4: Unit in slot 4
        :param s5: Unit in slot 5
        :param s6: Unit in slot 6
        :param s7: Unit in slot 7
        """
        self.slots = [s1, s2, s3, s4, s5, s6, s7]

    def check_units(self):
        suma = 0
        for s in self.slots:
            if s.unit.name != "":
                suma +=1
        return suma


class SecondarySkill:
    def __init__(self, lvl: int = 0, name: str = '', value: int = 0):
        """
        Secondary skill of our hero

        :param lvl: Level of the skill
        :param name: Name of the skill
        :param value: Value of the skill
        """
        self.lvl = lvl
        self.name = name
        self.value = value


class SecondarySkills:
    def __init__(self, s1: SecondarySkill = SecondarySkill(), s2: SecondarySkill = SecondarySkill(),
                 s3: SecondarySkill = SecondarySkill(),
                 s4: SecondarySkill = SecondarySkill(), s5: SecondarySkill = SecondarySkill(),
                 s6: SecondarySkill = SecondarySkill(),
                 s7: SecondarySkill = SecondarySkill(), s8: SecondarySkill = SecondarySkill()):
        """
        Class representing all the secondary skills of our hero.

        :param s1: Secondary skill 1
        :param s2: Secondary skill 2
        :param s3: Secondary skill 3
        :param s4: Secondary skill 4
        :param s5: Secondary skill 5
        :param s6: Secondary skill 6
        :param s7: Secondary skill 7
        :param s8: Secondary skill 8
        """
        self.secondary_skills = [s1, s2, s3, s4, s5, s6, s7, s8]


class Hero:
    def __init__(self, lvl: int, herotype: str, name: str, atc: int, defense: int, spellpower: int, knowledge: int,
                 slots: Slots = Slots(), spells: Spells = Spells(), skills: SecondarySkills = SecondarySkills(),
                 ally=True, heroclass: str = 'might'):
        """
        Class representing player's hero.

        :param lvl: Level of the hero
        :param herotype: Type of the hero
        :param name: Name of the hero
        :param atc: Attack parameter
        :param defense: Defense parameter
        :param spellpower: Spell power parameter
        :param knowledge: Knowledge parameter
        :param slots: Slots parameter representing an army of the hero
        :param spells: Spells of the hero
        :param skills: Skills of the hero
        :param ally: Boolean determining whether hero's an ally or not
        :param heroclass: Class of the hero
        """
        self.lvl = lvl
        self.herotype = herotype
        self.name = name
        self.attack = atc
        self.defense = defense
        self.spellpower = spellpower
        self.knowledge = knowledge
        self.slots = slots
        self.spellbook = spells
        self.morale = 0
        self.luck = 0
        self.speciality = ''
        self.skills = skills
        self.mspoints = 1900
        self.ally = ally
        self.position = (0, 0)
        self.heroclass = heroclass
        self.manapoint = 10 * self.knowledge
        self.value_map = np.zeros((72, 72))
        self.temp_value_map = np.zeros((72, 72))
        self.artifacts = {'Cape': [''], 'Feet': [''], 'Helm': [''], 'Shield': [''], 'Misc': ['', '', '', '', ''],
                          'Necklace': [''], 'Weapon': [''], 'Ring': ['', ''], 'Torso': [''], 'Backpack': []}
# TODO add artifact list

    def action(self,player,hero, okvalue):
        """
        Action function associated with handling fighting enemy hero window

        :param player: player object
        :param hero: hero object
        """
        time.sleep(0.1)
        execute_detecting(hero)
        time.sleep(0.1)

    def __str__(self):
        h1 = f"{Fore.CYAN}################### [CURRENT HERO] ###########################\n"
        header = f"| [LVL]: {self.lvl} | [NAME]: {self.name} | [TYPE]: {self.herotype}{Fore.RESET}\n"
        p = f"[POSITION]: {self.position} | [MS POINTS]:{self.mspoints} | [MANA]: {self.manapoint}\n"
        txt = h1 + header + p
        try:
            for slot in self.slots.slots:
                unit_txt = f"| [NAME]:{Fore.GREEN}{slot.unit.name}{Fore.RESET} | [AMOUNT]: {slot.amount} | [LVL]: {slot.unit.lvl}\n"
                txt = txt + unit_txt
        except AttributeError:
            print("XDDDDDDDDDDDDDDDDDDDD")
            for slot in self.slots.slots:
                print(type(slot.unit))

        txt = txt + f"{Fore.CYAN}################### [CURRENT HERO END] ###########################\n"
        return txt


def choose_attack_or_defence(hero: Hero):
    """
    Function determining whether to choose attack of defense parameter

    :param hero: Hero object
    :return: "attack" or "defense" (str)
    """
    if hero.attack < hero.defense:
        return "attack"
    else:
        return "defence"


# def choose_better_skill(hero: Hero, skills: list[SecondarySkill]):
#     """
#     Function determining what secondary skill to choose.
#
#     :param hero: Hero object
#     :param skills: List of secondary skills
#     :return: skill 1 or skill2 (Skills pop up in the lvl up window)
#     """
#     skill1 = skills[0]
#     skill2 = skills[1]
#     herotype = hero.herotype
#     if herotype == 'main':
#         goodness_of_skill1 = main_hero_skills.index(skill1)
#         goodness_of_skill2 = main_hero_skills.index(skill2)
#     else:
#         goodness_of_skill1 = picker_hero_skills.index(skill1)
#         goodness_of_skill2 = picker_hero_skills.index(skill2)
#
#     if goodness_of_skill1 < goodness_of_skill2:
#         return skill1
#     else:
#         return skill2


Air_Magic = SecondarySkill(0, "Air_Magic", 5)
Archery = SecondarySkill(0, "Archery", 4)
Armorer = SecondarySkill(0, "Armorer", 5)
Artillery = SecondarySkill(0, "Artillery", 1)
Ballistics = SecondarySkill(0, "Ballistics", 1)
Diplomacy = SecondarySkill(0, "Diplomacy", 4)
Eagle_Eye = SecondarySkill(0, "Eagle_Eye", 0)
Earth_Magic = SecondarySkill(0, "Earth_Magic", 5)
Estates = SecondarySkill(0, "Estates", 5)
Fire_Magic = SecondarySkill(0, "Fire_Magic", 4)
First_Aid = SecondarySkill(0, "First_Aid", 0)
Intelligence = SecondarySkill(0, "Intelligence", 3)
Leadership = SecondarySkill(0, "Leadership", 3)
Learning = SecondarySkill(0, "Learning", 0)
Logistics = SecondarySkill(0, "Logistics", 5)
Luck = SecondarySkill(0, "Luck", 2)
Mysticism = SecondarySkill(0, "Mysticism", 2)
Navigation = SecondarySkill(0, "Navigation", 3)
Necromancy = SecondarySkill(0, "Necromancy", 5)
Offense = SecondarySkill(0, "Offense", 5)
Pathfinding = SecondarySkill(0, "Pathfinding", 3)
Resistance = SecondarySkill(0, "Resistance", 3)
Scholar = SecondarySkill(0, "Scholar", 3)
Scouting = SecondarySkill(0, "Scouting", 4)
Sorcery = SecondarySkill(0, "Sorcery", 2)
Tactics = SecondarySkill(0, "Tactics", 3)
Water_Magic = SecondarySkill(0, "Water_Magic", 4)
Wisdom = SecondarySkill(0, "Wisdom", 4)
Interference = SecondarySkill(0, "Interference", 3)

main_hero_skills = [Logistics, Earth_Magic, Air_Magic, Armorer, Necromancy, Offense, Archery,
                    Water_Magic, Diplomacy, Estates, Fire_Magic, Scouting, Wisdom, Intelligence, Leadership, Navigation,
                    Pathfinding, Resistance, Scholar, Tactics, Interference, Luck, Mysticism, Sorcery, Artillery,
                    Ballistics, Eagle_Eye, First_Aid, Learning]

picker_hero_skills = [Logistics, Estates, Scouting, Navigation, Pathfinding, Earth_Magic, Air_Magic, Armorer,
                      Necromancy, Offense, Archery, Water_Magic, Diplomacy, Fire_Magic, Wisdom, Intelligence,
                      Leadership, Resistance, Scholar, Tactics, Interference, Luck, Mysticism, Sorcery, Artillery,
                      Ballistics, Eagle_Eye, First_Aid, Learning]

# Dictionary listing hero:
# str(name): tuple(str(Speciality), str(Skill 1), str(Skill 2), str(Starting Spell), int(starting movement points))
# Units have added 's' at the end, all but (Pegasus - Pegasi, Mage - Magi,)

hero_dict = {'Anabel': ('Captain', 'Pirates', 'Basic Offense', 'Basic Archery', '', 1700),
             'Cassiopeia': ('Captain', 'Nymphs', 'Basic Offense', 'Basic Tactics', '', 1760),
             'Corkes': ('Captain', 'Offense', 'Basic Offense', 'Basic Pathfinding', '', 1630),
             'Derek': ('Captain', 'Crew Mates', 'Basic Offense', 'Basic Leadership', '', 1700),
             'Elmore': ('Captain', 'Navigation', 'Advanced Navigation', '', '', 1630),
             'Illor': ('Captain', 'Storm Birds', 'Basic Armorer', 'Basic Tactics', '', 1700),
             'Jeremy': ('Captain', 'Cannon', 'Basic Offense', 'Basic Artillery', '', 1700),
             'Leena': ('Captain', 'Gold', 'Basic Pathfinding', 'Basic Estates', '', 1630),
             'Miriam': ('Captain', 'Scouting', 'Basic Logistics', 'Basic Scouting', '', 1711),
             'Bidley': ('Captain', 'Sea Dogs', 'Advanced Offense', '', '', 1760),
             'Tark': ('Captain', 'Nix', 'Basic Offense', 'Basic Armorer', '', 1760),

             'Andal': ('Navigator', 'Crystal', 'Basic Wisdom', 'Basic Pathfinding', 'Slow', 1630),
             'Astra': ('Navigator', 'Cure', 'Basic Wisdom', 'Basic Luck', 'Cure', 1630),
             'Casmetra': ('Navigator', 'Sea Witches', 'Basic Wisdom', 'Basic Water Magic', 'Dispel', 1630),
             'Dargem': ('Navigator', 'Air Shield', 'Basic Wisdom', 'Basic Tactics', 'Air Shield', 1630),
             'Eovacius': ('Navigator', 'Clone', 'Basic Wisdom', 'Basic Intelligence', 'Clone', 1630),
             'Manfred': ('Navigator', 'Fireball', 'Basic Wisdom', 'Basic Fire Magic', 'Fireball', 1630),
             'Spint': ('Navigator', 'Sorcery', 'Basic Wisdom', 'Basic Sorcery', 'Bless', 1630),
             'Zilare': ('Navigator', 'Forgetfulness', 'Basic Wisdom', 'Basic Interference', 'Forgetfulness', 1630),

             'Christian': ('Knight', 'Ballista', 'Basic Leadership', 'Basic Artillery', '', 1560),
             'Edric': ('Knight', 'Griffins', 'Basic Leadership', 'Basic Armorer', '', 1560),
             'Orrin': ('Knight', 'Archery', 'Basic Leadership', 'Basic Archery', '', 1560),
             'Sorsha': ('Knight', 'Swordsman', 'Basic Leadership', 'Basic Offense', '', 1560),
             'Sylvia': ('Knight', 'Navigation', 'Basic Leadership', 'Basic Navigation', '', 1560),
             'Valeska': ('Knight', 'Archers', 'Basic Leadership', 'Basic Archery', '', 1630),
             'Tyris': ('Knight', 'Cavaliers', 'Basic Leadership', 'Basic Tactics', '', 1560),
             'Lord Haart': ('Knight', 'Estates', 'Basic Leadership', 'Basic Estates', '', 1560),
             'Catherine': ('Knight', 'Swordsman', 'Basic Leadership', 'Basic Offense', '', 1560),
             'Roland': ('Knight', 'Swordsman', 'Basic Leadership', 'Basic Armorer', '', 1560),
             'Sir Mullich': ('Knight', 'Speed', 'Advanced Logistics', '', '', 1560),
             'Beatrice': ('Knight', 'Scouting', 'Basic Leadership', 'Basic Scouting', '', 1560),

             'Adela': ('Cleric', 'Bless', 'Basic Wisdom', 'Basic Diplomacy', 'Bless', 1560),
             'Adelaide': ('Cleric', 'Frost Ring', 'Advanced Wisdom', '', 'Frost Ring', 1560),
             'Caitlin': ('Cleric', 'Gold', 'Basic Wisdom', 'Basic Intelligence', 'Cure', 1560),
             'Cuthbert': ('Cleric', 'Weakness', 'Basic Wisdom', 'Basic Estates', 'Weakness', 1560),
             'Ingham': ('Cleric', 'Monks', 'Basic Wisdom', 'Basic Mysticism', 'Curse', 1560),
             'Loynis': ('Cleric', 'Prayer', 'Basic Wisdom', 'Basic Learning', 'Prayer', 1560),
             'Rion': ('Cleric', 'First Aid', 'Basic Wisdom', 'Basic First Aid', 'Stone Skin', 1560),
             'Sanya': ('Cleric', 'Eagle Eye', 'Basic Wisdom', 'Basic Eagle Eye', 'Dispel', 1560),

             'Clancy': ('Ranger', 'Unicorns', 'Basic Interference', 'Basic Pathfinding', '', 1500),
             'Ivor': ('Ranger', 'Elves', 'Basic Archery', 'Basic Offense', '', 1700),
             'Jenova': ('Ranger', 'Gold', 'Advanced Archery', '', '', 1500),
             'Kyrre': ('Ranger', 'Logistics', 'Basic Archery', 'Basic Logistics', '', 1578),
             'Mephala': ('Ranger', 'Armorer', 'Basic Leadership', 'Basic Armorer', '', 1500),
             'Ryland': ('Ranger', 'Dendroids', 'Basic Leadership', 'Basic Diplomacy', '', 1500),
             'Thorgrim': ('Ranger', 'Resistance', 'Advanced Resistance', '', '', 1500),
             'Ufretin': ('Ranger', 'Dwarves', 'Basic Interference', 'Basic Luck', '', 1560),
             'Gelu': ('Ranger', 'Sharpshooters', 'Basic Leadership', 'Basic Archery', '', 1900),
             'Giselle': ('Ranger', 'Interference', 'Advanced Interference', '', '', 1500),

             'Aeris': ('Druid', 'Pegasi', 'Basic Wisdom', 'Basic Scouting', 'Protection from Air', 1500),
             'Alagar': ('Druid', 'Ice Bolt', 'Basic Wisdom', 'Basic Sorcery', 'Ice Bolt', 1500),
             'Coronius': ('Druid', 'Slayer', 'Basic Wisdom', 'Basic Scholar', 'Slayer', 1500),
             'Elleshar': ('Druid', 'Intelligence', 'Basic Wisdom', 'Basic Intelligence', 'Curse', 1500),
             # On a map without water Gem's starting spell is Bless
             'Gem': ('Druid', 'First Aid', 'Basic Wisdom', 'Basic First Aid', 'Summon Boat', 1700),
             'Malcom': ('Druid', 'Eagle Eye', 'Basic Wisdom', 'Basic Eagle Eye', 'Magic Arrow', 1500),
             'Melodia': ('Druid', 'Fortune', 'Basic Wisdom', 'Basic Luck', 'Fortune', 1500),
             'Uland': ('Druid', 'Cure', 'Advanced Wisdom', 'Basic Ballistics', 'Cure', 1500),

             'Fafner': ('Alchemist', 'Nagas', 'Basic Scholar', 'Basic Interference', 'Haste', 1500),
             'Iona': ('Alchemist', 'Genies', 'Basic Scholar', 'Basic Intelligence', 'Magic Arrow', 1500),
             'Josephine': ('Alchemist', 'Golems', 'Basic Mysticism', 'Basic Sorcery', 'Haste', 1560),
             'Neela': ('Alchemist', 'Armorer', 'Basic Scholar', 'Basic Armorer', 'Shield', 1500),
             'Piquedram': ('Alchemist', 'Gargoyles', 'Basic Mysticism', 'Basic Scouting', 'Shield', 1760),
             'Rissa': ('Alchemist', 'Mercury', 'Basic Mysticism', 'Basic Offense', 'Magic Arrow', 1500),
             'Thane': ('Alchemist', 'Genies', 'Advanced Scholar', '', 'Magic Arrow', 1500),
             'Torosar': ('Alchemist', 'Ballista', 'Basic Mysticism', 'Basic Tactics', 'Magic Arrow', 1500),

             'Aine': ('Wizard', 'Gold', 'Basic Wisdom', 'Basic Scholar', 'Curse', 1500),
             'Astral': ('Wizard', 'Hypnotize', 'Advanced Wisdom', '', 'Hypnotize', 1500),
             'Cyra': ('Wizard', 'Haste', 'Basic Wisdom', 'Basic Diplomacy', 'Haste', 1500),
             'Daremyth': ('Wizard', 'Fortune', 'Basic Wisdom', 'Basic Intelligence', 'Fortune', 1500),
             'Halon': ('Wizard', 'Mysticism', 'Basic Wisdom', 'Basic Mysticism', 'Stone Skin', 1500),
             'Serena': ('Wizard', 'Eagle Eye', 'Basic Wisdom', 'Basic Eagle Eye', 'Dispel', 1500),
             'Solmyr': ('Wizard', 'Chain Lightning', 'Basic Wisdom', 'Basic Sorcery', 'Chain Lightning', 1500),
             'Theodorus': ('Wizard', 'Magi', 'Basic Wisdom', 'Basic Ballistics', 'Shield', 1500),
             'Dracon': ('Wizard', 'Enchanters', 'Advanced Wisdom', '', 'Haste', 1900),

             'Calh': ('Demoniac', 'Gogs', 'Basic Archery', 'Basic Scouting', '', 1630),
             'Fiona': ('Demoniac', 'Hell Hounds', 'Advanced Scouting', '', '', 1630),
             'Ignatius': ('Demoniac', 'Imps', 'Basic Tactics', 'Basic Interference', '', 1700),
             'Marius': ('Demoniac', 'Demons', 'Advanced Armorer', '', '', 1560),
             'Nymus': ('Demoniac', 'Pit Fiends', 'Advanced Offense', '', '', 1560),
             'Octavia': ('Demoniac', 'Gold', 'Basic Scholar', 'Basic Offense', '', 1560),
             'Pyre': ('Demoniac', 'Ballista', 'Basic Logistics', 'Basic Artillery', '', 1711),
             'Rashka': ('Demoniac', 'Efreet', 'Basic Scholar', 'Basic Wisdom', '', 1560),
             'Xeron': ('Demoniac', 'Devils', 'Basic Leadership', 'Basic Tactics', '', 1630),

             'Ash': ('Heretic', 'Bloodlust', 'Basic Wisdom', 'Basic Eagle Eye', 'Bloodlust', 1560),
             'Axsis': ('Heretic', 'Mysticism', 'Basic Wisdom', 'Basic Mysticism', 'Protection from Air', 1560),
             'Ayden': ('Heretic', 'Intelligence', 'Basic Wisdom', 'Basic Intelligence', 'View Earth', 1560),
             'Calid': ('Heretic', 'Sulfur', 'Basic Wisdom', 'Basic Learning', 'Haste', 1560),
             'Olema': ('Heretic', 'Weakness', 'Basic Wisdom', 'Basic Ballistics', 'Weakness', 1560),
             'Xarfax': ('Heretic', 'Fireball', 'Basic Wisdom', 'Basic Leadership', 'Fireball', 1560),
             'Xyron': ('Heretic', 'Inferno', 'Basic Wisdom', 'Basic Scholar', 'Inferno', 1560),
             'Zydar': ('Heretic', 'Sorcery', 'Basic Wisdom', 'Basic Sorcery', 'Stone Skin', 1560),

             'Charna': ('Death Knight', 'Wights', 'Basic Necromancy', 'Basic Tactics', 'Magic Arrow', 1560),
             'Clavius': ('Death Knight', 'Gold', 'Basic Necromancy', 'Basic Offense', 'Magic Arrow', 1500),
             'Galthran': ('Death Knight', 'Skeletons', 'Basic Necromancy', 'Basic Armorer', 'Shield', 1630),
             'Isra': ('Death Knight', 'Necromancy', 'Advanced Necromancy', '', 'Magic Arrow', 1500),
             'Moandor': ('Death Knight', 'Liches', 'Basic Necromancy', 'Basic Learning', 'Slow', 1500),
             'Straker': ('Death Knight', 'Walking Dead', 'Basic Necromancy', 'Basic Interference', 'Haste', 1560),
             'Tamika': ('Death Knight', 'Black Knights', 'Basic Necromancy', 'Basic Offense', 'Magic Arrow', 1500),
             'Vokial': ('Death Knight', 'Vampires', 'Basic Necromancy', 'Basic Artillery', 'Stone Skin', 1500),
             'Haart Lich': ('Death Knight', 'Black Knights', 'Advanced Necromancy', '', 'Slow', 1500),
             'Ranloo': ('Death Knight', 'Ballista', 'Basic Necromancy', 'Basic Artillery', 'Haste', 1560),

             'Aislinn': ('Necromancer', 'Meteor Shower', 'Basic Necromancy', 'Basic Wisdom', 'Meteor Shower', 1500),
             'Nagash': ('Necromancer', 'Gold', 'Basic Necromancy', 'Basic Intelligence', 'Protection from Air', 1500),
             'Nimbus': ('Necromancer', 'Eagle Eye', 'Basic Necromancy', 'Basic Eagle Eye', 'Shield', 1500),
             'Sandro': ('Necromancer', 'Sorcery', 'Basic Necromancy', 'Basic Sorcery', 'Slow', 1500),
             'Septienna': ('Necromancer', 'Death Ripple', 'Basic Necromancy', 'Basic Scholar', 'Death Ripple', 1500),
             'Thant': ('Necromancer', 'Animate Dead', 'Basic Necromancy', 'Basic Mysticism', 'Animate Dead', 1500),
             'Vidomina': ('Necromancer', 'Necromancy', 'Advanced Necromancy', '', 'Curse', 1500),
             'Xsi': ('Necromancer', 'Stone Skin', 'Basic Necromancy', 'Basic Learning', 'Stone Skin', 1500),

             'Ajit': ('Overlord', 'Beholders', 'Basic Leadership', 'Basic Interference', '', 1560),
             'Arlach': ('Overlord', 'Ballista', 'Basic Offense', 'Basic Artillery', '', 1560),
             'Dace': ('Overlord', 'Minotaurs', 'Basic Tactics', 'Basic Offense', '', 1560),
             'Damacon': ('Overlord', 'Gold', 'Advanced Offense', '', '', 1560),
             'Gunnar': ('Overlord', 'Logistics', 'Basic Tactics', 'Basic Logistics', '', 1641),
             'Lorelei': ('Overlord', 'Harpies', 'Basic Leadership', 'Basic Scouting', '', 1760),
             'Shakti': ('Overlord', 'Troglodytes', 'Basic Offense', 'Basic Tactics', '', 1630),
             'Synca': ('Overlord', 'Manticores', 'Basic Leadership', 'Basic Scholar', '', 1560),
             'Mutare': ('Overlord', 'Dragons', 'Basic Estates', 'Basic Tactics', 'Magic Arrow', 1560),
             'Mutare Drake': ('Overlord', 'Dragons', 'Basic Estates', 'Basic Tactics', 'Magic Arrow', 1560),

             'Alamar': ('Warlock', 'Resurrection', 'Basic Wisdom', 'Basic Scholar', 'Resurrection', 1560),
             'Darkstorn': ('Warlock', 'Stone Skin', 'Basic Wisdom', 'Basic Learning', 'Stone Skin', 1560),
             'Deemer': ('Warlock', 'Meteor Shower', 'Basic Wisdom', 'Basic Scouting', 'Meteor Shower', 1560),
             'Geon': ('Warlock', 'Eagle Eye', 'Basic Wisdom', 'Basic Eagle Eye', 'Slow', 1560),
             'Jaegar': ('Warlock', 'Mysticism', 'Basic Wisdom', 'Basic Mysticism', 'Shield', 1560),
             'Jeddite': ('Warlock', 'Resurrection', 'Advanced Wisdom', '', 'Resurrection', 1560),
             'Malekith': ('Warlock', 'Sorcery', 'Basic Wisdom', 'Basic Sorcery', 'Bloodlust', 1560),
             'Sephinroth': ('Warlock', 'Crystal', 'Basic Wisdom', 'Basic Intelligence', 'Protection from Air', 1560),

             'Crag Hack': ('Barbarian', 'Offense', 'Advanced Offense', '', '', 1560),
             'Gretchin': ('Barbarian', 'Goblins', 'Basic Offense', 'Basic pathfinding', '', 1700),
             'Gurnisson': ('Barbarian', 'Ballista', 'Basic Offense', 'Basic Artillery', '', 1560),
             'Jabarkas': ('Barbarian', 'Orcs', 'Basic Offense', 'Basic Archery', '', 1630),
             'Krellion': ('Barbarian', 'Ogres', 'Basic Offense', 'Basic Interference', '', 1560),
             'Shiva': ('Barbarian', 'Rocs', 'Basic Offense', 'Basic Scouting', '', 1560),
             'Tyraxor': ('Barbarian', 'Wolf Riders', 'Basic Offense', 'Basic Tactics', '', 1760),
             'Yog': ('Barbarian', 'Cyclops', 'Basic Offense', 'Basic Ballistics', '', 1560),
             'Boragus': ('Barbarian', 'Ogres', 'Basic Offense', 'Basic Tactics', '', 1560),
             'Kilgor': ('Barbarian', 'Behemoths', 'Advanced Offense', '', '', 1560),

             'Dessa': ('Battle Mage', 'Logistics', 'Basic Wisdom', 'Basic Logistics', 'Stone Skin', 1641),
             'Gird': ('Battle Mage', 'Sorcery', 'Basic Wisdom', 'Basic Sorcery', 'Bloodlust', 1560),
             'Gundula': ('Battle Mage', 'Offense', 'Basic Wisdom', 'Basic Offense', 'Slow', 1560),
             'Oris': ('Battle Mage', 'Eagle Eye', 'Basic Wisdom', 'Basic Eagle Eye', 'Protection from Air', 1560),
             'Saurug': ('Battle Mage', 'Gems', 'Basic Wisdom', 'Basic Interference', 'Bloodlust', 1560),
             'Terek': ('Battle Mage', 'Haste', 'Basic Wisdom', 'Basic Tactics', 'Haste', 1560),
             'Vey': ('Battle Mage', 'Ogres', 'Basic Wisdom', 'Basic Leadership', 'Magic Arrow', 1560),
             'Zubin': ('Battle Mage', 'Precision', 'Basic Wisdom', 'Basic Artillery', 'Precision', 1560),

             'Alkin': ('Beastmaster', 'Gorgons', 'Basic Armorer', 'Basic Offense', '', 1560),
             'Broghild': ('Beastmaster', 'Wyverns', 'Basic Armorer', 'Basic Scouting', '', 1560),
             'Bron': ('Beastmaster', 'Basilisks', 'Basic Armorer', 'Basic Interference', '', 1560),
             'Drakon': ('Beastmaster', 'Gnolls', 'Basic Armorer', 'Basic Leadership', '', 1630),
             'Gerwulf': ('Beastmaster', 'Ballista', 'Basic Armorer', 'Basic Artillery', '', 1560),
             'Korbac': ('Beastmaster', 'Serpent Flies', 'Basic Armorer', 'Basic Pathfinding', '', 1560),
             'Tazar': ('Beastmaster', 'Armorer', 'Advanced Armorer', '', '', 1560),
             'Wystan': ('Beastmaster', 'Lizardman', 'Basic Armorer', 'Basic Archery', '', 1630),

             'Andra': ('Witch', 'Intelligence', 'Basic Wisdom', 'Basic Intelligence', 'Dispel', 1560),
             'Merist': ('Witch', 'Stone Skin', 'Basic Wisdom', 'Basic Learning', 'Stone Skin', 1560),
             'Mirlanda': ('Witch', 'Weakness', 'Advanced Wisdom', '', 'Weakness', 1560),
             'Rosic': ('Witch', 'Mysticism', 'Basic Wisdom', 'Basic Mysticism', 'Magic Arrow', 1560),
             'Styg': ('Witch', 'Sorcery', 'Basic Wisdom', 'Basic Sorcery', 'Shield', 1560),
             'Tiva': ('Witch', 'Eagle Eye', 'Basic Wisdom', 'Basic Eagle Eye', 'Stone Skin', 1560),
             'Verdish': ('Witch', 'First Aid', 'Basic Wisdom', 'Basic First Aid', 'Protection from Fire', 1560),
             'Voy': ('Witch', 'Navigation', 'Basic Wisdom', 'Basic Navigation', 'Slow', 1560),
             'Adrienne': ('Witch', 'Fire Magic', 'Basic Wisdom', 'Expert Fire Magic', 'Inferno', 1560),
             'Kinkeria': ('Witch', 'Learning', 'Basic Wisdom', 'Basic Learning', 'Slow', 1560),

             'Erdamon': ('Planeswalker', 'Earth Elementals', 'Basic Tactics', 'Basic Estates', '', 1630),
             'Fiur': ('Planeswalker', 'Fire Elementals', 'Advanced Offense', '', '', 1630),
             'Ignissa': ('Planeswalker', 'Fire Elementals', 'Basic Offense', 'Basic Artillery', '', 1630),
             'Kalt': ('Planeswalker', 'Water Elementals', 'Basic Tactics', 'Basic Learning', '', 1630),
             'Lacus': ('Planeswalker', 'Water Elementals', 'Advanced Tactics', '', '', 1630),
             'Monere': ('Planeswalker', 'Psychic Elementals', 'Basic Tactics', 'Basic Offense', '', 1848),
             'Pasis': ('Planeswalker', 'Psychic Elementals', 'Basic Tactics', 'Basic Artillery', '', 1760),
             'Thunar': ('Planeswalker', 'Earth Elementals', 'Basic Tactics', 'Basic Estates', '', 1630),

             'Aenain': ('Elementalist', 'Disrupting Ray', 'Basic Wisdom', 'Basic Air Magic', 'Disrupting Ray', 1630),
             'Brissa': ('Elementalist', 'Haste', 'Basic Wisdom', 'Basic Air Magic', 'Haste', 1630),
             'Ciele': ('Elementalist', 'Magic Arrow', 'Basic Wisdom', 'Basic Water Magic', 'Magic Arrow', 1630),
             'Gelare': ('Elementalist', 'Gold', 'Basic Wisdom', 'Basic Water Magic', 'Dispel', 1630),
             'Grindan': ('Elementalist', 'Gold', 'Basic Wisdom', 'Basic Earth Magic', 'Slow', 1630),
             'Inteus': ('Elementalist', 'Bloodlust', 'Basic Wisdom', 'Basic Fire Magic', 'Bloodlust', 1630),
             'Labetha': ('Elementalist', 'Stone Skin', 'Basic Wisdom', 'Basic Earth Magic', 'Stone Skin', 1630),
             'Luna': ('Elementalist', 'Fire Wall', 'Basic Wisdom', 'Basic Fire Magic', 'Fire Wall', 1630)
             }

