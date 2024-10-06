"""Script containing algorithms stating values for other factors in the game e.g. campfire"""
from data.hero import Hero
import data.classes_const as units
from data.player_data import Player


def resource_on_click(tile, hero: Hero):
    """
    Give value to building that give resources on click

    :param tile:
    :param hero:
    """

    if type(tile).__name__ != "RescourcesOnClick":
        return 0

    else:
        if hero.herotype == 'main':
            return 200
        else:
            return 700


def increase_skills(tile, hero: Hero):
    """
    Give value to buildings that increase skills

    :param tile: Given tile
    :param hero: Current hero
    :return: value to be added to overall value
    """
    if type(tile).__name__ != "Increase_Skill":
        return 0
    hero_type = hero.herotype
    hero_class = hero.heroclass
    scaling = 100
    if hero_class == "might":
        might_scalar = 2
        magic_scalar = 1
    else:
        might_scalar = 1
        magic_scalar = 2

    if hero_type == 'main':
        skill_want = 10
    else:
        skill_want = 1
    if tile.name in ['Arena', 'Library_of_Enlightenment', 'Marletto_Tower', 'Mercenary_Camp', 'School_of_War']:
        value = scaling * might_scalar * skill_want
    else:
        value = scaling * magic_scalar * skill_want

    if tile.name == 'Library_of_Enlightenment' and hero.lvl < 10:
        return -10000

    return value


def luck_morale(tile, hero):
    """
    Add value to objects that give luck and morale

    :param tile: Given tile
    :param hero: Current hero
    :return: value to be added to overall value
    """
    if type(tile).__name__ != "LuckMorale":
        return 0
    scaling = 5
    if hero.lvl > 15:
        scaling = 10
    if hero.lvl > 20:
        scaling = 20
    value = 0
    if hero.herotype == 'main':
        value += 10*scaling

    return value


def mp(tile, hero: Hero):
    """
    Add value to objects that give movement points

    :param tile: Given tile
    :param hero: Current hero
    :return: value to be added to overall value
    """
    if type(tile).__name__ != "Mp":
        return 0
    value = 0
    scale = 20
    slots = hero.slots.slots
    are_cavaliers = False
    for slot in slots:
        if slot.unit == units.Cavalier:
            are_cavaliers = True

    if tile.name == "Stables" and are_cavaliers:  # Cavaliers are upgraded for free to a better unit
        value += 1000
    elif tile.name == "Stables":
        value += 500
    else:
        value = scale*10
    return value


def disappear_on_click(tile, hero: Hero, player: Player):
    """
    Add value to objects that disappear on click

    :param tile: Given tile
    :param hero: Current hero
    :param player: Player instance
    :return: value to be added to overall value
    """
    if type(tile).__name__ != "DissapearOnClick":
        return 0
    value = 0
    if tile.name == "Campfire":
        if player.gold < 2000:
            value += 200
        else:
            value += 100
    if tile.name == "Scholar":
        if hero.herotype == 'main':
            value += 1000
        else:
            value += 500
    if tile.name == "Treasure_Chest":
        if hero.herotype == 'main' and hero.lvl < 15:
            value += 2000
        elif hero.herotype == 'main':
            value += 500
        else:
            value += 1000
    if tile.name == "Wagon":
        if hero.herotype == 'main':
            value -= 200
        else:
            value += 300
    return value


def the_rest(tile, hero: Hero):
    """
    Add value to all the objects that don't fit in other descriptions

    :param tile: Given tile
    :param hero: Current hero
    :return: value to be added to overall value
    """
    value = 0
    if type(tile).__name__ != "ObjectOnMap":
        return 0
    if tile.name == "Black_Market":
        return -10000
    elif tile.name == "Freelancers_Guild":
        return -10000

    elif tile.name == 'Learning_Stone':
        if hero.lvl > 20:
            value += 100
        elif hero.lvl > 15:
            value += 300
        elif hero.lvl > 10:
            value += 500
        else:
            value += 1000

    elif tile.name == 'Magic_Well':
        if hero.herotype != 'main':
            value += 0
        elif hero.manapoint < hero.knowledge * 5:
            value += 500
        elif hero.manapoint == hero.knowledge * 10:
            value += 0
        else:
            value += 100

    elif tile.name == 'Redwood_Observatory':
        pass  # implement later

    elif tile.name == 'Shrine_Of_Magic_Incantation' or tile.name == 'Shrine_Of_Magic_Gesture':
        if hero.spellbook.spells:
            value += 500
        else:
            value -= 1000

    elif tile.name == 'Shrine_Of_Magic_Thought':
        has_wisdom = False
        for skill in hero.skills.secondary_skills:
            if skill.name == 'Wisdom' and skill.lvl >= 1:
                has_wisdom = True
        if has_wisdom:
            value += 1000
        else:
            value -= 100000

    elif tile.name == 'Shrine_Of_Magic_Mystery':
        has_wisdom = False
        for skill in hero.skills.secondary_skills:
            if skill.name == 'Wisdom' and skill.lvl >= 2:
                has_wisdom = True
        if has_wisdom:
            value += 1000
        else:
            value -= 100000

    elif tile.name == 'Trading_Post':
        value -= 10000

    elif tile.name == 'Tree_Of_Knowledge':
        if hero.herotype == 'main':
            value += 2000
        else:
            value -= 2500

    elif tile.name == 'Witch_Hut':
        if hero.herotype != 'main':
            value += 500
        else:
            value -= 500

    elif tile.name == 'Windmill':
        if hero.herotype != 'main':
            value += 500
        else:
            value -= 500

    elif tile.name == 'Den_of_thieves':
        value -= 100000

    elif tile.name == 'War_Machine_Factory':
        value -= 10000

    elif tile.name in ['Portal_Two_Way',"Portal_One_Way_Exit","Portal_One_Way_Entrance","Monolith_Two_Way"
                       "Monolith_One_Way_Exit","Monolith_One_Way_Entrance"]:
        value -= 10000

    return value


# def fog_of_war_null(tile):
#     """
#     Make it so that fog of war has very small value
#
#     :param tile:
#     :return:
#     """
#     value = 0
#     if type(tile) == FogOfWar:
#         value = -1000000
#     return value

