"""Script containing Cove castle upgrade algorithm"""
from GUI_handling.TownGUI import buy_building
from data.building import Cost
from data.player_data import Player
from town_upgrading.choice_generator import town_choice, full_unit_cost


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


def coveUpgrade(player, cove):
    """
    Cove castle upgrade algorithm.
    :param player: Player object
    :param cove: Cove object
    :return: None
    """
    cost = full_unit_cost(cove)
    if player.gold < (cost/3):
        print("Not enough gold for units, don't build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if not cove.tavern.built:
        if resourceCheck(cove.tavern.cost[0], player):
            build(cove.tavern.cost[0], player)
            cove.tavern.built = True
            buy_building(cove.tavern.name, "cove")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort
    if cove.tavern.built and cove.fort.lvl < 1:
        if resourceCheck(cove.fort.cost[0][0], player):
            build(cove.fort.cost[0][0], player)
            cove.fort.lvl = 1
            buy_building(cove.fort.name, "cove")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Waterfall
    if cove.fort.lvl >= 1 and cove.creature_dwellings[1-1].lvl == 0:
        if resourceCheck(cove.creature_dwellings[1-1].cost[0][0], player):
            build(cove.creature_dwellings[1-1].cost[0][0], player)
            cove.creature_dwellings[1-1].lvl = 1
            buy_building(cove.creature_dwellings[1-1].name, "cove")
            print('Waterfall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Shack
    if cove.creature_dwellings[2-1].lvl == 0 and cove.fort.lvl >= 1:
        if resourceCheck(cove.creature_dwellings[2-1].cost[0][0], player):
            build(cove.creature_dwellings[2-1].cost[0][0], player)
            cove.creature_dwellings[2-1].lvl = 1
            buy_building(cove.creature_dwellings[2-1].name, "cove")
            print('Shack built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Nest
    if cove.creature_dwellings[4-1].lvl == 0 and cove.creature_dwellings[2-1].lvl >= 1:
        if resourceCheck(cove.creature_dwellings[4-1].cost[0][0], player):
            build(cove.creature_dwellings[4-1].cost[0][0], player)
            cove.creature_dwellings[4-1].lvl = 1
            buy_building(cove.creature_dwellings[4-1].name, "cove")
            print('Nest built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Nix Fort
    if cove.creature_dwellings[6-1].lvl == 0 and cove.creature_dwellings[4-1].lvl >= 1:
        if resourceCheck(cove.creature_dwellings[6-1].cost[0][0], player):
            build(cove.creature_dwellings[6-1].cost[0][0], player)
            cove.creature_dwellings[6-1].lvl = 1
            buy_building(cove.creature_dwellings[6-1].name, "cove")
            print('Nix Fort built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Town Hall
    if cove.city_hall.lvl == 0:
        if resourceCheck(cove.city_hall.cost[0][0], player):
            build(cove.city_hall.cost[0][0], player)
            cove.city_hall.lvl = 1
            player.daily_income[0] += 500
            buy_building(cove.city_hall.name, "cove")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Citadel
    if cove.fort.lvl == 1:
        if resourceCheck(cove.fort.cost[0][1], player):
            build(cove.fort.cost[0][1], player)
            cove.fort.lvl = 2
            buy_building(cove.fort.name, "cove")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, cove)

    # ------------------------------------------------------------------------------------------
    # 9 Mage Guild Level 1
    if cove.mage_guild.lvl == 0 and MG_M:
        if resourceCheck(cove.mage_guild.cost[0][0], player):
            build(cove.mage_guild.cost[0][0], player)
            cove.mage_guild.lvl = 1
            buy_building(cove.mage_guild.name, "cove")
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')

    # 10 Marketplace
    if not cove.marketplace.built and MG_M:
        if resourceCheck(cove.marketplace.cost[0], player):
            build(cove.marketplace.cost[0], player)
            cove.marketplace.built = True
            buy_building(cove.marketplace.name, "cove")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 11 Blacksmith
    if not cove.blacksmith.built and MG_M:
        if resourceCheck(cove.blacksmith.cost[0], player):
            build(cove.blacksmith.cost[0], player)
            cove.blacksmith.built = True
            buy_building(cove.blacksmith.name, "cove")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 12 City Hall
    if cove.city_hall.lvl == 1 and cove.mage_guild.lvl >= 1 and cove.blacksmith.built and cove.marketplace.built and capi:
        if resourceCheck(cove.city_hall.cost[0][1], player):
            build(cove.city_hall.cost[0][1], player)
            cove.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(cove.city_hall.name, "cove")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Frigate
    if cove.creature_dwellings[3-1].lvl == 0 and cove.creature_dwellings[2-1].lvl >= 1 and cove.blacksmith.built and hab:
        if resourceCheck(cove.creature_dwellings[3-1].cost[0][0], player):
            build(cove.creature_dwellings[3-1].cost[0][0], player)
            cove.creature_dwellings[3-1].lvl = 1
            buy_building(cove.creature_dwellings[3-1].name, "cove")
            print('Frigate built!')
            return None
        else:
            print('Not enough resources!')

    # 14 Tower of the Seas
    if cove.creature_dwellings[5-1].lvl == 0 and cove.creature_dwellings[2-1].lvl >= 1 and hab:
        if resourceCheck(cove.creature_dwellings[5-1].cost[0][0], player):
            build(cove.creature_dwellings[5-1].cost[0][0], player)
            cove.creature_dwellings[5-1].lvl = 1
            buy_building(cove.creature_dwellings[5-1].name, "cove")
            print('Tower of the Seas built!')
            return None
        else:
            print('Not enough resources!')

    # 15 Upg. Waterfall
    if cove.creature_dwellings[1-1].lvl == 1 and upg:
        if resourceCheck(cove.creature_dwellings[1-1].cost[0][1], player):
            build(cove.creature_dwellings[1-1].cost[0][1], player)
            cove.creature_dwellings[1-1].lvl = 2
            buy_building(cove.creature_dwellings[1-1].name, "cove")
            print('Waterfall upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 16 Upg. Shack
    if cove.creature_dwellings[2-1].lvl == 1 and upg:
        if resourceCheck(cove.creature_dwellings[2-1].cost[0][1], player):
            build(cove.creature_dwellings[2-1].cost[0][1], player)
            cove.creature_dwellings[2-1].lvl = 2
            buy_building(cove.creature_dwellings[2-1].name, "cove")
            print('Shack upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 17 Mage Guild Level 2
    if cove.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(cove.mage_guild.cost[0][1], player):
            build(cove.mage_guild.cost[0][1], player)
            cove.mage_guild.lvl = 2
            buy_building(cove.mage_guild.name, "cove")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 18 Castle
    if cove.fort.lvl == 2 and wall:
        if resourceCheck(cove.fort.cost[0][2], player):
            build(cove.fort.cost[0][2], player)
            cove.fort.lvl = 3
            buy_building(cove.fort.name, "cove")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 19 Capitol
    if cove.city_hall.lvl == 2 and cove.fort.lvl == 3 and capi:
        if resourceCheck(cove.city_hall.cost[0][2], player):
            build(cove.city_hall.cost[0][2], player)
            cove.city_hall.lvl = 3
            player.daily_income[0] += 2000
            buy_building(cove.city_hall.name, "cove")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 20 Upg. Nest
    if cove.creature_dwellings[4-1].lvl == 1 and upg:
        if resourceCheck(cove.creature_dwellings[4-1].cost[0][1], player):
            build(cove.creature_dwellings[4-1].cost[0][1], player)
            cove.creature_dwellings[4-1].lvl = 2
            buy_building(cove.creature_dwellings[4-1].name, "cove")
            print('Nest upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 21 Upg. Frigate
    if cove.creature_dwellings[3-1].lvl == 1 and upg:
        if resourceCheck(cove.creature_dwellings[3-1].cost[0][1], player):
            build(cove.creature_dwellings[3-1].cost[0][1], player)
            cove.creature_dwellings[3-1].lvl = 2
            buy_building(cove.creature_dwellings[3-1].name, "cove")
            print('Frigate upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 22 Pub
    if not cove.pub.built and cove.creature_dwellings[2-1].lvl >= 1 and builds:
        if resourceCheck(cove.pub.cost[0], player):
            build(cove.pub.cost[0], player)
            cove.pub.built = True
            buy_building(cove.pub.name, "cove")
            print("Pub built!")
            return None
        else:
            print('Not enough resources!')

    # 23 Thieves Guild
    if not cove.thieves_guild.built and cove.tavern.built and builds:
        if resourceCheck(cove.thieves_guild.cost[0], player):
            build(cove.thieves_guild.cost[0], player)
            cove.thieves_guild.built = True
            buy_building(cove.thieves_guild.name, "cove")
            print("Thieves Guild built!")
            return None
        else:
            print('Not enough resources!')

    # 24 Resource Silo
    if not cove.resource_silo.built and cove.marketplace.built:
        if resourceCheck(cove.resource_silo.cost[0], player):
            build(cove.resource_silo.cost[0], player)
            cove.resource_silo.built = True
            player.daily_income[4] += 1
            buy_building(cove.resource_silo.name, "cove")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 25 Grotto
    if not cove.grotto.built and cove.marketplace.built and builds:
        if resourceCheck(cove.grotto.cost[0], player):
            build(cove.grotto.cost[0], player)
            cove.grotto.built = True
            buy_building(cove.grotto.name, "cove")
            print("Grotto built!")
            return None
        else:
            print('Not enough resources!')

    # 26 Whirlpool
    if cove.creature_dwellings[7-1].lvl == 0 and cove.creature_dwellings[5-1].lvl >= 1 and cove.creature_dwellings[6-1].lvl >= 1 and hab:
        if resourceCheck(cove.creature_dwellings[7-1].cost[0][0], player):
            build(cove.creature_dwellings[7-1].cost[0][0], player)
            cove.creature_dwellings[7-1].lvl = 1
            buy_building(cove.creature_dwellings[7-1].name, "cove")
            print('Whirlpool built!')
            return None
        else:
            print('Not enough resources!')

    # 27 Upg. Tower of the Seas
    if cove.creature_dwellings[5-1].lvl == 1 and cove.mage_guild.lvl >= 2 and upg:
        if resourceCheck(cove.creature_dwellings[5-1].cost[0][1], player):
            build(cove.creature_dwellings[5-1].cost[0][1], player)
            cove.creature_dwellings[5-1].lvl = 2
            buy_building(cove.creature_dwellings[5-1].name, "cove")
            print('Tower of the Seas upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 28 Rost
    if not cove.roost.built and cove.creature_dwellings[4-1].lvl >= 1 and builds:
        if resourceCheck(cove.roost.cost[0], player):
            build(cove.roost.cost[0], player)
            cove.roost.built = True
            buy_building(cove.roost.name, "cove")
            print("Rost built!")
            return None
        else:
            print('Not enough resources!')

    # 29 Mage Guild Level 3
    if cove.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(cove.mage_guild.cost[0][2], player):
            build(cove.mage_guild.cost[0][2], player)
            cove.mage_guild.lvl = 3
            buy_building(cove.mage_guild.name, "cove")
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 30 Mage Guild Level 4
    if cove.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(cove.mage_guild.cost[0][3], player):
            build(cove.mage_guild.cost[0][3], player)
            cove.mage_guild.lvl = 4
            buy_building(cove.mage_guild.name, "cove")
            print('Mage guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # 31 Upg. Nix
    if cove.creature_dwellings[6-1].lvl == 1 and upg:
        if resourceCheck(cove.creature_dwellings[6-1].cost[0][1], player):
            build(cove.creature_dwellings[6-1].cost[0][1], player)
            cove.creature_dwellings[6-1].lvl = 2
            buy_building(cove.creature_dwellings[6-1].name, "cove")
            print('Nix upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 32 Upg. Whirlpool
    if cove.creature_dwellings[7-1].lvl == 1 and cove.mage_guild.lvl >= 2 and upg:
        if resourceCheck(cove.creature_dwellings[7-1].cost[0][1], player):
            build(cove.creature_dwellings[7-1].cost[0][1], player)
            cove.creature_dwellings[7-1].lvl = 2
            buy_building(cove.creature_dwellings[7-1].name, "cove")
            print('Whirlpool upgraded!')
            return None
        else:
            print('Not enough resources!')
