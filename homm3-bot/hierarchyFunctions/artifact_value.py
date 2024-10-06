"""Module responsible for calculating the value of artifacts on the adventure map"""
from data.Artifacts import Artifact
from data.hero import Hero


def artifact_value(field: Artifact, hero: Hero):
    """
    Assigns value to artifacts. Values can land in between 0-5k

    :param field: found Artifact
    :param hero: our Hero
    :return: value
    """
    value = 0
    multiplier = 10

    if type(field) != Artifact:
        return 0

    value += (gold_tier_value(field, multiplier) +
              necromancy_check(field, hero, multiplier) +
              heavy_hitters(field, hero, multiplier) +
              ranged_units_bonus(field, hero, multiplier/10))

    # Spells aren't used so value of items that add knowledge and spell power aren't as valuable
    if (field.effect.knowledge or field.effect.spell_power) and 'spell' in field.bonus.lower():
        value /= 2

    return int(value)


def gold_tier_value(item, mult):
    """
    Adds value based on based value of the artifact, its value in gold and its tier

    :param item: Artifact found
    :param mult: value multiplier
    :return: value
    """
    item_class = ['Scroll', 'Treasure', 'Minor', 'Major', 'Relic']
    tier = item_class.index(item.Class)
    return 10*mult*tier+item.val+int(item.cost/10)


def necromancy_check(item, hero, mult):
    """
    Adds value to necromancy artifacts if our hero has necromancy

    :param item: Artifact found
    :param hero: Our hero
    :param mult: Value multiplier
    :return: value
    """
    if hero.herotype != 'Necromancer' and hero.herotype != 'Death_Knight':
        return 0
    else:
        if 'necromancy' in item.bonus.lower():
            return 50*mult
        else:
            return 0


def heavy_hitters(item, hero, mult):
    """
    Adds additional value to strength artifacts if the hero focuses on strength

    :param item: artifact found
    :param hero: our hero
    :param mult: value multiplier
    :return: value
    """
    if hero.attack >= hero.defense+2:
        return 5*mult*item.effect.attack
    else:
        return 0


def check_for_archery(hero):
    """
    Checks if our hero has the archery skill

    :param hero: our hero
    :return: True/False
    """
    for skill in hero.skills.secondary_skills:
        if 'archery' in skill.name.lower():
            return True


def ranged_units_bonus(item, hero, mult):
    """
    Sets additional value for artifacts that give bonuses to ranged fight

    :param item: Artifact found
    :param hero: Our hero
    :param mult: Value multiplier
    :return: Additional value
    """
    ranged_value = 0
    ranged_amount = 0

    if 'bow' in item.name.lower() or 'ranged' in item.bonus.lower() or 'archery' in item.bonus.lower():
        for s in hero.slots.slots:
            if s.unit.ammo:
                ranged_value += s.unit.value
                ranged_amount += 1
        
        if ranged_amount > 4:
            return ranged_value*mult
        else:
            return 0
    else:
        return 0
