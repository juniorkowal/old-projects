"""Module containing an algorithm that states the value of entering the city"""
from hierarchyFunctions.power_evaluation import power_evaluation
from data.city import City

def full_unit_cost(town):
    """
    Gives value to the city if there are units to buy

    :param town: Town object
    :return cost: Cost of buying all units
    """
    cost = 0
    if town.creature_dwellings[1-1].lvl == 1:
        cost += town.creature_dwellings[1-1].unit_cost.gold * town.creature_dwellings[1-1].unit_ready
    if town.creature_dwellings[1-1].lvl == 2:
        cost += town.creature_dwellings[1-1].unit_cost_up.gold * town.creature_dwellings[1-1].unit_ready

    if town.creature_dwellings[2-1].lvl == 1:
        cost += town.creature_dwellings[2-1].unit_cost.gold * town.creature_dwellings[2-1].unit_ready
    if town.creature_dwellings[2-1].lvl == 2:
        cost += town.creature_dwellings[2-1].unit_cost_up.gold * town.creature_dwellings[2-1].unit_ready

    if town.creature_dwellings[3-1].lvl == 1:
        cost += town.creature_dwellings[3-1].unit_cost.gold * town.creature_dwellings[3-1].unit_ready
    if town.creature_dwellings[3-1].lvl == 2:
        cost += town.creature_dwellings[3-1].unit_cost_up.gold * town.creature_dwellings[3-1].unit_ready

    if town.creature_dwellings[4-1].lvl == 1:
        cost += town.creature_dwellings[4-1].unit_cost.gold * town.creature_dwellings[4-1].unit_ready
    if town.creature_dwellings[4-1].lvl == 2:
        cost += town.creature_dwellings[4-1].unit_cost_up.gold * town.creature_dwellings[4-1].unit_ready

    if town.creature_dwellings[5-1].lvl == 1:
        cost += town.creature_dwellings[5-1].unit_cost.gold * town.creature_dwellings[5-1].unit_ready
    if town.creature_dwellings[5-1].lvl == 2:
        cost += town.creature_dwellings[5-1].unit_cost_up.gold * town.creature_dwellings[5-1].unit_ready

    if town.creature_dwellings[6-1].lvl == 1:
        cost += town.creature_dwellings[6-1].unit_cost.gold * town.creature_dwellings[6-1].unit_ready
    if town.creature_dwellings[6-1].lvl == 2:
        cost += town.creature_dwellings[6-1].unit_cost_up.gold * town.creature_dwellings[6-1].unit_ready

    if town.creature_dwellings[7-1].lvl == 1:
        cost += town.creature_dwellings[7-1].unit_cost.gold * town.creature_dwellings[7-1].unit_ready
    if town.creature_dwellings[7-1].lvl == 2:
        cost += town.creature_dwellings[7-1].unit_cost_up.gold * town.creature_dwellings[7-1].unit_ready
    return cost

# TODO value jesli chcemy uzywac speli

#
# def new_magic(town):
#     """
#
#     :param town:
#     :return True or False:
#     """
#     if town.last_built.name == "Mage_Guild":
#         return True
#     else:
#         return False


def units_up(day):
    """
    Checks if there is a new week

    :param day: Parameter stating the day.
    :return: Boolean. True -> are up. False -> Not up.
    """
    if day == 1:
        return True
    else:
        return False


def enter_city_evaluation(arg, player, hero):
    """
    Adds value to the city

    :param arg: City to evaluate
    :param player: Player instance
    :param hero: Current hero
    :return: Value
    """

    number = 0
    if isinstance(arg, int):
        return 0

    if hero.herotype == 'main':
        return 0

    if issubclass(type(arg), City):

        if arg not in player.cities:  # Add any value to a city that isn't ours
            return 1000



    # wejscie do naszego miasta
    if arg in player.cities and hero.herotype != 'main':
        number = (arg.creature_dwellings[1-1].unit_type.value * arg.creature_dwellings[1-1].unit_ready +
                  arg.creature_dwellings[2-1].unit_type.value * arg.creature_dwellings[2-1].unit_ready +
                  arg.creature_dwellings[3-1].unit_type.value * arg.creature_dwellings[3-1].unit_ready +
                  arg.creature_dwellings[4-1].unit_type.value * arg.creature_dwellings[4-1].unit_ready +
                  arg.creature_dwellings[5-1].unit_type.value * arg.creature_dwellings[5-1].unit_ready +
                  arg.creature_dwellings[6-1].unit_type.value * arg.creature_dwellings[6-1].unit_ready +
                  arg.creature_dwellings[7-1].unit_type.value * arg.creature_dwellings[7-1].unit_ready)
        try:
            if player.gold/full_unit_cost(player.cities[0]) >= 1:
                number = number * 1
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.9:
                number = number * 0.9
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.8:
                number = number * 0.8
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.7:
                number = number * 0.7
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.6:
                number = number * 0.6
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.5:
                number = number * 0.5
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.4:
                number = number * 0.4
            else:
                number = 0
        except ZeroDivisionError:
            number = 0
    else:
        number = 0

        # if new_magic(player.cities[0]):
        #     number = number + 400
        # else:
        #     pass

        #wejscie do Neutral / Enemy
        # else:
        #     #TODO dodac miastu Slots
        #     zmienna = power_evaluation(player.heroes, arg.slots)
        #
        #     if zmienna == 1:
        #         number = number + 400
        #     else:
        #         number = number - 5000000
    number = number * 3

    if player.gold > 15000:
        return number * 2
    else:
        return number

