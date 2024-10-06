"""Script containing Tower castle upgrade algorithm"""
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


def towerUpgrade(player: Player, city):
    """
    Tower castle upgrade algorithm.
    :param player: Player object
    :param city: Tower object
    :return: None
    """
    cost = full_unit_cost(city)
    if player.gold < (cost/3):
        print("Not enough gold for units, don't build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # tavern
    if not city.tavern.built:
        if resourceCheck(city.tavern.cost[0], player):
            build(city.tavern.cost[0], player)
            city.tavern.built = True
            buy_building(city.tavern.name, "tower")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # fort
    if city.fort.lvl == 0 and city.tavern.built:
        if resourceCheck(city.fort.cost[0][0], player):
            build(city.fort.cost[0][0], player)
            city.fort.lvl = 1
            buy_building(city.fort.name, "tower")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # workshop
    if city.creature_dwellings[1-1].lvl==0 and city.fort.lvl >= 1:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][0], player):
            build(city.creature_dwellings[1-1].cost[0][0], player)
            city.creature_dwellings[1-1].lvl=1
            buy_building(city.creature_dwellings[1-1].name, "tower")
            print('Workshop built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # parapet
    if city.creature_dwellings[1-1].lvl>=1 and city.creature_dwellings[2-1].lvl==0:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][0], player):
            build(city.creature_dwellings[2-1].cost[0][0], player)
            city.creature_dwellings[2-1].lvl =1
            buy_building(city.creature_dwellings[2-1].name, "tower")
            print('Parapet built!')
            return None
        else:
            print('Not enough resources')
            return None

    # golem factory
    if city.creature_dwellings[3-1].lvl == 0 and city.creature_dwellings[1-1].lvl>=1 and city.creature_dwellings[2-1].lvl>=1:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][0], player):
            build(city.creature_dwellings[3-1].cost[0][0], player)
            city.creature_dwellings[3-1].lvl=1
            buy_building(city.creature_dwellings[3-1].name, "tower")
            print('Golem factory built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # town hall
    if city.city_hall.lvl==0 and city.city_hall.lvl == 0 and city.creature_dwellings[3-1].lvl>=1:
        if resourceCheck(city.city_hall.cost[0][0], player):
            build(city.city_hall.cost[0][0], player)
            city.city_hall.lvl = 1
            player.daily_income[0] += 500
            buy_building(city.city_hall.name, "tower")
            print('City hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # mage guild
    if city.city_hall.lvl >= 1 and city.mage_guild.lvl == 0:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            city.mage_guild.lvl = 1
            buy_building(city.mage_guild.name, "tower")
            print('Mage guild lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # marketplace
    if city.mage_guild.lvl >= 1 and city.marketplace.built == False:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            city.marketplace.built = True
            buy_building(city.marketplace.name, "tower")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------
    # blacksmith
    if not city.blacksmith.built and MG_M:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            city.blacksmith.built = True
            buy_building(city.blacksmith.name, "tower")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # city hall
    if city.city_hall.lvl == 1 and city.blacksmith.built and city.marketplace.built and city.mage_guild.lvl>=1 and capi:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            city.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(city.city_hall.name, "tower")
            print('City hall built!')
            return None
        else:
            print('Not enough resources!')

    # Citadel
    if city.fort.lvl == 1 and wall:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            city.fort.lvl = 2
            buy_building(city.fort.name, "tower")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # mage tower
    if city.mage_guild.lvl>=1 and city.creature_dwellings[4-1].lvl==0 and city.creature_dwellings[2-1].lvl>=1 and city.creature_dwellings[3-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            city.creature_dwellings[4-1].lvl=1
            buy_building(city.creature_dwellings[4-1].name, "tower")
            print('Mage tower built!')
            return None
        else:
            print('Not enough resources!')

    # castle
    if city.fort.lvl == 2 and capi:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            city.fort.lvl = 3
            buy_building(city.fort.name, "tower")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # capitol
    if city.fort.lvl == 3 and city.city_hall.lvl == 2 and capi:
        if resourceCheck(city.city_hall.cost[0][2], player):
            build(city.city_hall.cost[0][2], player)
            city.city_hall.lvl = 3
            player.daily_income[0] += 2000
            buy_building(city.city_hall.name, "tower")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # altar of wishes
    if city.creature_dwellings[5-1].lvl==0 and city.creature_dwellings[4-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][0], player):
            build(city.creature_dwellings[5-1].cost[0][0], player)
            city.creature_dwellings[5-1].lvl=1
            buy_building(city.creature_dwellings[5-1].name, "tower")
            print('Altar of wishes built!')
            return None
        else:
            print('Not enough resources!')

    # golden pavilion
    if city.creature_dwellings[6-1].lvl==0 and city.creature_dwellings[4-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][0], player)
            city.creature_dwellings[6-1].lvl=1
            buy_building(city.creature_dwellings[6-1].name, "tower")
            print('Golden pavilion built!')
            return None
        else:
            print('Not enough resources!')

    # mage guild lvl 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            city.mage_guild.lvl = 2
            buy_building(city.mage_guild.name, "tower")
            print('Mage guild lvl 2 built!')
            return None
        else:
            print('Not enough resources!')

    # mage guild lvl 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            city.mage_guild.lvl = 3
            buy_building(city.mage_guild.name, "tower")
            print('Mage guild lvl 3 built!')
            return None
        else:
            print('Not enough resources!')

    # wall of knowledge
    if city.mage_guild.lvl >= 1 and city.wall_of_knowledge.built == False and builds and False:
        if resourceCheck(city.wall_of_knowledge.cost[0], player):
            build(city.wall_of_knowledge.cost[0], player)
            city.wall_of_knowledge.built = True
            buy_building(city.wall_of_knowledge.name, "tower")
            print('Wall of knowledge built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Parapet
    if city.creature_dwellings[2-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][1], player):
            build(city.creature_dwellings[2-1].cost[0][1], player)
            city.creature_dwellings[2-1].lvl=2
            buy_building(city.creature_dwellings[2-1].name, "tower")
            print('Parapet upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Workshop
    if city.creature_dwellings[1-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][1], player):
            build(city.creature_dwellings[1-1].cost[0][1], player)
            city.creature_dwellings[1-1].lvl=2
            buy_building(city.creature_dwellings[1-1].name, "tower")
            print('Workshop upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. golem factory
    if city.creature_dwellings[3-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][1], player):
            build(city.creature_dwellings[3-1].cost[0][1], player)
            city.creature_dwellings[3-1].lvl=2
            buy_building(city.creature_dwellings[3-1].name, "tower")
            print('Golem factory upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Library
    if city.mage_guild.lvl>=1 and city.library.built == False and builds:
        if resourceCheck(city.library.cost[0], player):
            build(city.library.cost[0], player)
            city.library.built = True
            buy_building(city.library.name, "tower")
            print('Library built!')
            return None
        else:
            print('Not enough resources!')

    # Upg Mage tower
    if city.creature_dwellings[4-1].lvl==1 and city.library.built and upg:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][1], player):
            build(city.creature_dwellings[4-1].cost[0][1], player)
            city.creature_dwellings[4-1].lvl=2
            buy_building(city.creature_dwellings[4-1].name, "tower")
            print('Mage Tower Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # lookout tower
    if city.lookout_tower.built == False and city.fort.lvl >= 1 and builds:
        if resourceCheck(city.lookout_city.cost[0], player):
            build(city.lookout_city.cost[0], player)
            city.lookout_city.built = True
            buy_building(city.lookout_city.name, "tower")
            print('Lookout tower built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Altar of wishes
    if city.creature_dwellings[5-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][1], player):
            build(city.creature_dwellings[5-1].cost[0][1], player)
            city.creature_dwellings[5-1].lvl=2
            buy_building(city.creature_dwellings[5-1].name, "tower")
            print('Altar of wishes upgraded!')
            return None
        else:
            print('Not enough resources!')

    # cloud temple
    if city.creature_dwellings[7-1].lvl==0 and city.creature_dwellings[5-1].lvl>=1 and city.creature_dwellings[6-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][0], player):
            build(city.creature_dwellings[7-1].cost[0][0], player)
            city.creature_dwellings[7-1].lvl=1
            buy_building(city.creature_dwellings[7-1].name, "tower")
            print('Cloud temple built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. cloud temple
    if city.creature_dwellings[7-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][1], player):
            build(city.creature_dwellings[7-1].cost[0][1], player)
            city.creature_dwellings[7-1].lvl=2
            buy_building(city.creature_dwellings[7-1].name, "tower")
            print('Cloud temple upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. golden pavilion
    if city.creature_dwellings[6-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][1], player)
            city.creature_dwellings[6-1].lvl=2
            buy_building(city.creature_dwellings[6-1].name, "tower")
            print('Golden pavilion upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild lvl 4
    if city.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][3], player):
            build(city.mage_guild.cost[0][3], player)
            city.mage_guild.lvl = 4
            buy_building(city.mage_guild.name, "tower")
            print('Mage guild lvl 4!')
            return None
        else:
            print('Not enough resources!')

    # mage guild lvl 5
    if city.mage_guild.lvl == 4 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][4], player):
            build(city.mage_guild.cost[0][4], player)
            city.mage_guild.lvl = 5
            buy_building(city.mage_guild.name, "tower")
            print('Mage guild lvl 5!')
            return None
        else:
            print('Not enough resources!')

    # sculptors wings
    if city.sculptor_wings.built == False and city.creature_dwellings[2-1].lvl>=1 and builds:
        if resourceCheck(city.sculptor_wings.cost[0], player):
            build(city.sculptor_wings.cost[0], player)
            city.sculptor_wings.built = True
            buy_building(city.sculptor_wings.name, "tower")
            print('Sculptors Wings built!')
            return None
        else:
            print('Not enough resources!')

    # resource silo
    if city.resource_silo.built == False and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            city.resource_silo.built = True
            player.daily_income[6] += 1
            buy_building(city.resource_silo.name, "tower")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # artifact merchant
    if city.artifact_merchant.built == False and city.marketplace.built and builds:
        if resourceCheck(city.artifact_merchant.cost[0], player):
            build(city.artifact_merchant.cost[0], player)
            city.artifact_merchant.built = True
            buy_building(city.artifact_merchant.name, "tower")
            print('Artifact merchant build!')
            return None
        else:
            print('Not enough resources!')
