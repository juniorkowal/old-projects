"""Script containing spell type class and spell dataset"""
from data.magic import *


class Spell_type:
    def __init__(self, type_offence_defence: int, type_target: int, class_of_spell: Spell, power: int):
        """
        Class representing spell type.
        :param type_offence_defence: Parameter stating the type of spell
        :param type_target: Whether spell has a target
        :param class_of_spell: Spell school
        :param power: Power of the spell
        """
        # 0 -> defence spell (use on allies)     1 -> offence spell (use on enemies)      2 -> spell casted on everyone
        self.type_offence_defence = type_offence_defence
        # 0 -> spell casted on 1 target          1 -> spell casted on all enemies or allies
        self.type_target = type_target
        # Adding whole spell class to get values of mana_cost etc...
        self.class_of_spell = class_of_spell
        # Spell defining power (basic -> 0, advanced -> 1, expert -> 2)
        self.power = power


# Defining lists of every power of spell (basic, advanced, expert)
# Excluded spells: Sacrifice, Resurrection, Dimension Door,
#                  Remove Obstacle, Scuttle Boat, Summon Boat, Teleport, Town Portal,
#                  View Air, View Earth, Visions, Water Walk

Air_Shield_list = [Spell_type(0, 0, Air_Shield, 0),
                   Spell_type(0, 0, Air_Shield, 1),
                   Spell_type(0, 1, Air_Shield, 2)]
Animate_Dead_list = [Spell_type(0, 0, Animate_Dead, 0),
                     Spell_type(0, 0, Animate_Dead, 1),
                     Spell_type(0, 0, Animate_Dead, 2)]
Anti_Magic_list = [Spell_type(0, 0, Anti_Magic, 0),
                   Spell_type(0, 0, Anti_Magic, 1),
                   Spell_type(0, 0, Anti_Magic, 2)]
Armageddon_list = [Spell_type(2, 1, Armageddon, 0),
                   Spell_type(2, 1, Armageddon, 1),
                   Spell_type(2, 1, Armageddon, 2)]
Berserk_list = [Spell_type(2, 1, Berserk, 0),
                Spell_type(2, 1, Berserk, 1),
                Spell_type(2, 1, Berserk, 2)]
Bless_list = [Spell_type(0, 0, Bless, 0),
              Spell_type(0, 0, Bless, 1),
              Spell_type(0, 1, Bless, 2)]
Blind_list = [Spell_type(1, 0, Blind, 0),
              Spell_type(1, 0, Blind, 1),
              Spell_type(1, 0, Blind, 2)]
Bloodlust_list = [Spell_type(0, 0, Bloodlust, 0),
                  Spell_type(0, 0, Bloodlust, 1),
                  Spell_type(0, 1, Bloodlust, 2)]
Chain_Lightning_list = [Spell_type(1, 0, Chain_Lightning, 0),
                        Spell_type(1, 0, Chain_Lightning, 1),
                        Spell_type(1, 0, Chain_Lightning, 2)]
Clone_list = [Spell_type(0, 0, Clone, 0),
              Spell_type(0, 0, Clone, 1),
              Spell_type(0, 0, Clone, 2)]
Counterstrike_list = [Spell_type(0, 0, Counterstrike, 0),
                      Spell_type(0, 0, Counterstrike, 1),
                      Spell_type(0, 1, Counterstrike, 2)]
Cure_list = [Spell_type(0, 0, Cure, 0),
             Spell_type(0, 0, Cure, 1),
             Spell_type(0, 1, Cure, 2)]
Curse_list = [Spell_type(1, 0, Curse, 0),
              Spell_type(1, 0, Curse, 1),
              Spell_type(1, 1, Curse, 2)]
Death_Ripple_list = [Spell_type(2, 1, Death_Ripple, 0),
                     Spell_type(2, 1, Death_Ripple, 1),
                     Spell_type(2, 1, Death_Ripple, 2)]
Destroy_Undead_list = [Spell_type(2, 1, Destroy_Undead, 0),
                       Spell_type(2, 1, Destroy_Undead, 1),
                       Spell_type(2, 1, Destroy_Undead, 2)]
Dispel_list = [Spell_type(0, 0, Dispel, 0),
               Spell_type(2, 0, Dispel, 1),
               Spell_type(2, 1, Dispel, 2)]
Disrupting_Ray_list = [Spell_type(1, 0, Disrupting_Ray, 0),
                       Spell_type(1, 0, Disrupting_Ray, 1),
                       Spell_type(1, 0, Disrupting_Ray, 2)]
Earthquake_list = [Spell_type(2, 1, Earthquake, 0),
                   Spell_type(2, 1, Earthquake, 1),
                   Spell_type(2, 1, Earthquake, 2)]
Fire_Shield_list = [Spell_type(0, 1, Fire_Shield, 0),
                    Spell_type(0, 1, Fire_Shield, 1),
                    Spell_type(0, 1, Fire_Shield, 2)]
Fire_Wall_list = [Spell_type(1, 0, Fire_Wall, 0),
                  Spell_type(1, 0, Fire_Wall, 1),
                  Spell_type(1, 0, Fire_Wall, 2)]
Fireball_list = [Spell_type(1, 0, Fireball, 0),
                 Spell_type(1, 0, Fireball, 1),
                 Spell_type(1, 0, Fireball, 2)]
Force_Field_list = [Spell_type(0, 0, Force_Field, 0),
                    Spell_type(0, 0, Force_Field, 1),
                    Spell_type(0, 0, Force_Field, 2)]
Forgetfulness_list = [Spell_type(1, 0, Forgetfulness, 0),
                      Spell_type(1, 0, Forgetfulness, 1),
                      Spell_type(1, 1, Forgetfulness, 2)]
Fortune_list = [Spell_type(0, 0, Fortune, 0),
                Spell_type(0, 0, Fortune, 1),
                Spell_type(0, 0, Fortune, 2)]
Frenzy_list = [Spell_type(0, 0, Frenzy, 0),
               Spell_type(0, 0, Frenzy, 1),
               Spell_type(0, 0, Frenzy, 2)]
Frost_Ring_list = [Spell_type(0, 0, Frost_Ring, 0),
                   Spell_type(0, 0, Frost_Ring, 1),
                   Spell_type(0, 0, Frost_Ring, 2)]
Haste_list = [Spell_type(0, 0, Haste, 0),
              Spell_type(0, 0, Haste, 1),
              Spell_type(0, 1, Haste, 2)]
Hypnotize_list = [Spell_type(1, 0, Hypnotize, 0),
                  Spell_type(1, 0, Hypnotize, 1),
                  Spell_type(1, 0, Hypnotize, 2)]
Ice_Bolt_list = [Spell_type(1, 0, Ice_Bolt, 0),
                 Spell_type(1, 0, Ice_Bolt, 1),
                 Spell_type(1, 0, Ice_Bolt, 2)]
Implosion_list = [Spell_type(1, 0, Implosion, 0),
                  Spell_type(1, 0, Implosion, 1),
                  Spell_type(1, 0, Implosion, 2)]
Inferno_list = [Spell_type(1, 0, Inferno, 0),
                Spell_type(1, 0, Inferno, 1),
                Spell_type(1, 0, Inferno, 2)]
Land_Mine_list = [Spell_type(2, 1, Land_Mine, 0),
                  Spell_type(2, 1, Land_Mine, 1),
                  Spell_type(2, 1, Land_Mine, 2)]
Lightning_Bolt_list = [Spell_type(1, 0, Lightning_Bolt, 0),
                       Spell_type(1, 0, Lightning_Bolt, 1),
                       Spell_type(1, 0, Lightning_Bolt, 2)]
Magic_Arrow_list = [Spell_type(1, 0, Magic_Arrow, 0),
                    Spell_type(1, 0, Magic_Arrow, 1),
                    Spell_type(1, 0, Magic_Arrow, 2)]
Magic_Mirror_list = [Spell_type(0, 0, Magic_Mirror, 0),
                     Spell_type(0, 0, Magic_Mirror, 1),
                     Spell_type(0, 0, Magic_Mirror, 2)]
Meteor_Shower_list = [Spell_type(1, 0, Meteor_Shower, 0),
                      Spell_type(1, 0, Meteor_Shower, 1),
                      Spell_type(1, 0, Meteor_Shower, 2)]
Mirth_list = [Spell_type(0, 0, Mirth, 0),
              Spell_type(0, 0, Mirth, 1),
              Spell_type(0, 1, Mirth, 2)]
Misfortune_list = [Spell_type(1, 0, Misfortune, 0),
                   Spell_type(1, 0, Misfortune, 1),
                   Spell_type(1, 1, Misfortune, 2)]
Prayer_list = [Spell_type(0, 0, Prayer, 0),
               Spell_type(0, 0, Prayer, 1),
               Spell_type(0, 1, Prayer, 2)]
Precision_list = [Spell_type(0, 0, Precision, 0),
                  Spell_type(0, 0, Precision, 1),
                  Spell_type(0, 1, Precision, 2)]
Protection_from_Air_list = [Spell_type(0, 0, Protection_from_Air, 0),
                            Spell_type(0, 0, Protection_from_Air, 1),
                            Spell_type(0, 1, Protection_from_Air, 2)]
Protection_from_Earth_list = [Spell_type(0, 0, Protection_from_Earth, 0),
                              Spell_type(0, 0, Protection_from_Earth, 1),
                              Spell_type(0, 1, Protection_from_Earth, 2)]
Protection_from_Fire_list = [Spell_type(0, 0, Protection_from_Fire, 0),
                             Spell_type(0, 0, Protection_from_Fire, 1),
                             Spell_type(0, 1, Protection_from_Fire, 2)]
Protection_from_Water_list = [Spell_type(0, 0, Protection_from_Water, 0),
                              Spell_type(0, 0, Protection_from_Water, 1),
                              Spell_type(0, 1, Protection_from_Water, 2)]
Quicksand_list = [Spell_type(2, 1, Quicksand, 0),
                  Spell_type(2, 1, Quicksand, 1),
                  Spell_type(2, 1, Quicksand, 2)]
Shield_list = [Spell_type(0, 0, Shield, 0),
               Spell_type(0, 0, Shield, 1),
               Spell_type(0, 1, Shield, 2)]
Slayer_list = [Spell_type(0, 0, Slayer, 0),
               Spell_type(0, 0, Slayer, 1),
               Spell_type(0, 0, Slayer, 2)]
Slow_list = [Spell_type(1, 0, Slow, 0),
             Spell_type(1, 0, Slow, 1),
             Spell_type(1, 1, Slow, 2)]
Sorrow_list = [Spell_type(1, 0, Sorrow, 0),
               Spell_type(1, 0, Sorrow, 1),
               Spell_type(1, 1, Sorrow, 2)]
Stone_Skin_list = [Spell_type(0, 0, Stone_Skin, 0),
                   Spell_type(0, 0, Stone_Skin, 1),
                   Spell_type(0, 1, Stone_Skin, 2)]
Summon_Air_Elemental_list = [Spell_type(0, 1, Summon_Air_Elemental, 0),
                             Spell_type(0, 1, Summon_Air_Elemental, 1),
                             Spell_type(0, 1, Summon_Air_Elemental, 2)]
Summon_Earth_Elemental_list = [Spell_type(0, 1, Summon_Earth_Elemental, 0),
                               Spell_type(0, 1, Summon_Earth_Elemental, 1),
                               Spell_type(0, 1, Summon_Earth_Elemental, 2)]
Summon_Fire_Elemental_list = [Spell_type(0, 1, Summon_Fire_Elemental, 0),
                              Spell_type(0, 1, Summon_Fire_Elemental, 1),
                              Spell_type(0, 1, Summon_Fire_Elemental, 2)]
Summon_Water_Elemental_list = [Spell_type(0, 1, Summon_Water_Elemental, 0),
                               Spell_type(0, 1, Summon_Water_Elemental, 1),
                               Spell_type(0, 1, Summon_Water_Elemental, 2)]
Titans_Lightning_Bolt_list = [Spell_type(1, 0, Titans_Lightning_Bolt, 0),
                              Spell_type(1, 0, Titans_Lightning_Bolt, 1),
                              Spell_type(1, 0, Titans_Lightning_Bolt, 2)]
Weakness_list = [Spell_type(1, 0, Weakness, 0),
                 Spell_type(1, 0, Weakness, 1),
                 Spell_type(1, 1, Weakness, 2)]

list_of_spell_names = ['Bloodlust', 'Cure', 'Curse', 'Dispel', 'Bless', 'Haste', 'Magic_Arrow', 'Protection_from_Fire',
                       'Protection_from_Water', 'Shield', 'Slow', 'Summon_Boat', 'Stone_Skin', 'View_Air', 'View_Earth',
                       'Blind', 'Death_Ripple', 'Disguise', 'Disrupting_Ray', 'Fire_Wall', 'Fortune', 'Ice_Bolt',
                       'Lightning_Bolt', 'Precision', 'Protection_from_Air', 'Quicksand', 'Remove_Obstacle',
                       'Scuttle_Boat', 'Visions', 'Weakness', 'Air_Shield', 'Animate_Dead', 'Anti_Magic',
                       'Destroy_Undead', 'Earthquake', 'Fireball', 'Force_Field', 'Forgetfulness', 'Frost_Ring',
                       'Hypnotize', 'Land_Mine', 'Mirth', 'Misfortune', 'Protection_from_Earth', 'Teleport',
                       'Armageddon', 'Berserk', 'Chain_Lightning', 'Clone', 'Counterstrike', 'Fire_Shield', 'Frenzy',
                       'Inferno', 'Meteor_Shower', 'Prayer', 'Resurrection', 'Slayer', 'Sorrow', 'Town_Portal',
                       'Water_Walk', 'Dimension_Door', 'Fly', 'Implosion', 'Magic_Mirror', 'Sacrifice',
                       'Summon_Air_Elemental', 'Summon_Earth_Elemental', 'Summon_Fire_Elemental',
                       'Summon_Water_Elemental', 'Titans_Lightning_Bolt']

list_of_spells_lists = [Air_Shield_list, Animate_Dead_list, Anti_Magic_list, Armageddon_list, Berserk_list,
                        Bless_list, Blind_list, Bloodlust_list, Chain_Lightning_list, Clone_list,
                        Counterstrike_list, Cure_list, Curse_list, Death_Ripple_list, Destroy_Undead_list,
                        Dispel_list, Disrupting_Ray_list, Earthquake_list, Fire_Shield_list, Fire_Wall_list,
                        Fireball_list, Force_Field_list, Forgetfulness_list, Fortune_list, Frenzy_list,
                        Frost_Ring_list, Haste_list, Hypnotize_list, Ice_Bolt_list, Implosion_list,
                        Inferno_list, Land_Mine_list, Lightning_Bolt_list, Magic_Arrow_list,
                        Magic_Mirror_list, Meteor_Shower_list, Mirth_list, Misfortune_list,
                        Prayer_list, Precision_list, Protection_from_Air_list, Protection_from_Earth_list,
                        Protection_from_Fire_list, Protection_from_Water_list, Quicksand_list, Shield_list,
                        Slayer_list, Slow_list, Sorrow_list, Stone_Skin_list, Summon_Air_Elemental_list,
                        Summon_Earth_Elemental_list, Summon_Fire_Elemental_list, Summon_Water_Elemental_list,
                        Titans_Lightning_Bolt_list, Weakness_list]

spell_ranking = ['Implosion', 'Animate_Dead', 'Slow', 'Blind', 'Chain_Lightning', 'Haste', 'Meteor_Shower', 'Shield',
                 'Stone_Skin', 'Anti_Magic', 'Summon_Earth_Elemental', 'Berserk', 'Armageddon', 'Curse', 'Death_Ripple', 'Summon_Air_Elemental', 'Summon_Earth_Elemental', 'Titans_Lightning_Bolt',
                 'Lightning_Bolt', 'Bless', 'Cure', 'Prayer', 'Bloodlust', 'Frenzy', 'Ice_Bolt', 'Protection_from_Earth', 'Magic_Arrow', 'Summon_Water_Elemental',
                 'Quicksand', 'Clone', 'Air_Shield', 'Fireball', 'Dispel', 'Protection_from_Fire', 'Disrupting_Ray', 'Forgetfulness', 'Land_Mine', 'Mirth', 'Sorrow', 'Misfortune', 'Weakness',
                 'Protection_from_Water', 'Frost_Ring', 'Slayer', 'Protection_from_Air', 'Fire_Shield', 'Magic_Mirror', 'Inferno', 'Precision', 'Fire_Wall', 'Earthquake', 'Fortune', 'Counterstrike', 'Destroy_Undead']
