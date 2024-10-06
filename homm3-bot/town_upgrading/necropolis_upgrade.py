"""Script containing Necropolis castle upgrade alghoritm"""
from town_upgrading.choice_generator import town_choice, full_unit_cost
from GUI_handling.TownGUI import buy_building
from data.building import Cost
from data.player_data import Player


def resourceCheck(buildingCost, player: Player):
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


def build(buildingCost, player):
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


def necropolisUpgrade(player, necropolis):
    """
    Necropolis castle upgrade alghoritm.
    :param player: player object
    :param necropolis: Necropolis object
    :return: None
    """
    cost = full_unit_cost(necropolis)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if not necropolis.tavern.built:
        if resourceCheck(necropolis.tavern.cost[0], player):
            build(necropolis.tavern.cost[0], player)
            necropolis.tavern.built = True
            buy_building(necropolis.tavern.name, "necropolis")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort
    if necropolis.tavern.built and necropolis.fort.lvl < 1:
        if resourceCheck(necropolis.fort.cost[0][0], player):
            build(necropolis.fort.cost[0][0], player)
            necropolis.fort.lvl = 1
            buy_building(necropolis.fort.name, "necropolis")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Cursed Temple
    if necropolis.fort.lvl >= 1 and necropolis.creature_dwellings[1-1].lvl == 0 :
        if resourceCheck(necropolis.creature_dwellings[1-1].cost[0][0], player):
            build(necropolis.creature_dwellings[1-1].cost[0][0], player)
            necropolis.creature_dwellings[1-1].lvl = 1
            buy_building(necropolis.creature_dwellings[1-1].name, "necropolis")
            print('Cursed Temple built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Tomb of Souls
    if necropolis.creature_dwellings[3-1].lvl == 0 and necropolis.creature_dwellings[1-1].lvl >= 1:
        if resourceCheck(necropolis.creature_dwellings[3-1].cost[0][0], player):
            build(necropolis.creature_dwellings[3-1].cost[0][0], player)
            necropolis.creature_dwellings[3-1].lvl = 1
            buy_building(necropolis.creature_dwellings[3-1].name, "necropolis")
            print('Tomb of Souls built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Graveyard
    if necropolis.creature_dwellings[2-1].lvl == 0 and necropolis.creature_dwellings[3-1].lvl >= 1:
        if resourceCheck(necropolis.creature_dwellings[2-1].cost[0][0], player):
            build(necropolis.creature_dwellings[2-1].cost[0][0], player)
            necropolis.creature_dwellings[2-1].lvl = 1
            buy_building(necropolis.creature_dwellings[2-1].name, "necropolis")
            print('Graveyard built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Estate
    if necropolis.creature_dwellings[4-1].lvl == 0 and necropolis.creature_dwellings[2-1].lvl >= 1:
        if resourceCheck(necropolis.creature_dwellings[4-1].cost[0][0], player):
            build(necropolis.creature_dwellings[4-1].cost[0][0], player)
            necropolis.creature_dwellings[4-1].lvl = 1
            buy_building(necropolis.creature_dwellings[4-1].name, "necropolis")
            print('lvl 4 habitat built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Town Hall
    if necropolis.city_hall.lvl <= 0 and necropolis.creature_dwellings[4-1].lvl >= 1:
        if resourceCheck(necropolis.city_hall.cost[0][0], player):
            build(necropolis.city_hall.cost[0][0], player)
            necropolis.city_hall.lvl = 1
            player.daily_income[0] += 500
            buy_building(necropolis.city_hall.name, "necropolis")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, necropolis)

    #------------------------------------------------------------------------------------------

    # 8 Citadel
    if necropolis.fort.lvl == 1 and wall:
        if resourceCheck(necropolis.fort.cost[0][1], player):
            build(necropolis.fort.cost[0][1], player)
            necropolis.fort.lvl = 2
            buy_building(necropolis.fort.name, "necropolis")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # 9 Mage Guild Level 1
    if necropolis.mage_guild.lvl == 0 and MG_M:
        if resourceCheck(necropolis.mage_guild.cost[0][0], player):
            build(necropolis.mage_guild.cost[0][0], player)
            necropolis.mage_guild.lvl = 1
            buy_building(necropolis.mage_guild.name, "necropolis")
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')

    # 10 Marketplace
    if not necropolis.marketplace.built and MG_M:
        if resourceCheck(necropolis.marketplace.cost[0], player):
            build(necropolis.marketplace.cost[0], player)
            necropolis.marketplace.built = True
            buy_building(necropolis.marketplace.name, "necropolis")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 11 Blacksmith
    if not necropolis.blacksmith.built and MG_M:
        if resourceCheck(necropolis.blacksmith.cost[0], player):
            build(necropolis.blacksmith.cost[0], player)
            necropolis.blacksmith.built = True
            buy_building(necropolis.blacksmith.name, "necropolis")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 12 City Hall
    if necropolis.city_hall.lvl == 1 and necropolis.marketplace.built and necropolis.blacksmith.built and necropolis.mage_guild.lvl >= 1 and capi:
        if resourceCheck(necropolis.city_hall.cost[0][1], player):
            build(necropolis.city_hall.cost[0][1], player)
            necropolis.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(necropolis.city_hall.name, "necropolis")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Necromancy Amplifier
    if necropolis.mage_guild.lvl >= 1 and not necropolis.necromancy_amplifier.built and builds:
        if resourceCheck(necropolis.necromancy_amplifier.cost[0], player):
            build(necropolis.necromancy_amplifier.cost[0], player)
            necropolis.necromancy_amplifier.built = True
            buy_building(necropolis.necromancy_amplifier.name, "necropolis")
            print('Necromancy Amplifier built')
            return None
        else:
            print('Not enough resources!')

    # 14 Upg. Tomb of Souls
    if necropolis.creature_dwellings[3-1].lvl == 1 and upg:
        if resourceCheck(necropolis.creature_dwellings[3-1].cost[0][1], player):
            build(necropolis.creature_dwellings[3-1].cost[0][1], player)
            necropolis.creature_dwellings[3-1].lvl = 2
            buy_building(necropolis.creature_dwellings[3-1].name, "necropolis")
            print('Tomb of Souls upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 15 Mage Guild Level 2
    if necropolis.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(necropolis.mage_guild.cost[0][1], player):
            build(necropolis.mage_guild.cost[0][1], player)
            necropolis.mage_guild.lvl = 2
            buy_building(necropolis.mage_guild.name, "necropolis")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 16 Cover of Darkness
    if not necropolis.cover_of_darkness.built and necropolis.fort.lvl >= 1 and builds:
        if resourceCheck(necropolis.cover_of_darkness.cost[0], player):
            build(necropolis.cover_of_darkness.cost[0], player)
            necropolis.cover_of_darkness.built = True
            buy_building(necropolis.cover_of_darkness.name, "necropolis")
            print("Cover of Darkness built")
            return None
        else:
            print('Not enough resources!')

    # 17 Upg. Cursed Temple
    if necropolis.creature_dwellings[1-1].lvl == 1 and upg:
        if resourceCheck(necropolis.creature_dwellings[1-1].cost[0][1], player):
            build(necropolis.creature_dwellings[1-1].cost[0][1], player)
            necropolis.creature_dwellings[1-1].lvl = 2
            buy_building(necropolis.creature_dwellings[1-1].name, "necropolis")
            print('Cursed Temple upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 18 Skeleton Transformer
    if not necropolis.skeleton_transformer.built and necropolis.creature_dwellings[1-1].lvl >= 1 and builds:
        if resourceCheck(necropolis.skeleton_transformer.cost[0], player):
            build(necropolis.skeleton_transformer.cost[0], player)
            necropolis.skeleton_transformer.built = True
            buy_building(necropolis.skeleton_transformer.name, "necropolis")
            print("Skeleton Transformer Built")
            return None
        else:
            print('Not enough resources!')

    # 19 Mausoleum
    if necropolis.creature_dwellings[5-1].lvl == 0 and necropolis.mage_guild.lvl >= 1 and necropolis.creature_dwellings[2-1].lvl >= 1 and hab:
        if resourceCheck(necropolis.creature_dwellings[5-1].cost[0][0], player):
            build(necropolis.creature_dwellings[5-1].cost[0][0], player)
            necropolis.creature_dwellings[5-1].lvl = 1
            buy_building(necropolis.creature_dwellings[5-1].name, "necropolis")
            print('Mausoleum built!')
            return None
        else:
            print('Not enough resources!')

    # 20 Castle
    if necropolis.fort.lvl == 2 and wall:
        if resourceCheck(necropolis.fort.cost[0][2], player):
            build(necropolis.fort.cost[0][2], player)
            necropolis.fort.lvl = 3
            buy_building(necropolis.fort.name, "necropolis")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 21 Capitol
    if necropolis.fort.lvl == 3 and necropolis.city_hall.lvl == 2 and capi:
        if resourceCheck(necropolis.city_hall.cost[0][2], player):
            build(necropolis.city_hall.cost[0][2], player)
            necropolis.city_hall.lvl = 3
            player.daily_income[0] += 2000
            buy_building(necropolis.city_hall.name, "necropolis")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 22 Hall of Darkness
    if necropolis.creature_dwellings[6-1].lvl == 0 and necropolis.creature_dwellings[4-1].lvl >= 1 and necropolis.creature_dwellings[5-1].lvl >= 1 and hab:
        if resourceCheck(necropolis.creature_dwellings[6-1].cost[0][0], player):
            build(necropolis.creature_dwellings[6-1].cost[0][0], player)
            necropolis.creature_dwellings[6-1].lvl = 1
            buy_building(necropolis.creature_dwellings[6-1].name, "necropolis")
            print('Hall of Darkness built!')
            return None
        else:
            print('Not enough resources!')

    # 23 Upg. Estate
    if necropolis.creature_dwellings[4-1].lvl == 1 and necropolis.necromancy_amplifier.built and upg:
        if resourceCheck(necropolis.creature_dwellings[4-1].cost[0][1], player):
            build(necropolis.creature_dwellings[4-1].cost[0][1], player)
            necropolis.creature_dwellings[4-1].lvl = 2
            buy_building(necropolis.creature_dwellings[4-1].name, "necropolis")
            print('Estate upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 24 Mage Guild Level 3
    if necropolis.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(necropolis.mage_guild.cost[0][2], player):
            build(necropolis.mage_guild.cost[0][2], player)
            necropolis.mage_guild.lvl = 3
            buy_building(necropolis.mage_guild.name, "necropolis")
            print('Mage Guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 25 Upg. Graveyard
    if necropolis.creature_dwellings[2-1].lvl == 1 and upg:
        if resourceCheck(necropolis.creature_dwellings[2-1].cost[0][1], player):
            build(necropolis.creature_dwellings[2-1].cost[0][1], player)
            necropolis.creature_dwellings[2-1].lvl = 2
            buy_building(necropolis.creature_dwellings[2-1].name, "necropolis")
            print('Graveyard upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 26 Unearthed Graves
    if not necropolis.unearthed_graves.built and necropolis.skeleton_transformer.built and builds:
        if resourceCheck(necropolis.unearthed_graves.cost[0], player):
            build(necropolis.unearthed_graves.cost[0], player)
            necropolis.unearthed_graves.built = True
            buy_building(necropolis.unearthed_graves.name, "necropolis")
            print("Unherated Graves built")
            return None
        else:
            print('Not enough resources!')

    # 27 Upg. Mausoleum
    if necropolis.creature_dwellings[5-1].lvl == 1 and upg:
        if resourceCheck(necropolis.creature_dwellings[5-1].cost[0][1], player):
            build(necropolis.creature_dwellings[5-1].cost[0][1], player)
            necropolis.creature_dwellings[5-1].lvl = 2
            buy_building(necropolis.creature_dwellings[5-1].name, "necropolis")
            print('Mausoleum upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 28 Resource Silo
    if necropolis.marketplace.built and not necropolis.resource_silo.built:
        if resourceCheck(necropolis.resource_silo.cost[0], player):
            build(necropolis.resource_silo.cost[0], player)
            necropolis.resource_silo.built = True
            player.daily_income[1] += 1
            player.daily_income[2] += 1
            buy_building(necropolis.resource_silo.name, "necropolis")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 29 Dragon Vault
    if necropolis.creature_dwellings[7-1].lvl == 0 and necropolis.creature_dwellings[6-1].lvl >= 1 and hab:
        if resourceCheck(necropolis.creature_dwellings[7-1].cost[0][0], player):
            build(necropolis.creature_dwellings[7-1].cost[0][0], player)
            necropolis.creature_dwellings[7-1].lvl = 1
            buy_building(necropolis.creature_dwellings[7-1].name, "necropolis")
            print('Dragon Vault built!')
            return None
        else:
            print('Not enough resources!')

    # 30 Upg. Hall of Darkness
    if necropolis.creature_dwellings[6-1].lvl == 1 and upg:
        if resourceCheck(necropolis.creature_dwellings[6-1].cost[0][1], player):
            build(necropolis.creature_dwellings[6-1].cost[0][1], player)
            necropolis.creature_dwellings[6-1].lvl = 2
            buy_building(necropolis.creature_dwellings[6-1].name, "necropolis")
            print('Hall of Darkness upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 31 Mage Guild Level 4
    if necropolis.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(necropolis.mage_guild.cost[0][3], player):
            build(necropolis.mage_guild.cost[0][3], player)
            necropolis.mage_guild.lvl = 4
            buy_building(necropolis.mage_guild.name, "necropolis")
            print("Mage Guild Level 4")
            return None
        else:
            print('Not enough resources!')

    # 32 Mage Guild Level 5
    if necropolis.mage_guild.lvl == 4 and MG_M:
        if resourceCheck(necropolis.mage_guild.cost[0][4], player):
            build(necropolis.mage_guild.cost[0][4], player)
            necropolis.mage_guild.lvl = 5
            buy_building(necropolis.mage_guild.name, "necropolis")
            print("Mage Guild Level 5")
            return None
        else:
            print('Not enough resources!')

    # 33 Upg. Dragon Vault
    if necropolis.creature_dwellings[7-1].lvl == 1 and upg:
        if resourceCheck(necropolis.creature_dwellings[7-1].cost[0][1], player):
            build(necropolis.creature_dwellings[7-1].cost[0][1], player)
            necropolis.creature_dwellings[7-1].lvl = 2
            buy_building(necropolis.creature_dwellings[7-1].name, "necropolis")
            print('Dragon Vault upgraded!')
            return None
        else:
            print('Not enough resources!')
