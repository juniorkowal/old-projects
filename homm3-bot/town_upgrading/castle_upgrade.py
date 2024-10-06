"""Script containing Castle castle upgrade algorithm"""
from colorama import Fore

from data.building import Cost
from data.player_data import Player
from town_upgrading.choice_generator import town_choice, full_unit_cost
from GUI_handling.TownGUI import buy_building


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


def build(buildingCost, player: Player):
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


def castleUpgrade(player, city):
    """
    Castle castle upgrade algorithm.

    :param player: Player object
    :param city: city object
    :return: None
    """

    print(Fore.LIGHTYELLOW_EX,end="")
    print(f"[TOWN UPGRADING] {city.name}")
    print(f"    [PLAYER GOLD] {player.gold}",Fore.RESET)

    cost = full_unit_cost(city)
    if player.gold < (cost / 3):
        print("Not enough gold for units, don't build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # Tavern
    if not city.tavern.built:
        if resourceCheck(city.tavern.cost[0], player):
            build(city.tavern.cost[0], player)
            city.tavern.built = True
            buy_building(city.tavern.name, "castle")
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
            buy_building(city.fort.name, "castle")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Guardhouse
    if city.creature_dwellings[1 - 1].lvl == 0 and city.fort.lvl > 0:
        if resourceCheck(city.creature_dwellings[1 - 1].cost[0][0], player):
            build(city.creature_dwellings[1 - 1].cost[0][0], player)
            city.creature_dwellings[1 - 1].lvl = 1
            buy_building(city.creature_dwellings[1 - 1].name, "castle")
            print('Guardhouse built!')
            return None
        else:
            print('Not enough resources!')
            return None

            # Archers Tower
    if city.creature_dwellings[2 - 1].lvl == 0 and city.creature_dwellings[1 - 1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[2 - 1].cost[0][0], player):
            build(city.creature_dwellings[2 - 1].cost[0][0], player)
            city.creature_dwellings[2 - 1].lvl = 1
            buy_building(city.creature_dwellings[2 - 1].name, "castle")
            print('Archers Tower built!')
            return None
        else:
            print('Not enough resources!')
            return None

            # Upg. Archers Tower
    if city.creature_dwellings[2 - 1].lvl == 1:
        if resourceCheck(city.creature_dwellings[2 - 1].cost[0][1], player):
            build(city.creature_dwellings[2 - 1].cost[0][1], player)
            city.creature_dwellings[2 - 1].lvl = 2
            buy_building(city.creature_dwellings[2 - 1].name, "castle")
            print('Archers Tower upgraded!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Town Hall
    if city.tavern.built and city.creature_dwellings[2 - 1].lvl >= 1 and city.city_hall.lvl == 0:
        if resourceCheck(city.city_hall.cost[0][0], player):
            build(city.city_hall.cost[0][0], player)
            city.city_hall.lvl = 1
            player.daily_income[0] += 500
            city.city_hall.built = True
            buy_building(city.city_hall.name, "castle")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Blacksmith
    if not city.blacksmith.built:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            city.blacksmith.built = True
            buy_building(city.blacksmith.name, "castle")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Barracks
    if city.creature_dwellings[4 - 1].lvl == 0 and city.creature_dwellings[1 - 1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[4 - 1].cost[0][0], player):
            build(city.creature_dwellings[4 - 1].cost[0][0], player)
            city.creature_dwellings[4 - 1].lvl = 1
            print('Barracks built!')
            buy_building(city.creature_dwellings[4 - 1].name, "castle")
            return None
        else:
            print('Not enough resources!')
            return None

            # Griffin Tower
    if city.creature_dwellings[3 - 1].lvl == 0 and city.creature_dwellings[4 - 1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[3 - 1].cost[0][0], player):
            build(city.creature_dwellings[3 - 1].cost[0][0], player)
            city.creature_dwellings[3 - 1].lvl = 1
            print('Griffin Tower built!')
            buy_building(city.creature_dwellings[3 - 1].name, "castle")
            return None
        else:
            print('Not enough resources!')
            return None

            # Mage Guild Level 1
    if city.mage_guild.lvl == 0 and city.creature_dwellings[3 - 1].lvl >= 1:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            city.mage_guild.lvl = 1
            buy_building(city.mage_guild.name, "castle")
            print('Mage Guild Level 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------
    # Citadel
    if city.fort.lvl == 1 and wall:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            city.fort.lvl = 2
            buy_building(city.fort.name, "castle")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

            # Marketplace
    if not city.marketplace.built and MG_M:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            city.marketplace.built = True
            buy_building(city.marketplace.name, "castle")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # City Hall
    if city.city_hall.lvl == 1 and city.marketplace.built and city.blacksmith.built and city.mage_guild.lvl >= 1:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            city.city_hall.lvl = 2
            player.daily_income[0] += 1000
            buy_building(city.city_hall.name, "castle")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Monastery
    if city.creature_dwellings[5 - 1].lvl == 0 and city.creature_dwellings[1 - 1].lvl >= 1 and city.mage_guild.lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[5 - 1].cost[0][0], player):
            build(city.creature_dwellings[5 - 1].cost[0][0], player)
            city.creature_dwellings[5 - 1].lvl = 1
            buy_building(city.creature_dwellings[5 - 1].name, "castle")
            print('Monastery built!')
            return None
        else:
            print('Not enough resources!')

            # Castle
    if city.fort.lvl == 2 and wall:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            city.fort.lvl = 3
            buy_building(city.fort.name, "castle")
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
            buy_building(city.city_hall.name, "castle")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # Stables
    if not city.stables.built and city.creature_dwellings[1 - 1].lvl == 1 and builds and False:
        if resourceCheck(city.stables.cost[0], player):
            build(city.stables.cost[0], player)
            city.stables.built = True
            buy_building(city.stables.name, "castle")
            print('Stables built!')
            return None
        else:
            print('Not enough resources!')

            # Training Grounds
    if city.stables.built and city.creature_dwellings[6 - 1].lvl == 0 and hab:
        if resourceCheck(city.creature_dwellings[6 - 1].cost[0][0], player):
            build(city.creature_dwellings[6 - 1].cost[0][0], player)
            city.creature_dwellings[6 - 1].lvl = 1
            buy_building(city.creature_dwellings[6 - 1].name, "castle")
            print('Training Grounds built!')
            return None
        else:
            print('Not enough resources!')

            # Mage guild Level 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            city.mage_guild.lvl = 2
            buy_building(city.mage_guild.name, "castle")
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Guardhouse
    if city.creature_dwellings[1 - 1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[1 - 1].cost[0][1], player):
            build(city.creature_dwellings[1 - 1].cost[0][1], player)
            city.creature_dwellings[1 - 1].lvl = 2
            buy_building(city.creature_dwellings[1 - 1].name, "castle")
            print('Guardhouse upgraded !')
            return None
        else:
            print('Not enough resources!')

            # Upg. Griffin Tower
    if city.creature_dwellings[3 - 1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[3 - 1].cost[0][1], player):
            build(city.creature_dwellings[3 - 1].cost[0][1], player)
            city.creature_dwellings[3 - 1].lvl = 2
            buy_building(city.creature_dwellings[3 - 1].name, "castle")
            print('Griffin Tower upgraded!')
            return None
        else:
            print('Not enough resources!')

            # Upg. Barracks
    if city.creature_dwellings[4 - 1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[4 - 1].cost[0][1], player):
            build(city.creature_dwellings[4 - 1].cost[0][1], player)
            city.creature_dwellings[4 - 1].lvl = 2
            buy_building(city.creature_dwellings[4 - 1].name, "castle")
            print('Barracks upgraded!')
            return None
        else:
            print('Not enough resources!')

            # Portal of Glory
    if city.creature_dwellings[6 - 1].lvl >= 1 and city.creature_dwellings[7 - 1].lvl == 0 and city.creature_dwellings[5 - 1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[7 - 1].cost[0][0], player):
            build(city.creature_dwellings[7 - 1].cost[0][0], player)
            city.creature_dwellings[7 - 1].lvl = 1
            buy_building(city.creature_dwellings[7 - 1].name, "castle")
            print('Portal of Glory built!')
            return None
        else:
            print('Not enough resources!')

            # Resource Silo
    if city.resource_silo.built == False and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            city.resource_silo.built = True
            player.daily_income[1] += 1
            player.daily_income[2] += 1
            buy_building(city.resource_silo.name, "castle")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            city.mage_guild.lvl = 3
            buy_building(city.mage_guild.name, "castle")
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

            # Upg. Monastery
    if city.mage_guild.lvl >= 1 and city.creature_dwellings[5 - 1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[5 - 1].cost[0][1], player):
            build(city.creature_dwellings[5 - 1].cost[0][1], player)
            city.creature_dwellings[5 - 1].lvl = 2
            buy_building(city.creature_dwellings[5 - 1].name, "castle")
            print('Monastery upgraded!')
            return None
        else:
            print('Not enough resources!')

            # Griffin Bastion
    if city.creature_dwellings[3 - 1].lvl >= 1 and city.griffin_bastion.built == False and builds:
        if resourceCheck(city.griffin_bastion.cost[0], player):
            build(city.griffin_bastion.cost[0], player)
            city.griffin_bastion.built = True
            buy_building(city.griffin_bastion.name, "castle")
            print('Griffin Bastion built!')
            return None
        else:
            print('Not enough resources!')

    # Brotherhood of The Sword
    if city.tavern.built and city.brotherhood_of_the_sword.built == False and builds:
        if resourceCheck(city.brotherhood_of_the_sword.cost[0], player):
            build(city.brotherhood_of_the_sword.cost[0], player)
            city.brotherhood_of_the_sword.built = True
            buy_building(city.brotherhood_of_the_sword.name, "castle")
            print('Brotherhood of The Sword built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Training Grounds
    if city.creature_dwellings[6 - 1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[6 - 1].cost[0][1], player):
            build(city.creature_dwellings[6 - 1].cost[0][1], player)
            city.creature_dwellings[6 - 1].lvl = 2
            buy_building(city.creature_dwellings[6 - 1].name, "castle")
            print('Training Grounds upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 4
    if city.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][3], player):
            build(city.mage_guild.cost[0][3], player)
            city.mage_guild.lvl = 4
            buy_building(city.mage_guild.name, "castle")
            print('Mage guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Portal of Glory
    if city.creature_dwellings[7 - 1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[7 - 1].cost[0][1], player):
            build(city.creature_dwellings[7 - 1].cost[0][1], player)
            city.creature_dwellings[7 - 1].lvl = 2
            buy_building(city.creature_dwellings[7 - 1].name, "castle")
            print('Portal of Glory upgraded!')
            return None
        else:
            print('Not enough resources!')
