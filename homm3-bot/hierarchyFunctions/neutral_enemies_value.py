"""Script containing algorithms stating value for neutral enemies"""
from hierarchyFunctions.power_evaluation import power_evaluation, creature_power, hero_power
from data.hero import Slot, Hero


def neutral_enemies_value(hero: Hero, enemies):
    """
    Adds value to enemies standing free

    :param hero: Current hero
    :param enemies: Enemy troops
    :param coords: Coordinates of enemy troops
    :param mapObj: Adventure map
    :return: value to be added to overall value
    """
    value = 0
    if isinstance(enemies, Slot):
        battle_win = power_evaluation(hero, enemies)
        value += creature_power(enemies) * battle_win
    elif isinstance(enemies, Hero):
        battle_win = power_evaluation(hero, enemies)
        value += hero_power(enemies) * battle_win
        value += 10000 * battle_win

    return value

