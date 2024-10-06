"""Script containing value of habitats on map and value of given units"""
from data.habitats_on_map import Habitat_On_Map
from data.hero import Hero
from hierarchyFunctions.power_evaluation import power_evaluation


def habitat_on_map_units_value(habitat_building: Habitat_On_Map):
    """
    Internal function

    :param habitat_building: Habitat building object
    :return: Value
    """
    value = habitat_building.unit.value * habitat_building.number_of_units
    return value


def habitat_on_map_value(habitat_building: Habitat_On_Map, hero: Hero, player):
    """
    Adds value to habitats on the adventure map

    :param habitat_building: Habitat building object
    :param hero: Hero object
    :return: Value
    """
    value = 0
    if type(habitat_building) is Habitat_On_Map:
        if hero.herotype == 'main':
            value = power_evaluation(hero, habitat_building.guards) * habitat_on_map_units_value(habitat_building)
            return value
        else:
            if player.week > 3 or player.month > 1:
                value = power_evaluation(hero, habitat_building.guards) * habitat_on_map_units_value(habitat_building)
            else:
                value = -20000
    return value
