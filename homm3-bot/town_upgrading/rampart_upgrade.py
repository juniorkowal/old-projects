"""Script containing Rampart castle upgrade algorithm"""
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


def rampartUpgrade(player: Player, city):
    """
    Rampart castle upgrade algorithm.
    :param player: Player object
    :param city: Rampart object
    :return: None
    """
    cost = full_unit_cost(city)
    if player.gold < (cost/3):
        print("Not enough gold for units, don't build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if city.tavern.built == False:
        if resourceCheck(city.tavern.cost[0], player):
            build(city.tavern.cost[0], player)
            city.tavern.built = True
            buy_building(city.tavern.name, "rampart")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort
    if city.tavern.built and city.fort.lvl < 1:
        if resourceCheck(city.fort.cost[0][0], player):
            build(city.fort.cost[0][0], player)
            city.fort.lvl = 1
            buy_building(city.fort.name, "rampart")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Centaur Stables
    if city.fort.lvl>=1 and city.creature_dwellings[1-1].lvl==0:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][0], player):
            build(city.creature_dwellings[1-1].cost[0][0], player)
            city.creature_dwellings[1-1].lvl=1
            buy_building(city.creature_dwellings[1-1].name, "rampart")
            print('Centaur Stables built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Homestead
    if city.creature_dwellings[1-1].lvl>=1 and city.creature_dwellings[3-1].lvl==0:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][0], player):
            build(city.creature_dwellings[3-1].cost[0][0], player)
            city.creature_dwellings[3-1].lvl=1
            buy_building(city.creature_dwellings[3-1].name, "rampart")
            print('Homestead built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Dwarf Cottage
    if city.creature_dwellings[1-1].lvl>=1 and city.creature_dwellings[2-1].lvl==0:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][0], player):
            build(city.creature_dwellings[2-1].cost[0][0], player)
            city.creature_dwellings[2-1].lvl=1
            buy_building(city.creature_dwellings[2-1].name, "rampart")
            print('Dwarf Cottage built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Town Hall
    if city.tavern.built and city.city_hall.lvl <= 0:
        if resourceCheck(city.city_hall.cost[0][0], player):
            build(city.city_hall.cost[0][0], player)
            city.city_hall.lvl = 1
            player.daily_income[0] += 500
            buy_building(city.city_hall.name, "rampart")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Enchanted Spring
    if city.creature_dwellings[3-1].lvl>=1 and city.creature_dwellings[4-1].lvl==0:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            city.creature_dwellings[4-1].lvl=1
            buy_building(city.creature_dwellings[4-1].name, "rampart")
            print('Enchanted Spring built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Mage Guild Level 1
    if city.fort.lvl >= 1 and city.mage_guild.lvl < 1:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            city.mage_guild.lvl = 1
            buy_building(city.mage_guild.name, "rampart")
            print('Mage Guild Level 1 built')
            return None
        else:
            print('Not enough resources!')
            return None
            # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------

    # 9 Marketplace
    if not city.marketplace.built and MG_M:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            city.marketplace.built = True
            buy_building(city.marketplace.name, "rampart")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 10 Blacksmith
    if not city.blacksmith.built and MG_M:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            city.blacksmith.built = True
            buy_building(city.blacksmith.name, "rampart")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 11 City Hall
    if city.city_hall.lvl == 1 and city.mage_guild.lvl >= 1 and city.blacksmith.built and city.marketplace.built and capi:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            city.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(city.city_hall.name, "rampart")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 12 Capitol
    if city.city_hall.lvl == 2 and city.fort.lvl == 3 and capi:
        if resourceCheck(city.city_hall.cost[0][2], player):
            build(city.city_hall.cost[0][2], player)
            city.city_hall.lvl = 3
            player.daily_income[0] += 2000
            buy_building(city.city_hall.name, "rampart")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Citadel
    if city.fort.lvl == 1 and wall:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            city.fort.lvl = 2
            buy_building(city.fort.name, "rampart")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # 14 Dendroid Arches
    if city.creature_dwellings[3-1].lvl>=1 and city.creature_dwellings[5-1].lvl==0 and builds:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][0], player):
            build(city.creature_dwellings[5-1].cost[0][0], player)
            city.creature_dwellings[5-1].lvl=1
            buy_building(city.creature_dwellings[5-1].name, "rampart")
            print('Dendroid Arches built!')
            return None
        else:
            print('Not enough resources!')

    # 15 Upg. Homestead
    if city.creature_dwellings[3-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][1], player):
            build(city.creature_dwellings[3-1].cost[0][1], player)
            city.creature_dwellings[3-1].lvl=2
            buy_building(city.creature_dwellings[3-1].name, "rampart")
            print('Homestead upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if city.fort.lvl == 2 and wall:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            city.fort.lvl = 3
            buy_building(city.fort.name, "rampart")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Unicorn Glade
    if city.creature_dwellings[4-1].lvl>=1 and city.creature_dwellings[6-1].lvl==0 and city.creature_dwellings[5-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][0], player)
            city.creature_dwellings[6-1].lvl=1
            buy_building(city.creature_dwellings[6-1].name, "rampart")
            print('Unicorn Glade built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Mage Guild Level 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            city.mage_guild.lvl = 2
            buy_building(city.mage_guild.name, "rampart")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 19 Mage Guild Level 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            city.mage_guild.lvl = 3
            buy_building(city.mage_guild.name, "rampart")
            print('Mage Guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 20 Miners Guild
    if city.creature_dwellings[2-1].lvl>=1 and city.miners_guild.built == False and builds:
        if resourceCheck(city.miners_guild.cost[0], player):
            build(city.miners_guild.cost[0], player)
            city.miners_guild.built = True
            buy_building(city.miners_guild.name, "rampart")
            print('Miners Guild built')
            return None
        else:
            print('Not enough resources!')

    # 21 Upg. Centaur Stables
    if city.creature_dwellings[1-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][1], player):
            build(city.creature_dwellings[1-1].cost[0][1], player)
            city.creature_dwellings[1-1].lvl=2
            buy_building(city.creature_dwellings[1-1].name, "rampart")
            print('Centaur Stables upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 22 Upg. Dwarf Cottage
    if city.creature_dwellings[2-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][1], player):
            build(city.creature_dwellings[2-1].cost[0][1], player)
            city.creature_dwellings[2-1].lvl=2
            buy_building(city.creature_dwellings[2-1].name, "rampart")
            print('Dwarf Cottage upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 23 Treasury
    if city.miners_guild.built and city.treasury.built == False and builds:
        if resourceCheck(city.treasury.cost[0], player):
            build(city.treasury.cost[0], player)
            city.treasury.built = True
            buy_building(city.treasury.name, "rampart")
            print('Treasury built')
            return None
        else:
            print('Not enough resources!')

    # 24 Dragon Cliffs
    if city.creature_dwellings[6-1].lvl>=1 and city.creature_dwellings[7-1].lvl==0 and city.mage_guild.lvl >= 2 and hab:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][0], player):
            build(city.creature_dwellings[7-1].cost[0][0], player)
            city.creature_dwellings[7-1].lvl=1
            buy_building(city.creature_dwellings[7-1].name, "rampart")
            print('Dragon Cliffs built!')
            return None
        else:
            print('Not enough resources!')

    # 25 Upg. Unicorn Glade
    if city.creature_dwellings[6-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][1], player):
            build(city.creature_dwellings[6-1].cost[0][1], player)
            city.creature_dwellings[6-1].lvl=2
            buy_building(city.creature_dwellings[6-1].name, "rampart")
            print('Unicorn Glade upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 26 Upg. Dragon Cliffs
    if city.creature_dwellings[7-1].lvl==1 and city.mage_guild.lvl >= 3 and upg:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][1], player):
            build(city.creature_dwellings[7-1].cost[0][1], player)
            city.creature_dwellings[7-1].lvl=2
            buy_building(city.creature_dwellings[7-1].name, "rampart")
            print('Dragon Cliffs upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 27  Mage Guild Level 4
    if city.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][3], player):
            build(city.mage_guild.cost[0][3], player)
            city.mage_guild.lvl = 4
            buy_building(city.mage_guild.name, "rampart")
            print('Mage Guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # 28 Mage Guild Level 5
    if city.mage_guild.lvl == 4 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][4], player):
            build(city.mage_guild.cost[0][4], player)
            city.mage_guild.lvl = 5
            buy_building(city.mage_guild.name, "rampart")
            print('Mage Guild Level 5!')
            return None
        else:
            print('Not enough resources!')

    if not city.resource_silo.built and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            city.resource_silo.built = True
            player.daily_income[5] += 1
            buy_building(city.resource_silo.name, "rampart")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')
