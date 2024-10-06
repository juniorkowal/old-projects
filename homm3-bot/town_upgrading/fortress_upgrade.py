"""Script containing Fortress castle upgrade algorithm"""
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


def fortressUpgrade(player, city):
    """
    Fortress castle upgrade algorithm.
    :param player: player object
    :param city: Fortress object
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
            buy_building(city.tavern.name, "fortress")
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
            buy_building(city.fort.name, "fortress")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Gnoll Hut
    if city.fort.lvl>=1 and city.creature_dwellings[1-1].lvl==0:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][0], player):
            build(city.creature_dwellings[1-1].cost[0][0], player)
            city.creature_dwellings[1-1].lvl=1
            buy_building(city.creature_dwellings[1-1].name, "fortress")
            print('Gnoll Hut built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Lizard Den
    if city.creature_dwellings[2-1].lvl == 0 and city.creature_dwellings[1-1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][0], player):
            build(city.creature_dwellings[2-1].cost[0][0], player)
            city.creature_dwellings[2-1].lvl = 1
            buy_building(city.creature_dwellings[2-1].name, "fortress")
            print('Lizard Den built!')
            return None
        else:
            print('Not enough resources!')
            return None


    # 4.5 Wyvern Nest
    print(city.creature_dwellings[6-1].lvl)
    if city.creature_dwellings[6-1].lvl == 0 and city.creature_dwellings[2-1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][0], player)
            city.creature_dwellings[6-1].lvl = 1
            buy_building(city.creature_dwellings[6-1].name, "fortress")
            print('Wyvern Nest built!')
            return None
        else:
            print('Not enough resources!')
            return None


    # 5 Serpent Fly Hive
    if city.creature_dwellings[3-1].lvl == 0 and city.creature_dwellings[2-1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][0], player):
            build(city.creature_dwellings[3-1].cost[0][0], player)
            city.creature_dwellings[3-1].lvl = 1
            buy_building(city.creature_dwellings[3-1].name, "fortress")
            print('Serpent Fly Hive built!')
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
            buy_building(city.city_hall.name, "fortress")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Citadel
    if city.fort.lvl == 1 and city.city_hall.lvl == 1:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            city.fort.lvl = 2
            buy_building(city.fort.name, "fortress")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Basilisk Pit
    if city.creature_dwellings[4-1].lvl==0 and city.fort.lvl >= 2:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            city.creature_dwellings[4-1].lvl=1
            buy_building(city.creature_dwellings[4-1].name, "fortress")
            print('Basilisk Pit built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------
    # 9 Upg. Lizard Den
    if city.creature_dwellings[2-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][1], player):
            build(city.creature_dwellings[2-1].cost[0][1], player)
            city.creature_dwellings[2-1].lvl=2
            buy_building(city.creature_dwellings[2-1].name, "fortress")
            print('Lizard Den upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 10 Mage Guild Level 1
    if city.mage_guild.lvl == 0 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            city.mage_guild.lvl = 1
            buy_building(city.mage_guild.name, "fortress")
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')

    # 11 Marketplace
    if not city.marketplace.built and MG_M:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            city.marketplace.built = True
            buy_building(city.marketplace.name, "fortress")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 12 Blacksmith
    if not city.blacksmith.built and MG_M:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            city.blacksmith.built = True
            buy_building(city.blacksmith.name, "fortress")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 13 City Hall
    if city.city_hall.lvl == 0 and city.blacksmith.built and city.mage_guild.lvl >= 1 and city.marketplace.built and capi:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            city.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(city.city_hall.name, "fortress")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 14 Upg. Gnoll Hut
    if city.creature_dwellings[1-1].lvl==1 and city.city_hall.lvl >= 1 and upg:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][1], player):
            build(city.creature_dwellings[1-1].cost[0][1], player)
            city.creature_dwellings[1-1].lvl=2
            buy_building(city.creature_dwellings[1-1].name, "fortress")
            print('Gnoll Hut upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 15 Upg. Serpent Fly Hive
    if city.creature_dwellings[3-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][1], player):
            build(city.creature_dwellings[3-1].cost[0][1], player)
            city.creature_dwellings[3-1].upgraded = True
            buy_building(city.creature_dwellings[3-1].name, "fortress")
            print('Serpent Fly Hive upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if city.fort.lvl == 2 and wall:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            city.fort.lvl = 3
            buy_building(city.fort.name, "fortress")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Capitol
    if city.city_hall.lvl == 2 and city.fort.lvl == 3 and capi:
        if resourceCheck(city.city_hall.cost[0][2], player):
            build(city.city_hall.cost[0][2], player)
            city.city_hall.lvl = 3
            player.daily_income[0] += 2000
            buy_building(city.city_hall.name, "fortress")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Basilisk Pit
    if city.creature_dwellings[4-1].lvl==0 and city.creature_dwellings[3-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            city.creature_dwellings[4-1].lvl=1
            buy_building(city.creature_dwellings[4-1].name, "fortress")
            print('Basilisk Pit built!')
            return None
        else:
            print('Not enough resources!')

    # 19 Gorgon Lair
    if city.creature_dwellings[5-1].lvl==0 and city.creature_dwellings[3-1].lvl>=1 and city.creature_dwellings[2-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][0], player):
            build(city.creature_dwellings[5-1].cost[0][0], player)
            city.creature_dwellings[5-1].lvl=1
            buy_building(city.creature_dwellings[5-1].name, "fortress")
            print('Gorgon Lair built!')
            return None
        else:
            print('Not enough resources!')

    # 20 Glyphs of Fear
    if not city.glyphs_of_fear.built and city.fort.lvl>=1 and builds:
        if resourceCheck(city.glyphs_of_fear.cost[0], player):
            build(city.glyphs_of_fear.cost[0], player)
            city.glyphs_of_fear.built = True
            buy_building(city.glyphs_of_fear.name, "fortress")
            print("Glyphs of Fear built!")
            return None
        else:
            print('Not enough resources!')

    # 21 Cage of Warlords
    if not city.cage_of_warlords.built and city.glyphs_of_fear.built and city.city_hall.lvl >= 1 and builds:
        if resourceCheck(city.cage_of_warlords.cost[0], player):
            build(city.cage_of_warlords.cost[0], player)
            city.cage_of_warlords.built = True
            buy_building(city.cage_of_warlords.name, "fortress")
            print("Cage of Warlords")
            return None
        else:
            print('Not enough resources!')

    # 22 Mage Guild Level 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            city.mage_guild.lvl = 2
            buy_building(city.mage_guild.name, "fortress")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 23 Mage Guild Level 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            city.mage_guild.lvl = 3
            buy_building(city.mage_guild.name, "fortress")
            print('Mage Guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 24 Upg. Gorgon Lair
    if city.creature_dwellings[5-1].lvl==1 and city.resource_silo.built and upg:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][1], player):
            build(city.creature_dwellings[5-1].cost[0][1], player)
            city.creature_dwellings[5-1].upgraded = True
            buy_building(city.creature_dwellings[5-1].name, "fortress")
            print('Gorgon Lair upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 25 Captains Quarters
    if not city.captains_quarters.built and city.creature_dwellings[1-1].lvl>=1 and builds:
        if resourceCheck(city.captains_quarters.cost[0], player):
            build(city.captains_quarters.cost[0], player)
            city.captains_quarters.built = True
            buy_building(city.captains_quarters.name, "fortress")
            print("Captains Quarters built")
            return None
        else:
            print('Not enough resources!')

    # 26 Upg. Basilisk Pit
    if not city.creature_dwellings[4-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][1], player):
            build(city.creature_dwellings[4-1].cost[0][1], player)
            city.creature_dwellings[4-1].lvl=2
            buy_building(city.creature_dwellings[4-1].name, "fortress")
            print('Basilisk Pit Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 27 Resource Silo
    if not city.resource_silo.built and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            city.resource_silo.built = True
            player.daily_income[1] += 1
            player.daily_income[2] += 1
            buy_building(city.resource_silo.name, "fortress")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 28 Hydra Pond
    if city.creature_dwellings[7-1].lvl==0 and city.creature_dwellings[6-1].lvl>=1 and city.creature_dwellings[4-1].lvl>=1 and hab:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][0], player):
            build(city.creature_dwellings[7-1].cost[0][0], player)
            city.creature_dwellings[7-1].lvl=1
            buy_building(city.creature_dwellings[7-1].name, "fortress")
            print('Hydra Pond built!')
            return None
        else:
            print('Not enough resources!')


    # 29 Upg. Wyvern Nest
    if city.creature_dwellings[6-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][1], player):
            build(city.creature_dwellings[6-1].cost[0][1], player)
            city.creature_dwellings[6-1].lvl=2
            buy_building(city.creature_dwellings[6-1].name, "fortress")
            print('Wyvern Nest upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 30 Upg. Hydra Pond
    if city.creature_dwellings[7-1].lvl==1 and upg:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][1], player):
            build(city.creature_dwellings[7-1].cost[0][1], player)
            city.creature_dwellings[7-1].lvl=2
            buy_building(city.creature_dwellings[7-1].name, "fortress")
            print('Hydra Pond Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 31 Blood Obelisk
    if not city.blood_obelisk.built and city.glyphs_of_fear.built and builds:
        if resourceCheck(city.blood_obelisk.cost[0], player):
            build(city.blood_obelisk.cost[0], player)
            city.blood_obelisk.built = True
            buy_building(city.blood_obelisk.name, "fortress")
            print("Blood Obelisk built!")
            return None
        else:
            print('Not enough resources!')
