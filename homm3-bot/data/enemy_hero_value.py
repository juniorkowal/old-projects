"""Script containing function that calculates enemy hero value"""
from hierarchyFunctions.power_evaluation import creatures_power
from data.hero import Hero

def enemy_hero_value(enemyHero: Hero):
    """
    Function calculating enemy hero object

    :param enemyHero: enemy Hero object
    :return: value
    """
    value = creatures_power(enemyHero.slots)
    return value