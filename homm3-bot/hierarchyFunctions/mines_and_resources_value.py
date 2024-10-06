"""Script containing algorithms that state value for mine and mine-like objects in the game"""
from data.objects_on_map import Mine
from data.player_data import Player


def increase_mines_ratio(player_cities: list):
    """
    Increase value given based on mines

    :param player_cities: List of player's cities
    :return: Ratios for all towns (10 parameters)
    """
    Castle_ratio = 1
    Rampart_ratio = 1
    Tower_ratio = 1
    Inferno_ratio = 1
    Necropolis_ratio = 1
    Dungeon_ratio = 1
    Stronghold_ratio = 1
    Fortress_ratio = 1
    Conflux_ratio = 1
    Cove_ratio = 1
    for town in player_cities:
        if town.name == "Castle":
            Castle_ratio += 0.5
        if town.name == "Rampart":
            Rampart_ratio += 0.5
        if town.name == "Tower":
            Tower_ratio += 0.5
        if town.name == "Inferno":
            Inferno_ratio += 0.5
        if town.name == "Necropolis":
            Necropolis_ratio += 0.5
        if town.name == "Dungeon":
            Dungeon_ratio += 0.5
        if town.name == "Stronghold":
            Stronghold_ratio += 0.5
        if town.name == "Fortress":
            Fortress_ratio += 0.5
        if town.name == "Conflux":
            Conflux_ratio += 0.5
        if town.name == "Cove":
            Cove_ratio += 0.5
    return Castle_ratio, Rampart_ratio, Tower_ratio, Inferno_ratio, Necropolis_ratio, Dungeon_ratio, Stronghold_ratio, Fortress_ratio, Conflux_ratio, Cove_ratio


def cut_value(value, index, player):
    """
    Cut value based on resources we already own

    :param value: Value parameter
    :param index: Index of the resource
    :param player: Player object
    :return: Value
    """
    if index == 1:
        if player.wood > 60:
            value = value / 8
        elif player.wood > 40:
            value = value / 3
        else:
            return value
    elif index == 2:
        if player.ore > 60:
            value = value / 8
        elif player.ore > 40:
            value = value / 3
        else:
            return value
    elif index == 3:
        if player.mercury > 30:
            value = value / 4
        elif player.mercury > 20:
            value = value / 2
        else:
            return value
    elif index == 4:
        if player.sulfur > 30:
            value = value / 4
        elif player.sulfur > 20:
            value = value / 2
        else:
            return value
    elif index == 5:
        if player.crystal > 30:
            value = value / 4
        elif player.crystal > 20:
            value = value / 2
        else:
            return value
    elif index == 6:
        if player.gems > 30:
            value = value / 4
        elif player.gems > 20:
            value = value / 2
        else:
            return value
    return value


def mineCase(tile, player):
    """
    Add value to mines

    :param tile: parameter associated with checking the name of said tile in order to recognize what object is on that
    tile
    :param player: Player object
    :return: Value
    """
    if type(tile).__name__ == "Mine":
        Castle_ratio, Rampart_ratio, Tower_ratio, Inferno_ratio, Necropolis_ratio, Dungeon_ratio, Stronghold_ratio, Fortress_ratio, Conflux_ratio, Cove_ratio = increase_mines_ratio(
            player.cities)
        value = 1000

        if tile.captured:  # If the mine is ours, economically its non-sens to go there
            return -5000000
        else:
            if tile.name == "Sawmill":
                value = value * Castle_ratio * Stronghold_ratio * Fortress_ratio * Cove_ratio
                value = cut_value(value, 1, player)
                if player.week < 2:
                    value = value * 2
            elif tile.name == "Ore_Pit":
                value = value * Rampart_ratio * Tower_ratio * Inferno_ratio * Necropolis_ratio * Dungeon_ratio * Stronghold_ratio * Conflux_ratio
                value = cut_value(value, 2, player)
                if player.week < 2:
                    value = value * 2
            elif tile.name == "Crystal_Cavern":
                value = value * Rampart_ratio * Stronghold_ratio
                value = cut_value(value, 5, player)
            elif tile.name == "Gem_Pond":
                value = value * Castle_ratio * Tower_ratio
                value = cut_value(value, 6, player)
            elif tile.name == "Alchemists_Lab":
                value = value * Inferno_ratio * Necropolis_ratio * Conflux_ratio
                value = cut_value(value, 3, player)
            elif tile.name == "Sulfur_Dune":
                value = value * Dungeon_ratio * Fortress_ratio * Cove_ratio
                value = cut_value(value, 4, player)
            elif tile.name == "Gold_Mine":
                if player.gold < 10000:
                    value = value * 5
                value = value * Castle_ratio * Rampart_ratio * Tower_ratio * Inferno_ratio * Necropolis_ratio * Dungeon_ratio * Stronghold_ratio * Fortress_ratio * Conflux_ratio * Cove_ratio * 1.5
            elif tile.name == "Abandoned_Mine":
                value = value * 1.1
            return value
    else:
        return 0


def increase_resource_value(tile, value, player_cities):
    """
    Increase resource value based on owned towns

    :param tile: Parameter associated with checking the name of said tile in order to recognize what object is on that tile
    :param value: Value parameter
    :param player_cities: List of player cities
    :return: Value
    """
    for town in player_cities:
        if town.name == "Castle":
            value = value * 1.5
        if town.name == "Rampart":
            value = value * 1.5
        if town.name == "Tower":
            value = value * 1.5
        if town.name == "Inferno":
            value = value * 1.5
        if town.name == "Necropolis":
            value = value * 1.5
        if town.name == "Dungeon":
            value = value * 1.5
        if town.name == "Stronghold":
            value = value * 1.5
        if town.name == "Fortress":
            value = value * 1.5
        if town.name == "Conflux":
            value = value * 1.5
        if town.name == "Cove":
            value = value * 1.5
    return value


def cut_resource_value(tile, value, player):
    """
    Cut resource value based on owned resources

    :param tile: Parameter associated with checking the name of said tile in order to recognize what object is on that tile
    :param value: Value parameter
    :param player: Class Player
    :return: Value
    """
    if tile.name == "Wood":
        if player.wood > 60:
            value = value // 4
        elif player.wood > 40:
            value = value // 2
        else:
            pass
    if tile.name == "Ore":
        if player.ore > 60:
            value = value // 4
        elif player.ore > 40:
            value = value // 2
        else:
            pass
    if tile.name == "Mercury":
        if player.mercury > 40:
            value = value // 4
        elif player.mercury > 30:
            value = value // 2
        else:
            pass
    if tile.name == "Sulfur":
        if player.sulfur > 40:
            value = value // 4
        elif player.sulfur > 30:
            value = value // 2
        else:
            pass
    if tile.name == "Crystal":
        if player.crystal > 40:
            value = value // 4
        elif player.crystal > 30:
            value = value // 2
        else:
            pass
    if tile.name == "Gems":
        if player.gems > 40:
            value = value // 4
        elif player.gems > 30:
            value = value // 2
        else:
            pass

    return value


def resourceStackCase(tile, player, hero):
    """
    Give value to resources freely lying on the adventure map

    :param tile: Parameter associated with checking the name of said tile in order to recognize what object is on that tile
    :param player: Player object
    :param hero: Hero object
    :return: Value
    """
    value = 0
    if hero.herotype == "main":
        if type(tile).__name__ == "Resource":
            value = 0
            value = increase_resource_value(tile, value, player.cities)
            value = cut_resource_value(tile, value, player)
        else:
            return 0
        return value
    else:
        if type(tile).__name__ == "Resource":
            value = 1000
            value = increase_resource_value(tile, value, player.cities)
            if player.week < 2:
                value = value * 2
            if tile.name == "Gold":
                value = value * 4
        else:
            return 0
        return value


if __name__ == "__main__":
    player = Player('red', 1000, 120, 120, 110, 110, 110, 110)
    Gold_Mine = Mine(3500, "Gold_Mine")
    v = mineCase(Gold_Mine, player)
    print(v)

