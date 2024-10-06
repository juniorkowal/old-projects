"""Script containing Spell class and all the spell objects"""


class Spell:
    def __init__(self, name: str, school: str, lvl: int, duration: int, mana_cost: int, dmg: int = 0):
        """
        Class representing a spell.

        :param name: Name of the spell
        :param school: School of the spell (there are 4)
        :param lvl: Level of the school
        :param duration: Duration of the spell
        :param mana_cost: Mana cost of the spell
        :param dmg: Damage of the spell
        """
        self.name = name
        self.lvl = lvl
        self.school = school
        self.mana_cost = mana_cost
        self.duration = duration
        self.dmg = dmg


class Spells:
    def __init__(self, *spells: Spell):
        """
        Class representing spells (again)

        :param spells: Spell class
        """
        self.spells = spells
# name, school, lvl, duration, mana_cost,dmg
# lvl 1
Bloodlust = Spell("Bloodlust", "Fire Magic", 1, 1, 5)
Cure = Spell("Cure", "Water Magic", 1, 0, 6)
Curse = Spell("Curse", "Fire Magic", 1, 1, 6)
Dispel = Spell("Dispel", "Water Magic", 1, 0, 5)
Bless = Spell("Bless", "Water Magic", 1, 1, 5)
Haste = Spell("Haste", "Air Magic", 1, 1, 6)
Magic_Arrow = Spell("Magic_Arrow", "All Schools", 1, 0, 5, 10 + (10 * 5))
Protection_from_Fire = Spell("Protection_from_Fire", "Fire Magic", 1, 1, 5)
Protection_from_Water = Spell("Protection_from_Water", "Water Magic", 1, 1, 5)
Shield = Spell("Shield", "Earth Magic", 1, 1, 5)
Slow = Spell("Slow", "Earth Magic", 1, 1, 6)
Summon_Boat = Spell("Summon_Boat", "Water Magic", 1, 0, 8)
Stone_Skin = Spell("Stone_Skin", "Earth Magic", 1, 1, 5)
View_Air = Spell("View_Air", "Air Magic", 1, 0, 2)
View_Earth = Spell("View_Earth", "Earth Magic", 1, 0, 2)
# lvl 2
Blind = Spell("Blind", "Fire Magic", 2, 1, 10)
Death_Ripple = Spell("Death_Ripple", "Earth Magic", 2, 0, 10, 10+(5 * 5))
Disguise = Spell("Disguise", "Air Magic", 2, 1, 4)
Disrupting_Ray = Spell("Disrupting_Ray", "Air Magic", 2, 10000000, 10)
Fire_Wall = Spell("Fire_Wall", "Fire Magic", 2, 2, 8)
Fortune = Spell("Fortune", "Air Magic", 2, 1, 7)
Ice_Bolt = Spell("Ice_Bolt", "Water Magic", 2, 0, 8, 10+(20 * 5))
Lightning_Bolt = Spell("Lightning_Bolt", "Air Magic", 2, 0, 10, 10 + (25*5))
Precision = Spell("Precision", "Air Magic", 2, 1, 8)
Protection_from_Air = Spell("Protection_from_Air", "Air Magic", 2, 1, 7)
Quicksand = Spell("Quicksand", "Earth Magic", 2, 10000000, 8)
Remove_Obstacle = Spell("Remove_Obstacle", "Water Magic", 2, 0, 7)
Scuttle_Boat = Spell("Scuttle_Boat", "Water Magic", 2, 0, 8)
Visions = Spell("Visions", "All Schools", 2, 1, 4)
Weakness = Spell("Weakness", "Water Magic", 2, 1, 8)
# lvl 3
Air_Shield = Spell("Air_Shield", "Air Magic", 3, 1, 12)
Animate_Dead = Spell("Animate_Dead", "Earth Magic", 3, 10000000, 15)
Anti_Magic = Spell("Anti_Magic", "Earth Magic", 3, 1, 15)
Destroy_Undead = Spell("Destroy_Undead", "Air Magic", 3, 0, 15, 10 + (10*5))
Earthquake = Spell("Earthquake", "Earth Magic", 3, 0, 20)
Fireball = Spell("Fireball", "Fire Magic", 3, 0, 15, 15+(10*5))
Force_Field = Spell("Force_Field", "Earth Magic", 3, 2, 12)
Forgetfulness = Spell("Forgetfulness", "Water Magic", 3, 1, 12)
Frost_Ring = Spell("Frost_Ring", "Water Magic", 3, 0, 12, 15 + (10 * 5))
Hypnotize = Spell("Hypnotize", "Air Magic", 3, 1, 18)
Land_Mine = Spell("Land_Mine", "Fire Magic", 3, 5555555, 18)
Mirth = Spell("Mirth", "Water Magic", 3, 1, 12)
Misfortune = Spell("Misfortune", "Fire Magic", 3, 1, 12)
Protection_from_Earth = Spell("Protection_from_Earth", "Earth Magic", 3, 1, 12)
Teleport = Spell("Teleport", "Water Magic", 3, 0, 15)
# lvl 4
Armageddon = Spell("Armageddon", "Fire Magic", 4, 0, 24)
Berserk = Spell("Berserk", "Fire Magic", 4, 1, 20)
Chain_Lightning = Spell("Chain_Lightning", "Air Magic", 4, 0, 24)
Clone = Spell("Clone", "Water Magic", 4, 1, 24)
Counterstrike = Spell("Counterstrike", "Air Magic", 4, 1, 24)
Fire_Shield = Spell("Fire_Shield", "Fire Magic", 4, 1, 16)
Frenzy = Spell("Frenzy", "Fire Magic", 4, 1, 16)  #duration
Inferno = Spell("Inferno", "Fire Magic", 4, 0, 16)
Meteor_Shower = Spell("Meteor_Shower", "Earth Magic", 4, 0, 16)
Prayer = Spell("Prayer", "Water Magic", 4, 1, 16)
Resurrection = Spell("Resurrection", "Earth Magic", 4, 5555555, 20)
Slayer = Spell("Slayer", "Fire Magic", 4, 1, 16)
Sorrow = Spell("Sorrow", "Earth Magic", 4, 1, 16)
Town_Portal = Spell("Town_Portal", "Earth Magic", 4, 0, 16)
Water_Walk = Spell("Water_Walk", "Water Magic", 4, 1, 12)
# lvl 5
Dimension_Door = Spell("Dimension_Door", "Air Magic", 5, 0, 25)
Fly = Spell("Fly", "Air Magic", 5, 1, 20)
Implosion = Spell("Implosion", "Earth Magic", 5, 0, 30, 100 + (75 * 5))
Magic_Mirror = Spell("Magic_Mirror", "Air Magic", 5, 1, 25)
Sacrifice = Spell("Sacrifice", "Fire Magic", 5, 555555, 25)
Summon_Air_Elemental = Spell("Summon_Air_Elemental", "Air Magic", 5, 100000, 25)
Summon_Earth_Elemental = Spell("Summon_Earth_Elemental", "Earth Magic", 5, 100000, 25)
Summon_Fire_Elemental = Spell("Summon_Fire_Elemental", "Fire Magic", 5, 10000, 25)
Summon_Water_Elemental = Spell("Summon_Water_Elemental", "Water Magic", 5, 10000, 25)
Titans_Lightning_Bolt = Spell("Titans_Lightning_Bolt", "Air Magic", 5, 0, 0)
