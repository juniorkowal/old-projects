"""Script containing Dungeon castle upgrade algorithm"""
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


def dungeonUpgrade(player: Player, city):
    """
    Dungeon castle upgrade algorithm.
    :param player: Player object
    :param city: Dungeon object
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
            buy_building(city.tavern.name, "dungeon")
            city.tavern.built = True
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort
    if city.tavern.built and city.fort.lvl < 1:
        if resourceCheck(city.fort.cost[0][0], player):
            build(city.fort.cost[0][0], player)
            buy_building(city.fort.name, "dungeon")
            city.fort.built = True
            city.fort.lvl = 1
            print('Fort Level 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Warren
    if city.fort.lvl == 1 and city.creature_dwellings[1-1].lvl == 0:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][0], player):
            build(city.creature_dwellings[1-1].cost[0][0], player)
            buy_building(city.creature_dwellings[1-1].name, "dungeon")
            city.creature_dwellings[1-1].lvl = 1
            print('Warren built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Pillar of Eyes
    if city.creature_dwellings[3-1].lvl == 0 and city.creature_dwellings[1-1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][0], player):
            build(city.creature_dwellings[3-1].cost[0][0], player)
            buy_building(city.creature_dwellings[3-1].name, "dungeon")
            city.creature_dwellings[3-1].lvl = 1
            print('Pillar of Eyes built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Harpy Loft
    if city.creature_dwellings[2-1].lvl == 0 and city.creature_dwellings[3-1].lvl >= 1:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][0], player):
            build(city.creature_dwellings[2-1].cost[0][0], player)
            buy_building(city.creature_dwellings[2-1].name, "dungeon")
            city.creature_dwellings[2-1].lvl = 1
            print('Harpy Loft built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Town Hall
    if city.city_hall.lvl <= 0:
        if resourceCheck(city.city_hall.cost[0][0], player):
            build(city.city_hall.cost[0][0], player)
            buy_building(city.city_hall.name, "dungeon")
            city.city_hall.lvl = 1
            player.daily_income[0] += 500
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Mage Guild Level 1
    if city.mage_guild.lvl < 1:
        if resourceCheck(city.mage_guild.cost[0][0], player):
            build(city.mage_guild.cost[0][0], player)
            buy_building(city.mage_guild.name, "dungeon")
            city.mage_guild.lvl = 1
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Marketplace
    if city.mage_guild.lvl >= 1 and not city.marketplace.built:
        if resourceCheck(city.marketplace.cost[0], player):
            build(city.marketplace.cost[0], player)
            buy_building(city.marketplace.name, "dungeon")
            city.marketplace.built = True
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, city)

    # ------------------------------------------------------------------------------------------
    # 9 Blacksmith
    if not city.blacksmith.built and MG_M:
        if resourceCheck(city.blacksmith.cost[0], player):
            build(city.blacksmith.cost[0], player)
            buy_building(city.blacksmith.name, "dungeon")
            city.blacksmith.built = True
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 10 City Hall
    if city.city_hall.lvl == 1 and city.marketplace.built and city.blacksmith.built and city.mage_guild.lvl >= 1 and capi:
        if resourceCheck(city.city_hall.cost[0][1], player):
            build(city.city_hall.cost[0][1], player)
            buy_building(city.city_hall.name, "dungeon")
            city.city_hall.lvl = 2
            player.daily_income[0] += 1000
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 11 Upg. Pillar of Eyes
    if city.creature_dwellings[3-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[3-1].cost[0][1], player):
            build(city.creature_dwellings[3-1].cost[0][1], player)
            buy_building(city.creature_dwellings[3-1].name, "dungeon")
            city.creature_dwellings[3-1].lvl = 2
            print('Pillar of Eyes upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 12 Citadel
    if city.fort.lvl == 1 and wall:
        if resourceCheck(city.fort.cost[0][1], player):
            build(city.fort.cost[0][1], player)
            buy_building(city.fort.name, "dungeon")
            city.fort.lvl = 2
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Upg. Harpy Loft
    if city.creature_dwellings[2-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[2-1].cost[0][1], player):
            build(city.creature_dwellings[2-1].cost[0][1], player)
            buy_building(city.creature_dwellings[2-1].name, "dungeon")
            city.creature_dwellings[2-1].lvl = 2
            print('Harpy Loft upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 14 Chapel of Stilled Voices
    if city.creature_dwellings[4-1].lvl == 0 and city.creature_dwellings[2-1].lvl >= 1 and city.creature_dwellings[3-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][0], player):
            build(city.creature_dwellings[4-1].cost[0][0], player)
            buy_building(city.creature_dwellings[4-1].name, "dungeon")
            city.creature_dwellings[4-1].lvl = 1
            print('Chapel of Stilled Voices built!')
            return None
        else:
            print('Not enough resources!')

    # 15 Labyrinth
    if city.creature_dwellings[5-1].lvl == 0 and city.creature_dwellings[4-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][0], player):
            build(city.creature_dwellings[5-1].cost[0][0], player)
            buy_building(city.creature_dwellings[5-1].name, "dungeon")
            city.creature_dwellings[5-1].lvl = 1
            print('Labyrinth built!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if city.fort.lvl == 2 and wall:
        if resourceCheck(city.fort.cost[0][2], player):
            build(city.fort.cost[0][2], player)
            buy_building(city.fort.name, "dungeon")
            city.fort.lvl = 3
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Capitol
    if city.city_hall.lvl == 2 and city.fort.lvl == 3 and capi:
        if resourceCheck(city.city_hall.cost[0][2], player):
            build(city.city_hall.cost[0][2], player)
            buy_building(city.city_hall.name, "dungeon")
            city.city_hall.lvl = 3
            player.daily_income[0] += 2000
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Manticore Lair
    if city.creature_dwellings[6-1].lvl == 0 and city.creature_dwellings[4-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][0], player):
            build(city.creature_dwellings[6-1].cost[0][0], player)
            buy_building(city.creature_dwellings[6-1].name, "dungeon")
            city.creature_dwellings[6-1].lvl = 1
            print('Manticore Lair built!')
            return None
        else:
            print('Not enough resources!')

    # 19 Mage guild Level 2
    if city.mage_guild.lvl == 1 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][1], player):
            build(city.mage_guild.cost[0][1], player)
            buy_building(city.mage_guild.name, "dungeon")
            city.mage_guild.lvl = 2
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 20 Mage guild Level 3
    if city.mage_guild.lvl == 2 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][2], player):
            build(city.mage_guild.cost[0][2], player)
            buy_building(city.mage_guild.name, "dungeon")
            city.mage_guild.lvl = 3
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 21 Upg. Warren
    if city.creature_dwellings[1-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[1-1].cost[0][1], player):
            build(city.creature_dwellings[1-1].cost[0][1], player)
            buy_building(city.creature_dwellings[1-1].name, "dungeon")
            city.creature_dwellings[1-1].lvl = 2
            print('Warren upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 22 Mage guild Level 4
    if city.mage_guild.lvl == 3 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][3], player):
            build(city.mage_guild.cost[0][3], player)
            buy_building(city.mage_guild.name, "dungeon")
            city.mage_guild.lvl = 4
            print('Mage guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # 23 Battle Scholar Academy
    if not city.battle_scholar_academy.built and builds and False:
        if resourceCheck(city.battle_scholar_academy.cost[0], player):
            build(city.battle_scholar_academy.cost[0], player)
            buy_building(city.battle_scholar_academy.name, "dungeon")
            city.battle_scholar_academy.built = True
            print('Battle Scholar Academy built!')
            return None
        else:
            print('Not enough resources!')

    # 24 Upg. Chapel of Stilled Voices
    if city.creature_dwellings[4-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[4-1].cost[0][1], player):
            build(city.creature_dwellings[4-1].cost[0][1], player)
            buy_building(city.creature_dwellings[4-1].name, "dungeon")
            city.creature_dwellings[4-1].lvl = 2
            print('Chapel of Stilled Voices upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 25 Dragon Cave
    if city.creature_dwellings[7-1].lvl == 0 and city.mage_guild.lvl >= 2 and city.creature_dwellings[6-1].lvl >= 1 and hab:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][0], player):
            build(city.creature_dwellings[7-1].cost[0][0], player)
            buy_building(city.creature_dwellings[7-1].name, "dungeon")
            city.creature_dwellings[7-1].lvl = 1
            print('Dragon Cave built!')
            return None
        else:
            print('Not enough resources!')

    # 26 Upg. Labyrinth
    if city.creature_dwellings[5-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[5-1].cost[0][1], player):
            build(city.creature_dwellings[5-1].cost[0][1], player)
            buy_building(city.creature_dwellings[5-1].name, "dungeon")
            city.creature_dwellings[5-1].lvl = 2
            print('Labyrinth upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 27 Upg. Manticore Lair
    if city.creature_dwellings[6-1].lvl == 1 and upg:
        if resourceCheck(city.creature_dwellings[6-1].cost[0][1], player):
            build(city.creature_dwellings[6-1].cost[0][1], player)
            buy_building(city.creature_dwellings[6-1].name, "dungeon")
            city.creature_dwellings[6-1].lvl = 2
            print('Manticore Lair upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 28 Mage Guild Level 5
    if city.mage_guild.lvl == 4 and MG_M:
        if resourceCheck(city.mage_guild.cost[0][4], player):
            build(city.mage_guild.cost[0][4], player)
            buy_building(city.mage_guild.name, "dungeon")
            city.mage_guild.lvl = 5
            print('Mage Guild Level 5!')
            return None
        else:
            print('Not enough resources!')

    # 29 Upg. Dragon Cave
    if city.creature_dwellings[7-1].lvl == 1 and city.mage_guild.lvl >= 3 and upg:
        if resourceCheck(city.creature_dwellings[7-1].cost[0][1], player):
            build(city.creature_dwellings[7-1].cost[0][1], player)
            buy_building(city.creature_dwellings[7-1].name, "dungeon")
            city.creature_dwellings[7-1].lvl = 2
            print('Upg. Dragon Cave upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 30 Portal of Summoning
    if not city.portal_of_summoning.built and builds:
        if resourceCheck(city.portal_of_summoning.cost[0], player):
            build(city.portal_of_summoning.cost[0], player)
            buy_building(city.portal_of_summoning.name, "dungeon")
            city.portal_of_summoning.built = True
            print('Portal of Summoning built')
            return None
        else:
            print('Not enough resources!')

    # 31 Mana Vortex
    if not city.mana_vortex.built and city.mage_guild.lvl>=1 and builds:
        if resourceCheck(city.mana_vortex.cost[0], player):
            build(city.mana_vortex.cost[0], player)
            buy_building(city.mana_vortex.name, "dungeon")
            city.mana_vortex.built = True
            print('Mana Vortex built')
            return None
        else:
            print('Not enough resources!')

    # 32 Mushroom Rings
    if not city.mushroom_rings.built and city.creature_dwellings[1-1].lvl >= 1 and builds:
        if resourceCheck(city.mushroom_rings.cost[0], player):
            build(city.mushroom_rings.cost[0], player)
            buy_building(city.mushroom_rings.name, "dungeon")
            city.mushroom_rings.built = True
            print("Mushroom Rings built")
            return None
        else:
            print('Not enough resources!')

    # 33 Resource Silo
    if not city.resource_silo.built and city.marketplace.built:
        if resourceCheck(city.resource_silo.cost[0], player):
            build(city.resource_silo.cost[0], player)
            buy_building(city.resource_silo.name, "dungeon")
            city.resource_silo.built = True
            player.daily_income[4] += 1
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 34 Artifact Merchants
    if not city.artifact_merchant.built and city.marketplace.built and builds:
        if resourceCheck(city.artifact_merchant.cost[0], player):
            build(city.artifact_merchant.cost[0], player)
            buy_building(city.artifact_merchant.name, "dungeon")
            city.artifact_merchant.built = True
            print("Artifact Merchants built")
            return None
        else:
            print('Not enough resources!')
