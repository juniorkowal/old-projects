"""Script containing Conflux castle upgrade algorithm"""
from town_upgrading.choice_generator import town_choice, full_unit_cost
from GUI_handling.TownGUI import buy_building
from data.building import Cost
from data.player_data import Player


def resourceCheck(buildingCost: Cost, player: Player):
    """
    Checks if a player has enough resources to build.
    :param buildingCost: Cost of the given building
    :param player: Resources of the player
    :return: true or false
    """
    if (player.gold >= buildingCost.gold) and (player.wood >= buildingCost.wood) and (
            player.ore >= buildingCost.ore) and (player.mercury >= buildingCost.mercury) and (
            player.sulfur >= buildingCost.sulfur) and (player.crystal >= buildingCost.crystal) and (
            player.gems >= buildingCost.gems):
        return True
    else:
        return False


def build(buildingCost: Cost, player: Player):
    """
    Functions responsible for building and managing resources after construction
    :param buildingCost: Cost of the given building
    :param player: Resources of the player
    """
    player.gold -= buildingCost.gold
    player.wood -= buildingCost.wood
    player.ore -= buildingCost.ore
    player.mercury -= buildingCost.mercury
    player.sulfur -= buildingCost.sulfur
    player.crystal -= buildingCost.crystal
    player.gems -= buildingCost.gems


def confluxUpgrade(player: Player, city):
    """
    Conflux castle upgrade algorithm.
    :param player: Player object
    :param city: Conflux object
    :return: None
    """
    cost = full_unit_cost(city)
    if player.gold < (cost/3):
        print("Not enough gold for units, don't build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if not city.tavern.built:
        if resourceCheck(city.tavern.cost[0], player):
            build(city.tavern.cost[0], player)
            city.tavern.built = True
            buy_building(city.tavern.name, "conflux")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort                            <our rule>
    if city.fort.lvl == 0 and city.tavern.built:
        if resourceCheck(city.fort.cost[0][0], player):
            build(city.fort.cost[0][0], player)
            city.fort.lvl = 1
            buy_building(city.fort.name, "conflux")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Magic Lantern
    if city.creature_dwellings[1-1].lvl == 0 and city.fort.lvl >= 1:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][0], player):
            build(city.creature_dwellings[1-1].cost[0][0], player)
            city.creature_dwellings[1-1].lvl = 1
            buy_building(city.creature_dwellings[1-1].name, "conflux")
            print('Magic Lantern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Mage Guild Level 1                       <our rule>
    if city.mage_guild.lvl == 0 and city.creature_dwellings[1-1].lvl >= 1:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            city.mage_guild.lvl = 1
            buy_building(city.mage_guild.name, "conflux")
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Altar of Air
    if city.creature_dwellings[2-1].lvl == 0 and city.mage_guild.lvl >= 1 and city.creature_dwellings[1-1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][0], player):
            build(city.creature_dwellings[2-1].cost[0][0], player)
            city.creature_dwellings[2-1].lvl = 1
            buy_building(city.creature_dwellings[2-1].name, "conflux")
            print('Altair of Air built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Altar of Water
    if city.creature_dwellings[3-1].lvl == 0 and city.mage_guild.lvl >= 1 and city.creature_dwellings[1-1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][0], player):
            build(city.creature_dwellings[3-1].cost[0][0], player)
            city.creature_dwellings[3-1].lvl = 1
            buy_building(city.creature_dwellings[3-1].name, "conflux")
            print('Altar of Water built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Town Hall                                      <our rule>
    if city.city_hall.lvl == 0 and city.mage_guild.lvl >= 1 and city.tavern.built:
        if resourceCheck(city.city_hall.cost[0][0], player):
            build(city.city_hall.cost[0][0], player)
            city.city_hall.lvl = 1
            buy_building(city.city_hall.name, "conflux")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Citadel                             <our rule>
    if city.fort.lvl == 1 and city.city_hall.lvl >= 1:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            city.fort.lvl = 2
            buy_building(city.fort.name, "conflux")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------
    # 9 Altar of Fire
    if city.creature_dwellings[4-1].lvl == 0 and city.creature_dwellings[2-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            city.creature_dwellings[4-1].lvl = 1
            buy_building(city.creature_dwellings[4-1].name, "conflux")
            print('Altar of Fire built!')
            return None
        else:
            print('Not enough resources!')

    # 10 Marketplace
    if not city.marketplace.built and MG_M:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            city.marketplace.built = True
            buy_building(city.marketplace.name, "conflux")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 11 Blacksmith
    if not city.blacksmith.built and MG_M:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            city.blacksmith.built = True
            buy_building(city.blacksmith.name, "conflux")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 12 City Hall
    if city.city_hall.lvl == 1 and city.blacksmith.built and city.mage_guild.lvl >= 1 and city.marketplace.built and capi:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            city.city_hall.lvl = 2
            buy_building(city.city_hall.name, "conflux")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Upg. Altar of Water
    if city.creature_dwellings[3-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][1], player):
            build(city.creature_dwellings[3-1].cost[0][1], player)
            city.creature_dwellings[3-1].lvl = 2
            buy_building(city.creature_dwellings[3-1].name, "conflux")
            print('Altar of Water upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 14 Garden of Life
    if not city.garden_of_life.built and city.creature_dwellings[1-1].lvl >= 1 and builds:
        if resourceCheck(city.garden_of_life.cost[0], player):
            build(city.garden_of_life.cost[0], player)
            city.garden_of_life.built = True
            buy_building(city.garden_of_life.name, "conflux")
            print("Garden of Life built!")
            return None
        else:
            print('Not enough resources!')

    # 15 Mage Guild Level 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            city.mage_guild.lvl = 2
            buy_building(city.mage_guild.name, "conflux")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if city.fort.lvl == 2 and wall:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            city.fort.lvl = 3
            buy_building(city.fort.name, "conflux")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Capitol
    if city.fort.lvl >= 3 and city.city_hall.lvl == 2 and capi:
        if resourceCheck(city.city_hall.cost[0][2], player):
            build(city.city_hall.cost[0][2], player)
            city.city_hall.lvl = 3
            buy_building(city.city_hall.name, "conflux")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Altar of Earth
    if city.creature_dwellings[5-1].lvl == 0 and city.creature_dwellings[3-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][0], player):
            build(city.creature_dwellings[5-1].cost[0][0], player)
            city.creature_dwellings[5-1].lvl = 1
            buy_building(city.creature_dwellings[5-1].name, "conflux")
            print('Altar of Earth built!')
            return None
        else:
            print('Not enough resources!')

    # 19 Upg. Altar of Air
    if city.creature_dwellings[2-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][1], player):
            build(city.creature_dwellings[2-1].cost[0][1], player)
            city.creature_dwellings[2-1].lvl = 2
            buy_building(city.creature_dwellings[2-1].name, "conflux")
            print('Altar of Air upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 20 Upg. Magic Lantern
    if city.creature_dwellings[1-1].lvl == 1 and city.magic_university.built and upg:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][1], player):
            build(city.creature_dwellings[1-1].cost[0][1], player)
            city.creature_dwellings[1-1].lvl = 2
            buy_building(city.creature_dwellings[1-1].name, "conflux")
            print('Magic Lantern upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 21 Upg. Altar of Fire
    if city.creature_dwellings[4-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][1], player):
            build(city.creature_dwellings[4-1].cost[0][1], player)
            city.creature_dwellings[4-1].lvl = 2
            buy_building(city.creature_dwellings[4-1].name, "conflux")
            print('Altar of Fire Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 22 Mage Guild Level 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            city.mage_guild.lvl = 3
            buy_building(city.mage_guild.name, "conflux")
            print('Mage Guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 23 Altar of Thought
    if city.creature_dwellings[6-1].lvl == 0 and city.creature_dwellings[5-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][0], player)
            city.creature_dwellings[6-1].lvl = 1
            buy_building(city.creature_dwellings[6-1].name, "conflux")
            print('Altar of Thought built!')
            return None
        else:
            print('Not enough resources!')

    # 24 Magic University
    if not city.magic_university.built and city.mage_guild.lvl >= 1 and builds:
        if resourceCheck(city.magic_university.cost[0], player):
            build(city.magic_university.cost[0], player)
            city.magic_university.built = True
            buy_building(city.magic_university.name, "conflux")
            print("Magic University built!")
            return None
        else:
            print('Not enough resources!')

    # 25 Upg. Altar of Earth
    if city.creature_dwellings[5-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][1], player):
            build(city.creature_dwellings[5-1].cost[0][1], player)
            city.creature_dwellings[5-1].lvl = 2
            buy_building(city.creature_dwellings[5-1].name, "conflux")
            print('CAltar of Earth upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 26 Resource Silo
    if not city.resource_silo.built and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            city.resource_silo.built = True
            buy_building(city.resource_silo.name, "conflux")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 27 Pyre
    if city.creature_dwellings[7-1].lvl == 0 and city.creature_dwellings[6-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][0], player):
            build(city.creature_dwellings[7-1].cost[0][0], player)
            city.creature_dwellings[7-1].lvl = 1
            buy_building(city.creature_dwellings[7-1].name, "conflux")
            print('Pyre built!')
            return None
        else:
            print('Not enough resources!')

    # 28 Mage Guild Level 4
    if city.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][3], player):
            build(city.mage_guild.cost[0][3], player)
            city.mage_guild.lvl = 4
            buy_building(city.mage_guild.name, "conflux")
            print("Mage Guild Level 4!")
            return None
        else:
            print('Not enough resources!')

    # 29 Mage Guild Level 5
    if city.mage_guild.lvl == 4 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][4], player):
            build(city.mage_guild.cost[0][4], player)
            city.mage_guild.lvl = 5
            buy_building(city.mage_guild.name, "conflux")
            print("Mage Guild Level 5!")
            return None
        else:
            print('Not enough resources!')

    # 30 Upg. Altar of Thought
    if city.creature_dwellings[6-1].lvl == 1 and city.mage_guild.lvl >= 2 and upg:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][1], player):
            build(city.creature_dwellings[6-1].cost[0][1], player)
            city.creature_dwellings[6-1].lvl = 2
            buy_building(city.creature_dwellings[6-1].name, "conflux")
            print('Altar of Thought upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 31 Upg. Pyre
    if city.creature_dwellings[7-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][1], player):
            build(city.creature_dwellings[7-1].cost[0][1], player)
            city.creature_dwellings[7-1].lvl = 2
            buy_building(city.creature_dwellings[7-1].name, "conflux")
            print('Pyre upgraded!')
            return None
        else:
            print('Not enough resources!')
