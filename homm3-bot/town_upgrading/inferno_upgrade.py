"""Script containing Inferno castle upgrade algorithm"""
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


def infernoUpgrade(player, city):
    """
    Inferno castle upgrade algorithm.
    :param player: player object
    :param city: Inferno object
    :return: None
    """
    cost = full_unit_cost(city)
    if player.gold < (cost/3):
        print("Not enough gold for units, don't build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # Tavern
    if not city.tavern.built:
        if resourceCheck(city.tavern.cost[0], player):
            build(city.tavern.cost[0], player)
            city.tavern.built = True
            buy_building(city.tavern.name, "inferno")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Fort
    if city.fort.lvl == 0 and city.tavern.built:
        if resourceCheck(city.fort.cost[0][0], player):
            build(city.fort.cost[0][0], player)
            city.fort.built = True
            city.fort.lvl = 1
            buy_building(city.fort.name, "inferno")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Imp Crucible
    if city.creature_dwellings[1-1].lvl == 0 and city.fort.lvl > 0:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][0], player):
            build(city.creature_dwellings[1-1].cost[0][0], player)
            city.creature_dwellings[1-1].lvl = 1
            buy_building(city.creature_dwellings[1-1].name, "inferno")
            print('Imp crucible built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Hall of Sins
    if city.creature_dwellings[2-1].lvl == 0 and city.creature_dwellings[1-1].built >= 1:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][0], player):
            build(city.creature_dwellings[2-1].cost[0][0], player)
            city.creature_dwellings[2-1].lvl = 1
            buy_building(city.creature_dwellings[2-1].name, "inferno")
            print('Hall of sins built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Town Hall
    if city.tavern.built and city.creature_dwellings[2-1].lvl >= 1 and city.city_hall.lvl == 0:
        if resourceCheck(city.city_hall.cost[0][0], player):
            build(city.city_hall.cost[0][0], player)
            city.city_hall.lvl = 1
            player.daily_income[0] += 500
            buy_building(city.city_hall.name, "inferno")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Citadel
    if city.fort.lvl == 1 and city.city_hall.lvl >= 1:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            city.fort.lvl = 2
            buy_building(city.fort.name, "inferno")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Kennels
    if city.creature_dwellings[3-1].lvl == 0 and city.fort.lvl >= 2:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][0], player):
            build(city.creature_dwellings[3-1].cost[0][0], player)
            city.creature_dwellings[3-1].lvl = 1
            buy_building(city.creature_dwellings[3-1].name, "inferno")
            print('Kennels built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Mage Guild Level 1
    if city.mage_guild.lvl == 0 and city.creature_dwellings[3-1].lvl >= 1:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            city.mage_guild.lvl = 1
            buy_building(city.mage_guild.name, "inferno")
            print('Mage Guild Level 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------
    # Blacksmith
    if not city.blacksmith.built and MG_M:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            city.blacksmith.built = True
            buy_building(city.blacksmith.name, "inferno")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # Marketplace
    if not city.marketplace.built and MG_M:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            city.marketplace.built = True
            buy_building(city.marketplace.name, "inferno")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # City Hall
    if city.city_hall.lvl == 1 and city.marketplace.built and city.blacksmith.built and city.mage_guild.lvl >= 1 and capi:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            city.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(city.city_hall.name, "inferno")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Demon Gate
    if city.creature_dwellings[4-1].lvl == 0 and city.creature_dwellings[2-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            city.creature_dwellings[4-1].lvl = 1
            buy_building(city.creature_dwellings[4-1].name, "inferno")
            print('Demon Gate built!')
            return None
        else:
            print('Not enough resources!')

    # Hell Hole
    if city.creature_dwellings[5-1].lvl == 0 and city.creature_dwellings[4-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][0], player):
            build(city.creature_dwellings[5-1].cost[0][0], player)
            city.creature_dwellings[5-1].lvl = 1
            buy_building(city.creature_dwellings[5-1].name, "inferno")
            print('Hell Hole built!')
            return None
        else:
            print('Not enough resources!')

    # Castle
    if city.fort.lvl == 2 and wall:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            city.fort.lvl = 3
            buy_building(city.fort.name, "inferno")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # Capitol
    if city.fort.lvl == 3 and city.city_hall.lvl == 2 and capi:
        if resourceCheck(city.city_hall.cost[0][2], player):
            build(city.city_hall.cost[0][2], player)
            city.city_hall.lvl = 3
            player.daily_income[0] += 2000
            buy_building(city.city_hall.name, "inferno")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Imp crucible
    if city.creature_dwellings[1-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][1], player):
            build(city.creature_dwellings[1-1].cost[0][1], player)
            city.creature_dwellings[1-1].lvl = 2
            buy_building(city.creature_dwellings[1-1].name, "inferno")
            print('Imp crucible upgraded !')
            return None
        else:
            print('Not enough resources!')

    # Upg. Kennels
    if city.creature_dwellings[3-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][1], player):
            build(city.creature_dwellings[3-1].cost[0][1], player)
            city.creature_dwellings[3-1].lvl = 2
            buy_building(city.creature_dwellings[3-1].name, "inferno")
            print('Kennels upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Hall of sins
    if city.creature_dwellings[2-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][1], player):
            build(city.creature_dwellings[2-1].cost[0][1], player)
            city.creature_dwellings[2-1].lvl = 2
            buy_building(city.creature_dwellings[2-1].name, "inferno")
            print('Hall of sins upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Demon gate
    if city.creature_dwellings[4-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][1], player):
            build(city.creature_dwellings[4-1].cost[0][1], player)
            city.creature_dwellings[4-1].lvl = 2
            buy_building(city.creature_dwellings[4-1].name, "inferno")
            print('Demon gate upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            city.mage_guild.lvl = 2
            buy_building(city.mage_guild.name, "inferno")
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            city.mage_guild.lvl = 3
            buy_building(city.mage_guild.name, "inferno")
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # Fire Lake
    if city.mage_guild.lvl >= 1 and city.creature_dwellings[4-1].lvl >= 1 and city.creature_dwellings[6-1].lvl == 0 and hab:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][0], player)
            city.creature_dwellings[6-1].lvl = 1
            buy_building(city.creature_dwellings[6-1].name, "inferno")
            print('Fire Lake built!')
            return None
        else:
            print('Not enough resources!')

    # Forsaken Palace
    if city.creature_dwellings[6-1].lvl >= 1 and city.creature_dwellings[7-1].lvl == 0 and city.creature_dwellings[5-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][0], player):
            build(city.creature_dwellings[7-1].cost[0][0], player)
            city.creature_dwellings[7-1].lvl = 1
            buy_building(city.creature_dwellings[7-1].name, "inferno")
            print('Forsaken Palace built!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 4
    if city.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][3], player):
            build(city.mage_guild.cost[0][3], player)
            city.mage_guild.lvl = 4
            buy_building(city.mage_guild.name, "inferno")
            print('Mage guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 5
    if city.mage_guild.lvl == 4 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][4], player):
            build(city.mage_guild.cost[0][4], player)
            city.mage_guild.lvl = 5
            buy_building(city.mage_guild.name, "inferno")
            print('Mage guild Level 5 built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Hell Hole
    if city.mage_guild.lvl >= 2 and city.creature_dwellings[5-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][1], player):
            build(city.creature_dwellings[5-1].cost[0][1], player)
            city.creature_dwellings[5-1].lvl = 2
            buy_building(city.creature_dwellings[5-1].name, "inferno")
            print('Hell Hole upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Forsaken Palace
    if city.creature_dwellings[7-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][1], player):
            build(city.creature_dwellings[7-1].cost[0][1], player)
            city.creature_dwellings[7-1].lvl = 2
            buy_building(city.creature_dwellings[7-1].name, "inferno")
            print('Forsaken Palace upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Fire Lake
    if city.creature_dwellings[6-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][1], player):
            build(city.creature_dwellings[6-1].cost[0][1], player)
            city.creature_dwellings[6-1].lvl = 2
            buy_building(city.creature_dwellings[6-1].name, "inferno")
            print('Fire Lake upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Order of Fire
    if city.mage_guild.lvl >= 1 and city.order_of_fire.built == False and builds:
        if resourceCheck(city.order_of_fire.cost[0], player):
            build(city.order_of_fire.cost[0], player)
            city.order_of_fire.built = True
            buy_building(city.order_of_fire.name, "inferno")
            print('Order of Fire built!')
            return None
        else:
            print('Not enough resources!')

    # Cages
    if city.creature_dwellings[3-1].lvl >= 1 and city.cages.built == False and builds:
        if resourceCheck(city.cages.cost[0], player):
            build(city.cages.cost[0], player)
            city.cages.built = True
            buy_building(city.cages.name, "inferno")
            print('Cages built!')
            return None
        else:
            print('Not enough resources!')

    # Birthing Pools
    if city.creature_dwellings[1-1].lvl >= 1 and city.birthing_pools.built == False and builds:
        if resourceCheck(city.birthing_pools.cost[0], player):
            build(city.birthing_pools.cost[0], player)
            city.birthing_pools.built = True
            buy_building(city.birthing_pools.name, "inferno")
            print('Birthing Pool built!')
            return None
        else:
            print('Not enough resources!')

    # Castle Gate
    if city.fort.lvl >= 2 and city.castle_gate.built == False and builds:
        if resourceCheck(city.castle_gate.cost[0], player):
            build(city.castle_gate.cost[0], player)
            city.castle_gate.built = True
            buy_building(city.castle_gate.name, "inferno")
            print('Castle Gate built!')
            return None
        else:
            print('Not enough resources!')

    # Brimstone Stormclouds
    if city.fort.lvl >= 1 and city.brimstone_stormclouds.built == False and builds:
        if resourceCheck(city.brimstone_stormclouds.cost[0], player):
            build(city.brimstone_stormclouds.cost[0], player)
            city.brimstone_stormclouds.built = True
            buy_building(city.brimstone_stormclouds.name, "inferno")
            print('Brimstone Stormclouds built!')
            return None
        else:
            print('Not enough resources!')

    # Resource Silo
    if city.resource_silo.built == False and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            city.resource_silo.built = True
            player.daily_income[3] += 1
            buy_building(city.resource_silo.name, "inferno")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')
