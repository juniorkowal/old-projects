from colorama import Fore

from colorama import Fore
from numpy import count_nonzero

from Adventure_AI.AdventureAI_Map_Init import read_map, read_map_from_php_file
from image_processing import screen_slicing
from image_processing.adventure_image_processing import remove_lost_cities, find_heroes, get_cursor_type
import GUI_handling.AdventureGUI
import image_processing.hero_filling
import Adventure_AI.AdventureAI as adv
from GUI_handling.TownGUI import hire_hero
from image_processing.blue_hero import check_if_blue_hero_exists, fill_enemy_hero
from image_processing.screen_slicing import check_resources
from town_upgrading.castle_upgrade import castleUpgrade
from town_upgrading.conflux_upgrade import confluxUpgrade
from town_upgrading.cove_upgrade import coveUpgrade
from town_upgrading.dungeon_upgrade import dungeonUpgrade
from town_upgrading.fortress_upgrade import fortressUpgrade
from town_upgrading.inferno_upgrade import infernoUpgrade
from town_upgrading.necropolis_upgrade import necropolisUpgrade
from town_upgrading.rampart_upgrade import rampartUpgrade
from town_upgrading.stronghold_upgrade import strongholdUpgrade
from town_upgrading.tower_upgrade import towerUpgrade
from data.player_data import Player
from data.hero import Hero, Slot, Slots, SecondarySkills, SecondarySkill
import data.classes_const as creatures
import time
from GUI_handling.AdventureGUI import enter_town, leave_screen, save_in_game
from path_finding_alghoritms.calculate_movments_points_at_start_day import \
    calculate_movments_points_at_start_day as movment
from image_processing.detecting_window import execute_detecting_enemy_turn
import save



#     """
#
#     :param map_obj:
#     :param map_fog:
#     :return:
#     """
#     for y, row in enumerate(map_obj):
#         for x, tile in enumerate(row):
#             value = tile
#             if map_fog[y, x] == 0:
#                 map_obj[y, x] = terrain.fow
#
#             elif value == 0:
#                 map_obj[y, x] = terrain.Obstacle_terr
#             elif value == 1:
#                 map_obj[y, x] = terrain.Grass
#             elif value == 2:
#                 map_obj[y, x] = terrain.Dirt
#             elif value == 8:
#                 map_obj[y, x] = objects.Treasure_Chest


def leave_town():
    """
    someone wanted to have better name for function
    """
    leave_screen()


def read_hero(heroreader, player, n):
    """
    function for reading all available information about our hero

    :param heroreader: heroreader object
    :param player: player object
    :param n: number of hero on list
    """
    GUI_handling.AdventureGUI.press_hero(n)
    time.sleep(0.04)
    heroreader.find_all(player.heroes[n])  # find values of our first hero
    time.sleep(0.04)
    leave_town()
    time.sleep(0.04)


def read_army(heroreader, hero, i):
    """
    function to read army of our hero

    :param heroreader: heroreader object
    :param hero: hero to read
    :param i: number of hero on list
    """
    GUI_handling.AdventureGUI.press_hero(i)
    time.sleep(0.04)
    heroreader.find_units(hero)
    time.sleep(0.04)
    leave_town()
    time.sleep(0.04)


def build_building_in_town(player, city):
    """
    function checks what is the type of our city

    :param player: class Player
    :param city:
    """

    if city.name == "Castle":
        castleUpgrade(player, city)
    if city.name == "Rampart":
        rampartUpgrade(player, city)
    if city.name == "Tower":
        towerUpgrade(player, city)
    if city.name == "Inferno":
        infernoUpgrade(player, city)
    if city.name == "Necropolis":
        necropolisUpgrade(player, city)
    if city.name == "Dungeon":
        dungeonUpgrade(player, city)
    if city.name == "Stronghold":
        strongholdUpgrade(player, city)
    if city.name == "Fortress":
        fortressUpgrade(player, city)
    if city.name == "Conflux":
        confluxUpgrade(player, city)
    if city.name == "Cove":
        coveUpgrade(player, city)


def buy_hero(player, reader, type,advAI):
    """
    function to buy new hero

    :param player: player object
    :param reader: heroreader object
    :param type: type of hero main/not main
    """
    enter_town(0)
    time.sleep(0.1)
    GUI_handling.TownGUI.click_tavern(player.cities[0].name)
    time.sleep(0.1)
    GUI_handling.TownGUI.hire_hero(0)
    hero = Hero(1, type, 'Jenova', 1, 3, 1, 1, Slots(Slot(creatures.Centaur, 21), Slot(creatures.Dwarf, 5),
                                                     Slot(creatures.Wood_Elf, 2)),
                skills=SecondarySkills(SecondarySkill(2, 'Archery', 5)),
                heroclass='might')
    hero.position = (player.cities[0].position)
    advAI.screen.hero_positions.append((hero.position[0],hero.position[1],"Red"))
    player.heroes.append(hero)
    player.gold = player.gold - 2500
    time.sleep(0.1)
    leave_town()
    time.sleep(0.1)
    read_hero(reader, player, len(player.heroes) - 1)
    print("New Hero")
    print(player.heroes[len(player.heroes) - 1])

def check_if_we_need_new_hero(player, mapa, heroreader, advai):
    """
    adaptive function to buy new heroes

    :param player: player object
    :param mapa: map from adventure ai object
    :param heroreader: object containing methods to read all values of hero in game
    """
    after_third_day = (player.month >= 1 and player.week >= 1 and player.day >= 3)
    percent_of_map = count_nonzero(mapa.fog)/(72*72) > 0.25
    three_heroes = len(player.heroes) == 3
    four_heroes = len(player.heroes) == 4
    # buy new hero: if we have less than 2 heroes, if we have less than 3 heroes and is 3 day or later, if we discover
    # 25% on map and we have less than 4 heroes
    if len(player.heroes) < 2 or (after_third_day and not three_heroes and not four_heroes) or (percent_of_map and not four_heroes):
        # Actualize camera to the city position when we need to buy another hero
        player.camera = player.cities[0].position
        if player.heroes[0].herotype == "main":
            type = "not main"
        else:
            type = "main"
        buy_hero(player, heroreader, type,advai)


def main_loop(player, advAI, read_cities, heroreader, after):
    """
    function representing one day in game

    :param player: our player object
    :param advAI: adventure ai object
    :param read_cities: number representing amunt of cities that are read by our ai
    :param heroreader: object containing methods to read all values of hero in game
    :param after: image of hero list after previous turn
    :return: all objects that are changed during turn
    """
    print(Fore.YELLOW, f"########## DAY:{player.day},WEEK:{player.week}, MONTH: {player.month}#########", Fore.RESET)
    if len(player.cities) > read_cities:
        player.logResources()
        for i in range(read_cities - 1, len(player.cities)):
            enter_town(i)
            time.sleep(0.1)
            GUI_handling.TownGUI.click_town_hall(faction=player.cities[i].name)
            time.sleep(0.1)
            player.cities[i].crop_building_names()
            time.sleep(0.5)
            leave_town()
            time.sleep(0.5)
            leave_town()
        read_cities = i
    # Finding all the heroes, blue and red ones
    allTheHeroes = find_heroes(advAI.screen, advAI.map.obj)
    death = image_processing.adventure_image_processing.check_if_hero_is_dead_last_without_hero(after, player)
    if death:
        for hero in player.heroes:
            x, y = hero.position
            pos = (x, y, "Red")
            if pos not in allTheHeroes:
                player.heroes.remove(hero)
    remove_lost_cities(player)
    # Actualize camera to the first hero at the start of the turn
    player.camera = player.heroes[0].position
    check_if_we_need_new_hero(player, advAI.map, heroreader,advAI)
    time.sleep(0.1)
    image_processing.adventure_image_processing.remove_dead_heroes(player)

    # Testing whether detected blue heroes exists at their position
    player.enemies = []
    for x, y, color in allTheHeroes:
        if color == "Blue":
            fill_enemy_hero(player, (x, y))

    ranges = ((player.wood - 5, player.wood + 10),
              (player.mercury - 5, player.mercury + 10), (player.ore - 5, player.ore + 10),
              (player.sulfur - 5, player.sulfur + 10),
              (player.crystal - 5, player.crystal + 10), (player.gems - 5, player.gems + 10),
              (player.gold - 1000, player.gold + 10000))
    screen_slicing.check_resources(player, ranges)
    # Finding whether we lost our mines
    for mine in player.captured_mines:
        # Checking color of the mine at the global map
        # color = image_processing.adventure_image_processing.check_mine_owner_ocr(player, mine.position)[0]
        color = [player.color]  # temporary
        if color[0] != player.color:
            player.captured_mines.remove(mine)

            # Adding lost mine to goals
            # advAI.addLostMineToGoals(mine)

    # if player.week == 1 and player.month == 1:
    player.logResources()
    for i, city in enumerate(player.cities):
        player.camera = city.position
        enter_town(i)
        time.sleep(0.08)
        build_building_in_town(player, city)
        time.sleep(0.08)
        leave_town()
        time.sleep(0.08)
    for i, hero in enumerate(player.heroes):
        advAI.heroPointer = i
        player.camera = hero.position
        GUI_handling.AdventureGUI.press_hero(i)
        time.sleep(0.08)
        read_army(heroreader, hero, i)
        time.sleep(0.08)
        advAI.playHeroDay()
    # else:
    #     for i, hero in enumerate(player.heroes):
    #         GUI_handling.AdventureGUI.press_hero(i)
    #         advAI.heroes[0].mspoints = 1500
    #         advAI.playHeroDay()
    #     for i, city in enumerate(player.cities):
    #         enter_town(i)
    #         time.sleep(0.04)
    #         build_building_in_town(player, city)
    #         time.sleep(0.04)
    #         leave_town()
    after = image_processing.adventure_image_processing.check_if_hero_is_dead_first()
    GUI_handling.AdventureGUI.end_turn()
    player.day += 1
    execute_detecting_enemy_turn(player.heroes[0])
    for row in advAI.map.obj:
        for tile in row:
            if not isinstance(tile, int):
                tile.end_day(player)
    if player.day == 8:
        GUI_handling.AdventureGUI.accept_offer()
        # przelec po wszystkim koniec tygodnia

        player.day = 1
        player.week += 1
        for row in advAI.map.obj:
            for tile in row:
                if not isinstance(tile, int):
                    tile.end_week(player)
        if player.week == 5:
            player.month += 1
            player.week = 1

        # At the end of the week we add all the cities to the adventureAI goals (only if specific castle is not
        # already in the goal list) ---- CamaroTheBOSS
        advAI.addCastlesToGoals()

    # ACTUALIZE HEROES MOVEMENT
    for hero in player.heroes:
        hero.mspoints = movment(hero)
    return player, advAI, read_cities, after


def execute_save(name, advai):
    """
    function for executing save in game and saving of our ai state

    :param name: name of new save
    :param advai: adventure ai object
    """
    save_in_game(name)
    save.save_object(advai, name)


def main(save_name="saved_game"):
    """
    main function reloading saved game or starting new one

    :param save_name: name of saved game to load
    """
    game_active = True
    heroreader = image_processing.hero_filling.Finder()
    try:
        advAI, player = save.load_advai(save_name)
        read_cities = 1
        after = image_processing.adventure_image_processing.check_if_hero_is_dead_first()
    except:
        read_cities = 1
        player = Player('Red', 20000, 20, 20, 10, 10, 10, 10)
        ranges = ((player.wood - 5, player.wood + 10),
                  (player.mercury - 5, player.mercury + 10), (player.ore - 5, player.ore + 10),
                  (player.sulfur - 5, player.sulfur + 10),
                  (player.crystal - 5, player.crystal + 10), (player.gems - 5, player.gems + 10),
                  (player.gold - 1000, player.gold + 10000))
        screen_slicing.check_resources(player, ranges)
        hero = Hero(1, 'main', 'Jenova', 1, 3, 1, 1, Slots(Slot(creatures.Centaur, 21), Slot(creatures.Dwarf, 5),
                                                           Slot(creatures.Wood_Elf, 2)),
                    skills=SecondarySkills(SecondarySkill(2, 'Archery', 5)),
                    heroclass='might')
        ranges = (
            (player.wood - 5, player.wood + 10),
            (player.mercury - 5, player.mercury + 10), (player.ore - 5, player.ore + 10),
            (player.sulfur - 5, player.sulfur + 10), (player.crystal - 5, player.crystal + 10),
            (player.gems - 5, player.gems + 10), (player.gold - 1000, player.gold + 10000))
        screen_slicing.check_resources(player, ranges)
        player.heroes.append(hero)
        advAI = adv.AdventureAI(player, MAP_H3M_PATH)
        allTheHeroes = find_heroes(advAI.screen, advAI.map.obj)
        player.heroes[0].position = (allTheHeroes[0][0], allTheHeroes[0][1])

        advAI.heroPointer = 0
        read_hero(heroreader, player, 0)
        # read_hero(heroreader, player, 0)
        debug = 'a'
        enter_town(0)
        time.sleep(0.1)
        GUI_handling.TownGUI.click_town_hall(faction=player.cities[0].name)
        time.sleep(0.1)
        player.cities[0].crop_building_names()
        time.sleep(0.5)
        leave_town()
        time.sleep(0.5)
        leave_town()
        time.sleep(0.5)
        player.logResources()
        for i, city in enumerate(player.cities):  # In every city we build building
            player.camera = city.position
            enter_town(i)
            time.sleep(0.5)
            build_building_in_town(player, city)
            time.sleep(0.08)
            leave_town()
            time.sleep(0.08)

        enter_town(0)
        time.sleep(0.1)
        player.cities[0].action(player, player.heroes[0])
        time.sleep(0.1)
        enter_town(0)

        time.sleep(0.1)
        # advAI.heroes[0].mspoints = 1900
        # advAI.playHeroDay()
        # enter_town(0)
        # time.sleep(0.04)
        GUI_handling.TownGUI.hero_garrison_change('bottom')
        time.sleep(0.1)
        GUI_handling.TownGUI.click_tavern(player.cities[0].name)
        time.sleep(0.1)
        hire_hero(0)
        player.gold = player.gold - 2500
        # advAI.heroPointer = 1
        time.sleep(0.1)
        GUI_handling.TownGUI.hero_garrison_change('top')
        time.sleep(0.1)
        GUI_handling.TownGUI.move_all_units_to_other_side(1)
        time.sleep(0.1)
        for i in range(8, 16):
            GUI_handling.TownGUI.merge_stacks_unit(i)
            time.sleep(0.1)
        time.sleep(0.1)
        leave_town()
        time.sleep(0.1)
        advAI.heroPointer = 0
        read_hero(heroreader, player, 0)
        advAI.heroes[0].mspoints = movment(advAI.heroes[0])

        advAI.playHeroDay()
        time.sleep(0.1)
        enter_town(0)
        time.sleep(0.1)
        GUI_handling.TownGUI.hero_garrison_change('top')
        time.sleep(0.1)
        leave_town()
        advAI.heroPointer = 1
        player.heroes.append(Hero(1, 'not_main', 'Jenova', 1, 3, 1, 1))
        player.heroes[1].position = (allTheHeroes[0][0], allTheHeroes[0][1])
        player.camera = (allTheHeroes[0][0], allTheHeroes[0][1])
        time.sleep(0.1)
        read_hero(heroreader, player, 1)
        advAI.screen.hero_positions.append((3, 4, "Red"))
        advAI.heroes[1].mspoints = movment(advAI.heroes[1])
        time.sleep(0.1)
        advAI.screen.hero_positions.append((3, 4, 'Red'))
        advAI.playHeroDay()
        time.sleep(0.04)
        GUI_handling.AdventureGUI.end_turn()
        player.day += 1
        waiting = True
        time.sleep(0.3)
        while(waiting):
            cursor = get_cursor_type()
            if cursor == "wait":
                waiting = True
                time.sleep(0.1)
            else:
                waiting = False
        time.sleep(0.3)
        not_end = True
        for hero in player.heroes:
            hero.mspoints = movment(hero)
        after = image_processing.adventure_image_processing.check_if_hero_is_dead_first()
        print(Fore.YELLOW,f"########## DAY:{player.day},WEEK:{player.week}, MONTH: {player.month}#########",Fore.RESET)
    while game_active:
        execute_save(f"saved_game{player.month}{player.week}{player.day}", advAI)
        player, advAI, read_cities, after = main_loop(player, advAI, read_cities, heroreader, after)


if __name__ == '__main__':
    MAP_H3M_PATH = f"C:/GOG Games/HoMM 3 Complete/Maps/h3botmap.h3m"
    MAP_H3M_PATH = input("podaj pelna sciezke do mapy: ")
    saved = input("podaj nazwe wczytanego zapisu (puste dla nowej gry)")
    main(saved)
