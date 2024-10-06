"""Script containing Stronghold castle upgrade algorithm"""
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


def strongholdUpgrade(player, city):
    """
    Stronghold castle upgrade algorithm.
    :param player: Player object
    :param city: Stronghold object
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
            buy_building(city.tavern.name, "stronghold")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Fort
    if city.fort.lvl == 0 and city.tavern.built:
        if resourceCheck(city.fort.cost[0][0], player):
            build(city.fort.cost[0][0], player)
            city.fort.lvl = 1
            buy_building(city.fort.name, "stronghold")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Goblin Barracks
    if not city.creature_dwellings[1-1].lvl==0 and city.fort.built:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][0], player):
            build(city.creature_dwellings[1-1].cost[0][0], player)
            city.creature_dwellings[1-1].lvl=1
            buy_building(city.creature_dwellings[1-1].name, "stronghold")
            print('Goblin Barracks built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Wolf Pen
    if city.creature_dwellings[1-1].lvl>=1 and city.creature_dwellings[2-1].lvl==0:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][0], player):
            build(city.creature_dwellings[2-1].cost[0][0], player)
            city.creature_dwellings[2-1].lvl=1
            buy_building(city.creature_dwellings[2-1].name, "stronghold")
            print('Wolf Pen built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Cliff Nest
    if city.creature_dwellings[2-1].lvl>=1 and city.creature_dwellings[5-1].lvl==0:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][0], player):
            build(city.creature_dwellings[5-1].cost[0][0], player)
            city.creature_dwellings[5-1].lvl=1
            buy_building(city.creature_dwellings[5-1].name, "stronghold")
            print('Cliff Nest built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Behemoth Lair
    if city.creature_dwellings[5-1].lvl>=1 and city.creature_dwellings[7-1].lvl==0:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][0], player):
            build(city.creature_dwellings[7-1].cost[0][0], player)
            city.creature_dwellings[7-1].lvl=1
            buy_building(city.creature_dwellings[7-1].name, "stronghold")
            print('Behemoth Lair built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Orc Tower
    if city.creature_dwellings[7-1].lvl>=1 and city.creature_dwellings[3-1].lvl==0:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][0], player):
            build(city.creature_dwellings[3-1].cost[0][0], player)
            city.creature_dwellings[3-1].lvl=1
            buy_building(city.creature_dwellings[3-1].name, "stronghold")
            print('Orc Tower built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Town Hall
    if city.creature_dwellings[3-1].lvl>=1 and city.city_hall.lvl==0:
        if resourceCheck(city.city_hall.cost[0][0], player):
            build(city.city_hall.cost[0][0], player)
            city.city_hall.lvl = 1
            player.daily_income[0] += 500
            buy_building(city.city_hall.name, "stronghold")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------
    # Mage guild Level 1
    if city.mage_guild.lvl==0 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            city.mage_guild.lvl = 1
            buy_building(city.mage_guild.name, "stronghold")
            print('Mage guild Level 1!')
            return None
        else:
            print('Not enough resources!')

    # Marketplace
    if not city.marketplace.built and MG_M:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            city.marketplace.built = True
            buy_building(city.marketplace.name, "stronghold")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # Blacksmith
    if not city.blacksmith.built and MG_M:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            city.blacksmith.built = True
            buy_building(city.blacksmith.name, "stronghold")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # City Hall
    if city.blacksmith.built and city.city_hall.lvl == 1 and city.mage_guild.lvl>=1 and city.marketplace.built and capi:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            city.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(city.city_hall.name, "stronghold")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Citadel
    if city.fort.lvl == 1 and wall:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            city.fort.lvl = 2
            buy_building(city.fort.name, "stronghold")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # Ogre Fort
    if city.creature_dwellings[3-1].lvl>=1 and city.creature_dwellings[4-1].lvl==0 and hab:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            city.creature_dwellings[4-1].lvl=1
            buy_building(city.creature_dwellings[4-1].name, "stronghold")
            print('Ogre Fort built!')
            return None
        else:
            print('Not enough resources!')

    # Castle
    if city.fort.lvl == 2 and wall:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            city.fort.lvl = 3
            buy_building(city.fort.name, "stronghold")
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
            buy_building(city.city_hall.name, "stronghold")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Orc Tower
    if city.creature_dwellings[3-1].lvl==1 and city.blacksmith.built and upg:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][1], player):
            build(city.creature_dwellings[3-1].cost[0][1], player)
            city.creature_dwellings[3-1].lvl=2
            buy_building(city.creature_dwellings[3-1].name, "stronghold")
            print('Orc Tower upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Hall of Valhalla
    if not city.hall_of_valhalla.built and city.fort.lvl >= 1 and builds:
        if resourceCheck(city.hall_of_valhalla.cost[0], player):
            build(city.hall_of_valhalla.cost[0], player)
            city.hall_of_valhalla.built = True
            buy_building(city.hall_of_valhalla.name, "stronghold")
            print('Hall of Valhalla built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Goblin Barracks
    if city.creature_dwellings[1-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][1], player):
            build(city.creature_dwellings[1-1].cost[0][1], player)
            city.creature_dwellings[1-1].lvl=2
            buy_building(city.creature_dwellings[1-1].name, "stronghold")
            print('Goblin Barracks upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Wolf Pen
    if city.creature_dwellings[1-1].lvl==2 and city.creature_dwellings[2-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][1], player):
            build(city.creature_dwellings[2-1].cost[0][1], player)
            city.creature_dwellings[2-1].lvl=2
            buy_building(city.creature_dwellings[2-1].name, "stronghold")
            print('Wolf Pen upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Cliff Nest
    if city.creature_dwellings[5-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][1], player):
            build(city.creature_dwellings[5-1].cost[0][1], player)
            city.creature_dwellings[5-1].lvl=2
            buy_building(city.creature_dwellings[5-1].name, "stronghold")
            print('Cliff Nest upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Ogre Fort
    if city.creature_dwellings[4-1].lvl==1 and city.mage_guild.lvl>=1 and upg:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][1], player):
            build(city.creature_dwellings[4-1].cost[0][1], player)
            city.creature_dwellings[4-1].lvl=2
            buy_building(city.creature_dwellings[4-1].name, "stronghold")
            print('Ogre Fort upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            city.mage_guild.lvl = 2
            buy_building(city.mage_guild.name, "stronghold")
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            city.mage_guild.lvl = 3
            buy_building(city.mage_guild.name, "stronghold")
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Behemoth
    if city.creature_dwellings[7-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][1], player):
            build(city.creature_dwellings[7-1].cost[0][1], player)
            city.creature_dwellings[7-1].lvl=2
            buy_building(city.creature_dwellings[7-1].name, "stronghold")
            print('Behemoths upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Freelancers Guild
    if not city.freelancers_guild.built and city.marketplace.built and builds:
        if resourceCheck(city.freelancers_guild.cost[0], player):
            build(city.freelancers_guild.cost[0], player)
            city.freelancers_guild.built = True
            buy_building(city.freelancers_guild.name, "stronghold")
            print('Freelancers Guild built!')
            return None
        else:
            print('Not enough resources!')

    # Resource Silo
    if not city.resource_silo.built and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            city.resource_silo.built = True
            player.daily_income[1] += 1
            player.daily_income[2] += 1
            buy_building(city.resource_silo.name, "stronghold")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # Cyclops Cave
    if city.creature_dwellings[4-1].lvl>=1 and city.creature_dwellings[6-1].lvl==0 and hab:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][0], player)
            city.creature_dwellings[6-1].lvl=1
            buy_building(city.creature_dwellings[6-1].name, "stronghold")
            print('Cyclops Cave built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Cyclops Cave
    if city.creature_dwellings[6-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][1], player):
            build(city.creature_dwellings[6-1].cost[0][1], player)
            city.creature_dwellings[6-1].lvl=2
            buy_building(city.creature_dwellings[6-1].name, "stronghold")
            print('Upgraded Cyclops Cave!')
            return None
        else:
            print('Not enough resources!')

    # Mess Hall
    if city.creature_dwellings[1-1].lvl>=1 and not city.mess_hall.built and builds:
        if resourceCheck(city.mess_hall.cost[0], player):
            build(city.mess_hall.cost[0], player)
            city.mess_hall.built = True
            buy_building(city.mess_hall.name, "stronghold")
            print('Mess Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Ballista Yard
    if not city.ballists_yard.built and city.blacksmith.built and builds:
        if resourceCheck(city.ballists_yard.cost[0], player):
            build(city.ballists_yard.cost[0], player)
            city.ballists_yard.built = True
            buy_building(city.ballists_yard.name, "stronghold")
            print('Ballista Yard built!')
            return None
        else:
            print('Not enough resources!')
