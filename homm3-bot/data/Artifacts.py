"""Script containing artefact handling"""
import GUI_handling.AdventureGUI


def artifact_filler(artifact, hero):
    """
        Function that fills slots with artifacts

        :param artifact: Artifact
        :param hero: Hero object
    """
    counter = 0
    for i, item in enumerate(hero.artifacts[artifact.slot]):
        if item == '':
            hero.artifacts[artifact.slot][i] = artifact
        else:
            counter += 1
    if counter == len(hero.artifacts[artifact.slot]):
        hero.artifacts['Backpack'].append(artifact)


class Effect:
    def __init__(self, attack: int, defense: int, spell_power: int, knowledge: int):
        """
        Class containing an effect of the artifact

        :param attack: attack parameter
        :param defense: defense parameter
        :param spell_power: spell power parameter
        :param knowledge: knowledge parameter
        """
        self.attack = attack
        self.defense = defense
        self.spell_power = spell_power
        self.knowledge = knowledge


class Artifact:
    def __init__(self, name: str, slot: str, Class: str, val: int, effect: Effect, cost: int, bonus: str):
        """
        Artifact init function.

        :param name: name of the artifact
        :param slot: Which part of the body will artifact be placed in.
        :param Class: Class of the artifact object
        :param val: Value of the artifact
        :param effect: Effect class representing artifact effect
        :param cost: Cost of the artifact
        :param bonus: Bonus that artifact gives
        """
        self.name = name
        self.slot = slot
        self.Class = Class
        self.val = val
        self.effect = effect
        self.cost = cost
        self.bonus = bonus
        self.value = 10000  # TODO: Fill artifacts with correct values

    def __repr__(self):
        return self.name + f' value: ({str(self.value)})'

    def __str__(self):
        return self.name + f' value: ({str(self.value)})'

    # placeholders for end ow week/day function
    def end_day(self, player):
        """
        A buffer function for the end of the day event

        :param player: player object
        """
        pass

    # IT IS IMPORTANT DONT DELETE
    def end_week(self, player):
        """
        A buffer function for the end of the week event

        :param player: player object
        """
        pass

    def action(self, player, hero, okayVal):
        """
        Function that handles action upon finding artifact

        :param player: Player object
        :param hero: Hero object
        :param okayVal: detected okay button index
        """
        GUI_handling.AdventureGUI.accept_offer()
        artifact_filler(self, hero)
        pass


# Value, stats, bonus do uzupelnienia
# (attack, defense, spell_power, knowledge)
Cape_of_Conjuring = Artifact("Cape_of_Conjuring", "Cape", "Treasure", 100, Effect(0, 0, 0, 0), 1500,
                             "spell duration +3")
Dragon_Wing_Tabard = Artifact("Dragon_Wing_Tabard", "Cape", "Minor", 100, Effect(0, 0, 2, 2), 4000,
                              "+2 to spell power and knowledge")
Vampires_Cowl = Artifact("Vampires_Cowl", "Cape", "Minor", 0, Effect(0, 0, 0, 0), 4000, "Necromancy +10%")
Surcoat_of_Counterpoise = Artifact("Surcoat_of_Counterpoise", "Cape", "Major", 200, Effect(0, 0, 0, 0), 4000,
                                   "Magic Resistance +10%")
Ambassadors_Sash = Artifact("Ambassadors_Sash", "Cape", "Major", 100, Effect(0, 0, 0, 0), 5000,
                            "Surrendering cost is reduced by 10%")
Everflowing_Crystal_Cloak = Artifact("Everflowing_Crystal_Cloak", "Cape", "Major", 100, Effect(0, 0, 0, 0), 5000,
                                     "Resource Crystal +1")
Recanters_Cloak = Artifact("Recanters_Cloak", "Cape", "Major", 500, Effect(0, 0, 0, 0), 8000,
                           "Prevents casting lvl 3+ spells")
Cape_of_Velocity = Artifact("Cape_of_Velocity", "Cape", "Major", 500, Effect(0, 0, 0, 0), 10000, "Unit speed +2")
Angel_Wings = Artifact("Angel_Wings", "Cape", "Relic", 800, Effect(0, 0, 0, 0), 20000, "Spell Fly permanent")
Cloak_of_the_Undead_King = Artifact("Cloak_of_the_Undead_King", "Combo", "Relic", 800, Effect(0, 0, 0, 0), 12000,
                                    "Ability to raise Skeletons,Walking Dead, Wights or Liches")
Cape_of_Silence = Artifact("Cape_of_Silence", "Cape", "Major", 500, Effect(0, 0, 0, 0), 7500,
                           "Bans all level 1 and 2 spells in battle")
Diplomats_Cloak = Artifact("Diplomats_Cloak", "Combo", "Relic", 500, Effect(0, 0, 0, 0), 15000,
                           "Allows your hero to retreat or surrender when battling neutral monsters or defending a town. Multiplies your hero army strength by 3")
# Feet
Dragonbone_Greaves = Artifact("Dragonbone_Greaves", "Feet", "Treasure", 100, Effect(0, 0, 1, 1), 2000,
                              "Knowledge +1 Power skill +1")
Boots_of_Speed = Artifact("Boots_of_Speed", "Feet", "Major", 300, Effect(0, 0, 0, 0), 6000, "Hero Movement points +600")
Dead_Mans_Boots = Artifact("Dead_Mans_Boots", "Feet", "Major", 0, Effect(0, 0, 0, 0), 6000, "Necromancy +15%")
Boots_of_Polarity = Artifact("Boots_of_Polarity", "Feet", "Major", 300, Effect(0, 0, 0, 0), 6000,
                             "Magic Resistance +15%")
Sandals_of_the_Saint = Artifact("Sandals_of_the_Saint", "Feet", "Relic", 500, Effect(2, 2, 2, 2), 8000,
                                "All Primary skills +2")
Boots_of_Levitation = Artifact("Boots_of_Levitation", "Feet", "Relic", 500, Effect(0, 0, 0, 0), 10000,
                               "Spell Water Walk permanent")
Wayfarers_Boots = Artifact("Wayfarers_Boots", "Feet", "Major", 100, Effect(0, 0, 0, 0), 5000,
                           "Allows your hero to move over rough terrain without penalty")
# Helm
Helm_of_the_Alabaster_Unicorn = Artifact("Helm_of_the_Alabaster_Unicorn", "Helm", "Treasure", 0, Effect(0, 0, 0, 1),
                                         1000,
                                         "Knowledge +1")
Skull_Helmet = Artifact("Skull_Helmet", "Helm", "Treasure", 0, Effect(0, 0, 0, 2), 3000, "Knowledge +2")
Helm_of_Chaos = Artifact("Helm_of_Chaos", "Helm", "Minor", 0, Effect(0, 0, 0, 3), 4000, "Knowledge +3")
Crown_of_the_Supreme_Magi = Artifact("Crown_of_the_Supreme_Magi", "Helm", "Minor", 0, Effect(0, 0, 0, 4), 5000,
                                     "Knowledge +4")
Hellstorm_Helmet = Artifact("Hellstorm_Helmet", "Helm", "Major", 0, Effect(0, 0, 0, 5), 6000, "	Knowledge +5")
Crown_of_Dragontooth = Artifact("Crown_of_Dragontooth", "Helm", "Relic", 0, Effect(0, 0, 4, 4), 8000,
                                "Spell Power +4 Knowledge +4")
Thunder_Helmet = Artifact("Thunder_Helmet", "Helm", "Relic", 0, Effect(0, 0, -2, 10), 10000,
                          "Knowledge +10 Spell Power -2")
Sea_Captains_Hat = Artifact("Sea_Captains_Hat", "Helm", "Relic", 700, Effect(0, 0, 0, 0), 15000,
                            "Hero sea movement +500 Spells Summon Boat, Scuttle Boat Protects army in whirlpools")
Helm_of_Heavenly_Enlightenment = Artifact("Helm_of_Heavenly_Enlightenment", "Helm", "Relic", 900, Effect(6, 6, 6, 6),
                                          24000, "All Primary Skills +6")
Spellbinders_Hat = Artifact("Spellbinders_Hat", "Helm", "Relic", 0, Effect(0, 0, 0, 0), 30000, "All lvl 5 Spells")
Admirals_Hat = Artifact("Admirals_Hat", "Combo", "Relic", 900, Effect(0, 0, 0, 0), 25000,
                        "Hero sea movement + 1500 No penalty for Boat boarding/disembarking Spells Summon Boat, Scuttle Boat Movement converted between land and sea Protects army in whirlpools")
Crown_of_the_Five_Seas = Artifact("Crown_of_the_Five_Seas", "Helm", "Major", 0, Effect(0, 0, 0, 6), 7000,
                                  "knowledge +6")
# Shield
Shield_of_the_Dwarven_Lords = Artifact("Shield_of_the_Dwarven_Lords", "Shield", "Treasure", 200, Effect(0, 2, 0, 0),
                                       2000, "Defense +2")
Shield_of_the_Yawning_Dead = Artifact("Shield_of_the_Yawning_Dead", "Shield", "Minor", 300, Effect(0, 3, 0, 0), 3000,
                                      "Defense +3")
Buckler_of_the_Gnoll_King = Artifact("Buckler_of_the_Gnoll_King", "Shield", "Minor", 400, Effect(0, 4, 0, 0), 4000,
                                     "Defense +4")
Targ_of_the_Rampaging_Ogre = Artifact("Targ_of_the_Rampaging_Ogre", "Shield", "Major", 500, Effect(0, 5, 0, 0), 5000,
                                      "Defense +5")
Shield_of_the_Damned = Artifact("Shield_of_the_Damned", "Shield", "Major", 600, Effect(0, 6, 0, 0), 6000, "Defense +6")
Dragon_Scale_Shield = Artifact("Dragon_Scale_Shield", "Shield", "Major", 600, Effect(3, 3, 0, 0), 6000,
                               "Attack +3 Defense +3")
Lions_Shield_of_Courage = Artifact("Lions_Shield_of_Courage", "Shield", "Relic", 800, Effect(4, 4, 4, 4), 16000,
                                   "All Primary Skills +4")
Sentinels_Shield = Artifact("Sentinels_Shield", "Shield", "Relic", 500, Effect(-3, 12, 0, 0), 10000,
                            "Defense +12 Attack -3")
Shield_of_Naval_Glory = Artifact("Shield_of_Naval_Glory", "Shield", "Major", 650, Effect(0, 7, 0, 0), 7000,
                                 "defense +7")
# Misc
Spell_Scroll = Artifact("Spell_Scroll", "Misc", "Scroll", 0, Effect(0, 0, 0, 0), 2500, "name of spell")
Charm_of_Mana = Artifact("Charm_of_Mana", "Misc", "Treasure", 0, Effect(0, 0, 0, 0), 500, "Spell points +1/day")
Talisman_of_Mana = Artifact("Talisman_of_Mana", "Misc", "Treasure", 0, Effect(0, 0, 0, 0), 1000, "Spell points +2/day")
Mystic_Orb_of_Mana = Artifact("Mystic_Orb_of_Mana", "Misc", "Treasure", 0, Effect(0, 0, 0, 0), 1500,
                              "Spell points +3/day")
Wizards_Well = Artifact("Wizards_Well", "Combo", "Relic", 0, Effect(0, 0, 0, 0), 3000, "Spell points +all/day")
Orb_of_Silt = Artifact("Orb_of_Silt", "Misc", "Major", 0, Effect(0, 0, 0, 0), 6000, "All Earth spell dmg +50%")
Orb_of_the_Firmament = Artifact("Orb_of_the_Firmament", "Misc", "Major", 0, Effect(0, 0, 0, 0), 6000,
                                "All Air spell dmg +50%")
Orb_of_Driving_Rain = Artifact("Orb_of_Driving_Rain", "Misc", "Major", 0, Effect(0, 0, 0, 0), 6000,
                               "All Water spell dmg +50%")
Orb_of_Tempestuous_Fire = Artifact("Orb_of_Tempestuous_Fire", "Misc", "Major", 0, Effect(0, 0, 0, 0), 6000,
                                   "All Fire spell dmg +50%")
Tome_of_Earth = Artifact("Tome_of_Earth", "Misc", "Relic", 0, Effect(0, 0, 0, 0), 20000, "All Earth spells")
Tome_of_Air = Artifact("Tome_of_Air", "Misc", "Relic", 0, Effect(0, 0, 0, 0), 20000, "All Air spells")
Tome_of_Water = Artifact("Tome_of_Water", "Misc", "Relic", 0, Effect(0, 0, 0, 0), 20000, "All Water spells")
Tome_of_Fire = Artifact("Tome_of_Fire", "Misc", "Relic", 0, Effect(0, 0, 0, 0), 20000, "All Fire spells")
Sphere_of_Permanence = Artifact("Sphere_of_Permanence", "Misc", "Major", 0, Effect(0, 0, 0, 0), 7500,
                                "Immune to Dispel")
Orb_of_Inhibition = Artifact("Orb_of_Inhibition", "Misc", "Relic", 1000, Effect(0, 0, 0, 0), 20000,
                             "Prevents casting all spells")
Orb_of_Vulnerability = Artifact("Orb_of_Vulnerability", "Misc", "Relic", 0, Effect(0, 0, 0, 0), 25000,
                                "All spells usable, no immunities")
Bird_of_Perception = Artifact("Bird_of_Perception", "Misc", "Treasure", 50, Effect(0, 0, 0, 0), 1000, "Eagle Eye +5%")
Stoic_Watchman = Artifact("Stoic_Watchman", "Misc", "Treasure", 100, Effect(0, 0, 0, 0), 2000, "Eagle Eye +10%")
Emblem_of_Cognizance = Artifact("Emblem_of_Cognizance", "Misc", "Treasure", 150, Effect(0, 0, 0, 0), 3000,
                                "Eagle Eye +15%")
Clover_of_Fortune = Artifact("Clover_of_Fortune", "Misc", "Treasure", 150, Effect(0, 0, 0, 0), 1000, "Luck +1")
Ladybird_of_Luck = Artifact("Ladybird_of_Luck", "Misc", "Treasure", 150, Effect(0, 0, 0, 0), 1000, "Luck +1")
Cards_of_Prophecy = Artifact("Cards_of_Prophecy", "Misc", "Treasure", 150, Effect(0, 0, 0, 0), 1000, "Luck +1")
Hourglass_of_the_Evil_Hour = Artifact("Hourglass_of_the_Evil_Hour", "Misc", "Treasure", 200, Effect(0, 0, 0, 0), 2000,
                                      "Luck disabled")
Glyph_of_Gallantry = Artifact("Glyph_of_Gallantry", "Misc", "Treasure", 100, Effect(0, 0, 0, 0), 1000, "Morale +1")
Crest_of_Valor = Artifact("Crest_of_Valor", "Misc", "Treasure", 100, Effect(0, 0, 0, 0), 1000, "Morale +1")
Badge_of_Courage = Artifact("Badge_of_Courage", "Misc", "Treasure", 100, Effect(0, 0, 0, 0), 1000, "Morale +1")
Spirit_of_Oppression = Artifact("Spirit_of_Oppression", "Misc", "Treasure", 500, Effect(0, 0, 0, 0), 2000,
                                "Morale disabled except negative")
Spyglass = Artifact("Spyglass", "Misc", "Treasure", 100, Effect(0, 0, 0, 0), 1000, "Scouting radius +1")
Speculum = Artifact("Speculum", "Misc", "Treasure", 100, Effect(0, 0, 0, 0), 1000, "Scouting radius +1")
Golden_Bow = Artifact("Golden_Bow", "Misc", "Major", 700, Effect(0, 0, 0, 0), 8000, "No range and obstacle penalty")
Bow_of_Elven_Cherrywood = Artifact("Bow_of_Elven_Cherrywood", "Misc", "Treasure", 200, Effect(0, 0, 0, 0), 2000,
                                   "Archery +5%")
Bowstring_of_the_Unicorns_Mane = Artifact("Bowstring_of_the_Unicorns_Mane", "Misc", "Minor", 300, Effect(0, 0, 0, 0),
                                          4000, "Archery +10%")
Angel_Feather_Arrows = Artifact("Angel_Feather_Arrows", "Misc", "Major", 400, Effect(0, 0, 0, 0), 6000, "Archery +15%")
Bow_of_the_Sharpshooter = Artifact("Bow_of_the_Sharpshooter", "Combo", "Relic", 0, Effect(0, 0, 0, 0), 12000,
                                   "No range and obstacle penalty Allows to shoot while adjacent to an enemy Archery +30%")
Vial_of_Lifeblood = Artifact("Vial_of_Lifeblood", "Misc", "Major", 500, Effect(0, 0, 0, 0), 10000, "Unit health +2")
Elixir_of_Life = Artifact("Elixir_of_Life", "Combo", "Relic", 900, Effect(0, 0, 0, 0), 20000,
                          "Unit health +25% & +4Hp Regeneration ability")
Endless_Purse_of_Gold = Artifact("Endless_Purse_of_Gold", "Misc", "Major", 500, Effect(0, 0, 0, 0), 5000, "Gold +500")
Endless_Bag_of_Gold = Artifact("Endless_Bag_of_Gold", "Misc", "Major", 600, Effect(0, 0, 0, 0), 7500, "Gold +750")
Endless_Sack_of_Gold = Artifact("Endless_Sack_of_Gold", "Misc", "Relic", 700, Effect(0, 0, 0, 0), 10000, "Gold +1000")
Inexhaustible_Cart_of_Lumber = Artifact("Inexhaustible_Cart_of_Lumber", "Misc", "Minor", 300, Effect(0, 0, 0, 0), 5000,
                                        "Resource Wood +1")
Inexhaustible_Cart_of_Ore = Artifact("Inexhaustible_Cart_of_Ore", "Misc", "Minor", 300, Effect(0, 0, 0, 0), 5000,
                                     "Resource Ore +1")
Everpouring_Vial_of_Mercury = Artifact("Everpouring_Vial_of_Mercury", "Misc", "Major", 300, Effect(0, 0, 0, 0), 5000,
                                       "Resource Mercury +1")
Cornucopia = Artifact("Cornucopia", "Combo", "Relic", 600, Effect(0, 0, 0, 0), 20000,
                      "Resources Crystal Mercury Sulfur Gem +5")
Legs_of_Legion = Artifact("Legs_of_Legion", "Misc", "Treasure", 400, Effect(0, 0, 0, 0), 5000,
                          "Creature lvl 2 growth +5")
Loins_of_Legion = Artifact("Loins_of_Legion", "Misc", "Minor", 400, Effect(0, 0, 0, 0), 5000,
                           "Creature lvl 3 growth +4")
Torso_of_Legion = Artifact("Torso_of_Legion", "Misc", "Minor", 400, Effect(0, 0, 0, 0), 5000,
                           "Creature lvl 4 growth +3")
Arms_of_Legion = Artifact("Arms_of_Legion", "Misc", "Major", 400, Effect(0, 0, 0, 0), 5000, "Creature lvl 5 growth +2")
Head_of_Legion = Artifact("Head_of_Legion", "Misc", "Major", 400, Effect(0, 0, 0, 0), 5000, "Creature lvl 6 growth +1")
Statue_of_Legion = Artifact("Statue_of_Legion", "Combo", "Relic", 1000, Effect(0, 0, 0, 0), 25000,
                            "Creature growth +50%")
Shackles_of_War = Artifact("Shackles_of_War", "Misc", "Major", 300, Effect(0, 0, 0, 0), 5000,
                           "Prevents retreat and surrender")
Vial_of_Dragon_Blood = Artifact("Vial_of_Dragon_Blood", "Misc", "Relic", 0, Effect(0, 0, 0, 0), 20000,
                                "Dragons gets +5 Attack and Defense")
Golden_Goose = Artifact("Golden_Goose", "Combo", "Relic", 1000, Effect(0, 0, 0, 0), 22500, "brings 4750 gold per day")
Hideous_Mask = Artifact("Hideous_Mask", "Misc", "Minor", 250, Effect(0, 0, 0, 0), 4000, "Decreases enemy's Morale by 1")
Runes_of_Imminency = Artifact("Runes_of_Imminency", "Misc", "Treasure", 150, Effect(0, 0, 0, 0), 2000,
                              "Decrease enemy's Luck by 1")
Demons_Horseshoe = Artifact("Demons_Horseshoe", "Misc", "Treasure", 150, Effect(0, 0, 0, 0), 2000,
                            "Decreases enemy's Luck by 1")
Shamans_Puppet = Artifact("Shamans_Puppet", "Misc", "Minor", 200, Effect(0, 0, 0, 0), 4000,
                          "Decreases enemy's Luck by 2")
Charm_of_Eclipse = Artifact("Charm_of_Eclipse", "Misc", "Minor", 400, Effect(0, 0, 0, 0), 5000,
                            "reduces the Power skill of enemy hero by 10%")
Horn_of_the_Abyss = Artifact("Horn_of_the_Abyss", "Misc", "Relic", 1000, Effect(0, 0, 0, 0), 50000,
                             "After a stack of living creatures is slain, a stack of Fangarms will rise in their stead and will stay loyal to the hero after the battle concludes")
# Necklace
Pendant_of_Dispassion = Artifact("Pendant_of_Dispassion", "Necklace", "Treasure", 100, Effect(0, 0, 0, 0), 1000,
                                 "Immune to Berserk")
Pendant_of_Free_Will = Artifact("Pendant_of_Free_Will", "Necklace", "Treasure", 100, Effect(0, 0, 0, 0), 1000,
                                "Immune to Hypnotize")
Pendant_of_Life = Artifact("Pendant_of_Life", "Necklace", "Treasure", 100, Effect(0, 0, 0, 0), 2500,
                           "Immune to Death Ripple")
Pendant_of_Death = Artifact("Pendant_of_Death", "Necklace", "Treasure", 100, Effect(0, 0, 0, 0), 2500,
                            "Immune to Destroy Undead")
Pendant_of_Total_Recall = Artifact("Pendant_of_Total_Recall", "Necklace", "Treasure", 200, Effect(0, 0, 0, 0), 3000,
                                   "Immune to Forgetfulness")
Pendant_of_Holiness = Artifact("Pendant_of_Holiness", "Necklace", "Treasure", 300, Effect(0, 0, 0, 0), 5000,
                               "Immune to Curse")
Pendant_of_Second_Sight = Artifact("Pendant_of_Second_Sight", "Necklace", "Major", 300, Effect(0, 0, 0, 0), 5000,
                                   "Immune to Blind")
Pendant_of_Negativity = Artifact("Pendant_of_Negativity", "Necklace", "Major", 400, Effect(0, 0, 0, 0), 5000,
                                 "Immune to Lightning Bolt Immune to Chain Lightning")
Collar_of_Conjuring = Artifact("Collar_of_Conjuring", "Necklace", "Treasure", 0, Effect(0, 0, 0, 0), 500,
                               "Spell duration +1")
Amulet_of_the_Undertaker = Artifact("Amulet_of_the_Undertaker", "Necklace", "Treasure", 150, Effect(0, 0, 0, 0), 2000,
                                    "Necromancy +5%")
Garniture_of_Interference = Artifact("Garniture_of_Interference", "Necklace", "Major", 150, Effect(0, 0, 0, 0), 2000,
                                     "Magic resistance +5%")
Statesmans_Medal = Artifact("Statesmans_Medal", "Necklace", "Major", 300, Effect(0, 0, 0, 0), 5000,
                            "Surrending cost is reduced by 10%")
Necklace_of_Swiftness = Artifact("Necklace_of_Swiftness", "Necklace", "Treasure", 300, Effect(0, 0, 0, 0), 5000,
                                 "Unit speed +1")
Pendant_of_Courage = Artifact("Pendant_of_Courage", "Necklace", "Major", 550, Effect(0, 0, 0, 0), 7000,
                              "Luck +3 Morale +3")
Necklace_of_Dragonteeth = Artifact("Necklace_of_Dragonteeth", "Necklace", "Major", 0, Effect(0, 0, 3, 3), 6000,
                                   "Spell Power +3 Knowledge +3")
Necklace_of_Ocean_Guidance = Artifact("Necklace_of_Ocean_Guidance", "Necklace", "Major", 500, Effect(0, 0, 0, 0), 10000,
                                      "Hero sea movement +1000")
Celestial_Necklace_of_Bliss = Artifact("Celestial_Necklace_of_Bliss", "Necklace", "Relic", 650, Effect(3, 3, 3, 3),
                                       12000, "All Primary Skills +3")
Pendant_of_Downfall = Artifact("Pendant_of_Downfall", "Necklace", "Major", 200, Effect(0, 0, 0, 0), 7000,
                               "Decreases enemy's Morale by 2")
Pendant_of_Reflection = Artifact("Pendant_of_Reflection", "Combo", "Relic", 700, Effect(0, 0, 0, 0), 12000,
                                 "Increases hero's magic resistance by 20%")
# Weapon
Centaurs_Axe = Artifact("Centaurs_Axe", "Weapon", "Treasure", 200, Effect(2, 0, 0, 0), 2000, "Attack +2")
Blackshard_of_the_Dead_Knight = Artifact("Blackshard_of_the_Dead_Knight", "Weapon", "Minor", 300, Effect(3, 0, 0, 0),
                                         3000, "Attack +3")
Greater_Gnolls_Flail = Artifact("Greater_Gnolls_Flail", "Weapon", "Minor", 400, Effect(4, 0, 0, 0), 4000, "Attack +4")
Ogres_Club_of_Havoc = Artifact("Ogres_Club_of_Havoc", "Weapon", "Major", 500, Effect(5, 0, 0, 0), 5000, "Attack +5")
Sword_of_Hellfire = Artifact("Sword_of_Hellfire", "Weapon", "Major", 600, Effect(6, 0, 0, 0), 6000, "Attack +6")
Red_Dragon_Flame_Tongue = Artifact("Red_Dragon_Flame_Tongue", "Weapon", "Minor", 450, Effect(2, 2, 0, 0), 4000,
                                   "	Attack +2 Defense +2")
Titans_Gladius = Artifact("Titans_Gladius", "Weapon", "Relic", 600, Effect(12, -3, 0, 0), 10000,
                          "Attack +12 Defense -3")
Sword_of_Judgement = Artifact("Sword_of_Judgement", "Weapon", "Relic", 800, Effect(5, 5, 5, 5), 20000,
                              "All Primary Skills +5")
Titans_Thunder = Artifact("Titans_Thunder", "Combo", "Relic", 850, Effect(9, 9, 8, 8), 40000,
                          "Attack +9, Defense +9 Knowledge +8, Spell Power +8 Spell Titan's Lightning Bolt Adds a Spell Book permanently")
Angelic_Alliance = Artifact("Angelic_Alliance", "Combo", "Relic", 1000, Effect(21, 21, 21, 21), 84000,
                            "All Primary Skills +21 no Alignment penalty for units from good and neutral towns, except for Conflux Prayer in combat")
Armageddons_Blade = Artifact("Armageddons_Blade", "Weapon", "Relic", 1000, Effect(3, 3, 3, 6), 50000,
                             "Attack +3, Defense +3 Knowledge +6, Spell Power +3 Spell Armageddon expert Immune to Armageddon")
Trident_of_Dominion = Artifact("Trident_of_Dominion", "Weapon", "Major", 700, Effect(7, 0, 0, 0), 7000, "attack +7")
Ironfist_of_the_Ogre = Artifact("Ironfist_of_the_Ogre", "Combo", "Relic", 800, Effect(5, 5, 4, 4), 20000,
                                "At the beginning of a combat casts Haste, Bloodlust, Fire Shield and Counterstrike; +5 to Attack and Defense; +4 to Spell Power and Knowledge")
# Ring
Ring_of_Conjuring = Artifact("Ring_of_Conjuring", "Ring", "Treasure", 100, Effect(0, 0, 0, 0), 1000,
                             "spell duration +2")
Still_Eye_of_the_Dragon = Artifact("Still_Eye_of_the_Dragon", "Ring", "Treasure", 200, Effect(0, 0, 0, 0), 2000,
                                   "increases hero's luck and morale by +1")
Quiet_Eye_of_the_Dragon = Artifact("Quiet_Eye_of_the_Dragon", "Ring", "Treasure", 200, Effect(1, 1, 0, 0), 2000,
                                   "increases hero's attack and defense skills by +1")
Equestrians_Gloves = Artifact("Equestrians_Gloves", "Ring", "Minor", 300, Effect(0, 0, 0, 0), 3000,
                              "hero movement points +200")
Diplomats_Ring = Artifact("Diplomats_Ring", "Ring", "Major", 400, Effect(0, 0, 0, 0), 5000,
                          "reduces the cost of surrendering")
Ring_of_the_Wayfarer = Artifact("Ring_of_the_Wayfarer", "Ring", "Major", 400, Effect(0, 0, 0, 0), 5000,
                                "increases the combat speed of all hero's units by +1")
Ring_of_Vitality = Artifact("Ring_of_Vitality", "Ring", "Treasure", 500, Effect(0, 0, 0, 0), 5000,
                            "increases the health of all hero's units by +1")
Ring_of_Life = Artifact("Ring_of_Life", "Ring", "Minor", 500, Effect(0, 0, 0, 0), 5000,
                        "increases the health of all hero's units by +1")
Ring_of_Infinite_Gems = Artifact("Ring_of_Infinite_Gems", "Ring", "Major", 300, Effect(0, 0, 0, 0), 5000,
                                 "increases kingdom's gem production by +1 per day")
Eversmoking_Ring_of_Sulfur = Artifact("Eversmoking_Ring_of_Sulfur", "Ring", "Major", 300, Effect(0, 0, 0, 0), 5000,
                                      "increases your sulfur production by +1 per day")
Ring_of_the_Magi = Artifact("Ring_of_the_Magi", "Combo", "Relic", 200, Effect(0, 0, 0, 0), 3000, "spell duration +56")
Ring_of_Suppression = Artifact("Ring_of_Suppression", "Ring", "Treasure", 300, Effect(0, 0, 0, 0), 4000,
                               "decreases enemy's Morale by 1")
Ring_of_Oblivion = Artifact("Ring_of_Oblivion", "Ring", "Major", 550, Effect(0, 0, 0, 0), 7500,
                            "makes all losses in the battle irrevocable")
Seal_of_Sunset = Artifact("Seal_of_Sunset", "Ring", "Minor", 400, Effect(0, 0, 0, 0), 5000,
                          "reduces the power skill of enemy hero by 10 percent during combat")
# Torso
Breastplate_of_Petrified_Wood = Artifact("Breastplate_of_Petrified_Wood", "Torso", "Treasure", 100, Effect(0, 0, 1, 0),
                                         1000, "increases your Power skill by +1")
Rib_Cage = Artifact("Rib_Cage", "Torso", "Minor", 200, Effect(0, 0, 2, 0), 3000, "increases hero's power skill by +2")
Scales_of_the_Greater_Basilisk = Artifact("Scales_of_the_Greater_Basilisk", "Torso", "Minor", 300, Effect(0, 0, 3, 0),
                                          4000, "increases hero's power skill by +3")
Tunic_of_the_Cyclops_King = Artifact("Tunic_of_the_Cyclops_King", "Torso", "Major", 400, Effect(0, 0, 4, 0), 5000,
                                     "increases your Power skill by +4")
Breastplate_of_Brimstone = Artifact("Breastplate_of_Brimstone", "Torso", "Major", 500, Effect(0, 0, 5, 0), 6000,
                                    "increases your Power skill by +5")
Armor_of_Wonder = Artifact("Armor_of_Wonder", "Torso", "Minor", 500, Effect(1, 1, 1, 1), 4000,
                           "increases all four primary skills by +1")
Dragon_Scale_Armor = Artifact("Dragon_Scale_Armor", "Torso", "Relic", 750, Effect(4, 4, 0, 0), 8000,
                              "increases hero's attack and defense skills by +4")
Titans_Cuirass = Artifact("Titans_Cuirass", "Torso", "Relic", 650, Effect(0, 0, 10, -2), 10000,
                          "increases hero's power skill by +10, but reduces knowledge skill by -2")
Armor_of_the_Damned = Artifact("Armor_of_the_Damned", "Combo", "Relic", 800, Effect(3, 3, 2, 2), 12000,
                               "all opponents have these spells effective on them for fifty turns: slow, curse, weakness, and misfortune")
Power_of_the_Dragon_Father = Artifact("Power_of_the_Dragon_Father", "Combo", "Relic", 1000, Effect(16, 16, 16, 16),
                                      42000,
                                      "+6 to all primary skills, all troops are immune to 1-4th level spells")
Royal_Armor_of_Nix = Artifact("Royal_Armor_of_Nix", "Torso", "Major", 0, Effect(0, 0, 6, 0), 7000, "spell power +6")
Plate_of_Dying_Light = Artifact("Plate_of_Dying_Light", "Torso", "Relic", 700, Effect(0, 0, 0, 0), 10000,
                                "reduces enemy's spell power by 25 percent during combat")
