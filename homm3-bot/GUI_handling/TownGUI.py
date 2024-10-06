import time
import keyboard as kb
import mouse
"""Script containing functions essential for handling town GUI."""

def move_mouse_and_click(x: int, y: int):
    """
    move mouse and click

    :param x: x coordinate
    :param y: y coordinate
    """
    mouse.move(x, y, duration=0)
    time.sleep(0.1)
    mouse.click()


def hero_garrison_change(garrison: str = 'bottom'):
    """
    change hero in garrison if the opposite garrison is empty
    Changed it because for some reason space button sometimes doesn't click

    :param garrison: Indicates whether to move starting from top or bottom
    """
    if garrison == 'bottom':
        coords_from = (830, 750)
        coords_to = (830, 650)
    else:
        coords_from = (830, 650)
        coords_to = (830, 750)
    time.sleep(0.1)
    move_mouse_and_click(coords_from[0], coords_from[1])
    time.sleep(0.2)
    move_mouse_and_click(coords_to[0], coords_to[1])
    time.sleep(0.2)



def click_building(id):
    """
    click on a building

    :param id: Building number
    """
    if 0 > id > 18:
        print("Id should be within (0, 18)")
        return
    mouse.move(830 + 62 * (id % 8), 660 + 100 * (id / 8), duration=0)
    time.sleep(0.1)
    mouse.click()


def click_tile(tile_num):
    """
    Click on a tile
    0-7 upper row, 8-15 lower row

    :param tile_num: Unit number
    """
    if 0 <= tile_num <= 15:
        move_mouse_and_click(830 + 62 * (tile_num % 8), 660 + 100 * int(tile_num / 8))
    else:
        print("Tile number should be within 0-15")


def change_tile_unit(tile_num1, tile_num2):
    """
    change units tile

    :param tile_num1: Unit number
    :param tile_num2: Unit number
    """
    click_tile(tile_num1)
    click_tile(tile_num2)


def double_click_tile(tile_num):
    """
    double click on a tile

    :param tile_num: Unit number
    """
    click_tile(tile_num)
    click_tile(tile_num)


def upgrade_unit(tile_num):
    """
    upgrade unit

    :param tile_num: Unit number
    """
    double_click_tile(tile_num)
    time.sleep(0.1)
    move_mouse_and_click(881, 465)
    time.sleep(0.1)
    kb.send('enter')


def make_single_stack_unit(tile_num):
    """
    take positions of unit and make it into a single stack

    :param tile_num: Unit number
    """
    kb.press("ctrl")
    click_tile(tile_num)
    time.sleep(0.1)
    kb.release("ctrl")


def merge_stacks_unit(tile_num):
    """
    merge stacks

    :param tile_num: Unit number
    """
    kb.press("left alt")
    click_tile(tile_num)
    time.sleep(0.1)
    kb.release("left alt")


def split_even_unit(tile_num):
    """
    split units evenly

    :param tile_num: Unit number
    """
    kb.press("shift")
    click_tile(tile_num)
    time.sleep(0.1)
    kb.release("shift")


def move_all_units_to_other_side(tile_num: object):
    """
    Moves every unit except if it moves from a hero.
    Then it moves every unit but one chosen, so the hero is left with 1 stack of 1 unit

    :param tile_num: Tile number deciding which one unit will stay if taking army from a hero
    """
    kb.press("ctrl+alt+shift")
    click_tile(tile_num)
    time.sleep(0.1)
    kb.release("ctrl+alt+shift")


def dismiss_unit(tile_num: object):
    """
    dismiss a unit

    :param tile_num: Our tile number
    """
    kb.press("alt+shift")
    click_tile(tile_num)
    time.sleep(0.1)
    kb.release("alt+shift")
    kb.send("enter")


# TODO: Amount not implemented yet
def recruit_unit(tier: str, upgraded=None, amount=None):
    """
    Buys every unit chosen. tier=8 is the additional unit from the 'Portal of summoning' in Dungeon.
    Buy multiple units using '+' e.g. tier='1+2+3', or using tier='all' -> amount is not used then.
    Can also specify the amount of units bought, if not specified it buys every unit in the given order:
    e.g. tier='4+1+2' will buy every unit of tier 4 then 1 then 2 if there's enough resources.
    If you only have e.g. 3 tiers (1, 2, 6) then to buy the 6th one you have to write 3 as it's the 3rd bought
    !!!If buying a certain amount, then it has to be written as '10+2+3+...' and has to have the same amount
    of specified numbers as the amount of tiers bought!!!
    amount=-1 is equivalent to buying every unit.
    Normally buys upgraded units but can also buy unupgraded by setting upgraded=False
    If you buy more than one tier and want some units unupgraded than it is necessary to specify each of them
    as upgraded=[True, False, True,...]. If all units are to be upgraded than no input is necessary.

    :param tier: Unit tier
    :param upgraded: True/False
    :param amount: amount to buy
    """

    tier = tier.strip()  # Remove all accidental whitespaces
    tier_split = tier.split('+')
    if upgraded is None:
        upgraded = []
        for _ in tier_split:
            upgraded.append(True)

    if amount is None:
        amount = ''
        count = len(tier_split)
        for i in range(count):
            if i != count-1:
                amount += '-1+'
            else:
                amount += '-1'
    amount = amount.replace(" ", "")
    amount_split = amount.split('+')

    if len(tier_split) != len(amount_split) != len(upgraded):
        print("The number of given amount and upgrades must be the same as the amount of bought tiers")
        return

    for tier, upgrade, amount in zip(tier_split, upgraded, amount_split):
        amount = int(amount)
        if upgrade:
            main_button = 'ctrl'
        else:
            main_button = 'alt'

        if tier != 'all':
            kb.press(main_button)
            move_mouse_and_click(600 + 50 * (int(tier) % 5) - 50, 715 + 50 * int(int(tier) / 5))
            time.sleep(0.1)
            kb.release(main_button)
        else:
            kb.send(main_button, do_press=True, do_release=False)
            #kb.release(main_button)
            #while not kb.is_pressed(main_button):
                #print(kb.is_pressed(main_button))
                #time.sleep(0.1)
            move_mouse_and_click(700, 670)
            time.sleep(0.1)
            kb.send(main_button, do_press=False, do_release=True)
            break


def click_town_hall(faction: str):
    """
    Click on town hall Don't use

    :param faction: Your faction
    """
    faction = faction.lower()
    if faction not in {'castle', 'rampart', 'tower', 'inferno', 'necropolis',
                       'dungeon', 'stronghold', 'fortress', 'conflux', 'cove'}:
        print('Wrong faction name')
        return
    if faction == 'castle':
        move_mouse_and_click(690, 500)
    elif faction == 'rampart':
        move_mouse_and_click(1230, 525)
    elif faction == 'tower':
        move_mouse_and_click(660, 535)
    elif faction == 'inferno':
        move_mouse_and_click(650, 450)
    elif faction == 'necropolis':
        move_mouse_and_click(1100, 370)
    elif faction == 'dungeon':
        move_mouse_and_click(650, 500)
    elif faction == 'stronghold':
        move_mouse_and_click(680, 560)
    elif faction == 'fortress':
        move_mouse_and_click(870, 380)
    elif faction == 'conflux':
        move_mouse_and_click(670, 530)
    elif faction == 'cove':
        move_mouse_and_click(660, 450)


def buy_generic_building(name: str):
    """
    buy a building don't use

    :param name: Name of the building
    """
    if name == 'town_hall' or name == 'city_hall' or name == 'capitol':
        move_mouse_and_click(660, 310)
    elif name == 'fort' or name == 'citadel' or name == 'castle':
        move_mouse_and_click(860, 310)
    elif name == 'tavern':
        move_mouse_and_click(1050, 310)
    elif name == 'blacksmith':
        move_mouse_and_click(1250, 310)
    elif name == 't1':
        move_mouse_and_click(660, 630)
    elif name == 't2':
        move_mouse_and_click(860, 630)
    elif name == 't3':
        move_mouse_and_click(1050, 630)
    elif name == 't4':
        move_mouse_and_click(1250, 630)
    elif name == 't5':
        move_mouse_and_click(760, 730)
    elif name == 't6':
        move_mouse_and_click(960, 730)
    elif name == 't7':
        move_mouse_and_click(1150, 730)


def buy_marketplace(faction):
    """
    don't use

    :param faction: Your faction
    """
    if faction in {'castle', 'fortress', 'rampart', }:
        move_mouse_and_click(760, 420)
    else:
        move_mouse_and_click(670, 420)


def buy_mage_guild(faction):
    """
    dont touch

    :param faction: Your faction
    """
    if faction in {'castle', 'fortress', 'rampart', }:
        move_mouse_and_click(960, 420)
    else:
        move_mouse_and_click(860, 420)


def buy_shipyard(faction):
    """
    dont use

    :param faction: Your faction
    :return:
    """
    if faction not in {'castle', 'cove', 'conflux', 'fortress', 'necropolis'}:
        print("This faction can't build a shipyard")
        return
    elif faction in {'castle', 'fortress'}:
        move_mouse_and_click(1150, 420)
    elif faction == 'cove':
        move_mouse_and_click(1050, 420)
    else:
        move_mouse_and_click(1250, 420)


def buy_building_castle(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'brotherhood_of_the_sword':
        move_mouse_and_click(1050, 310)
    elif name == 'stables':
        move_mouse_and_click(860, 530)
    elif name == 'griffin_bastion':
        move_mouse_and_click(1050, 530)
    elif name == 'lighthouse':
        move_mouse_and_click(1150, 420)


def buy_building_rampart(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name in {'mystic_pond', 'fountain_of_fortune'}:
        move_mouse_and_click(1150, 420)
    elif name == 'dendroid_saplings':
        move_mouse_and_click(960, 530)
    elif name == 'treasury':
        move_mouse_and_click(760, 530)
    elif name in {"miners' guild", 'miners_guild'}:
        move_mouse_and_click(1150, 530)


def buy_building_tower(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'library':
        move_mouse_and_click(1050, 420)
    elif name == 'wall_of_knowledge':
        move_mouse_and_click(1250, 420)
    elif name in {'sculptors_wings', "sculptor's wings"}:
        move_mouse_and_click(1150, 530)
    elif name == 'artifact_merchants':
        move_mouse_and_click(760, 530)
    elif name == 'lookout_tower':
        move_mouse_and_click(960, 530)


def buy_building_inferno(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'order_of_fire':
        move_mouse_and_click(1050, 420)
    elif name == 'brimstone_stormclouds':
        move_mouse_and_click(1250, 420)
    elif name == 'birthing_pools':
        move_mouse_and_click(960, 530)
    elif name == 'cages':
        move_mouse_and_click(1150, 530)
    elif name == 'castle_gate':
        move_mouse_and_click(760, 530)


def buy_building_necropolis(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'necromancy_amplifier':
        move_mouse_and_click(1050, 420)
    elif name == 'cover_of_darkness':
        move_mouse_and_click(760, 530)
    elif name == 'skeleton_transformer':
        move_mouse_and_click(960, 530)
    elif name == 'unearthed_graves':
        move_mouse_and_click(1150, 530)


def buy_building_dungeon(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'mana_vortex':
        move_mouse_and_click(1050, 420)
    elif name == 'portal_of_summoning':
        move_mouse_and_click(1250, 420)
    elif name == 'artifact_merchants':
        move_mouse_and_click(760, 530)
    elif name == 'battle_scholar_academy':
        move_mouse_and_click(960, 530)
    elif name == 'mushroom_rings':
        move_mouse_and_click(1150, 530)


def buy_building_stronghold(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'hall_of_valhalla':
        move_mouse_and_click(1050, 420)
    elif name == 'escape_tunnel':
        move_mouse_and_click(1250, 420)
    elif name in {'freelancers_guild', "freelancer's guild"}:
        move_mouse_and_click(760, 530)
    elif name == 'ballista_yard':
        move_mouse_and_click(960, 530)
    elif name == 'mess_hall':
        move_mouse_and_click(1150, 530)


def buy_building_fortress(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'cage_of_warlords':
        move_mouse_and_click(760, 530)
    if name in {'glyphs_of_fear', 'blood_obelisk'}:
        move_mouse_and_click(960, 530)
    if name in {'captains_quarters', "captain's quarters"}:
        move_mouse_and_click(1150, 530)


def buy_building_conflux(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name == 'magic_university':
        move_mouse_and_click(1050, 420)
    elif name == 'artifact_merchants':
        move_mouse_and_click(760, 530)
    elif name == 'vault_of_ashes':
        move_mouse_and_click(960, 530)
    elif name == 'garden_of_life':
        move_mouse_and_click(1150, 530)


def buy_building_cove(name: str):
    """
    buy building

    :param name: Name of the building
    """
    if name in {'thieves_guild', "thieves' guild"}:
        move_mouse_and_click(1250, 420)
    elif name == 'pub':
        move_mouse_and_click(760, 530)
    elif name == 'grotto':
        move_mouse_and_click(960, 530)
    elif name == 'roost':
        move_mouse_and_click(1150, 530)


def buy_building(name: str, faction: str):
    """
    Actual function please don't use anything to build other than this
    The generic function that should be used to buy everything

    :param name: name of the building
    :param faction: your current faction
    """
    faction = faction.lower()
    name = name.lower()
    if faction not in {'castle', 'rampart', 'tower', 'inferno', 'necropolis',
                       'dungeon', 'stronghold', 'fortress', 'conflux', 'cove'}:
        print('Wrong faction name')
        return

    click_town_hall(faction)

    if name in {'town_hall', 'city_hall', 'capitol', 'fort', 'citadel', 'castle', 'blacksmith', 'tavern',
                't1', 't2', 't3', 't4', 't5', 't6', 't7'}:
        buy_generic_building(name)

    elif name in ('marketplace', 'resource_silo'):
        buy_marketplace(faction)

    elif name == 'mage_guild':
        buy_mage_guild(faction)

    elif name == 'shipyard':
        buy_shipyard(faction)

    elif faction == 'castle':
        buy_building_castle(name)

    elif faction == 'rampart':
        buy_building_rampart(name)

    elif faction == 'tower':
        buy_building_tower(name)

    elif faction == 'inferno':
        buy_building_inferno(name)

    elif faction == 'necropolis':
        buy_building_necropolis(name)

    elif faction == 'dungeon':
        buy_building_dungeon(name)

    elif faction == 'stronghold':
        buy_building_stronghold(name)

    elif faction == 'fortress':
        buy_building_fortress(name)

    elif faction == 'conflux':
        buy_building_conflux(name)

    elif faction == 'cove':
        buy_building_cove(name)
    time.sleep(0.3)
    mouse.click()
    time.sleep(0.3)
    kb.send('enter')
    time.sleep(2)


def click_tavern(faction):
    """
    click tavern

    :param faction: your current faction
    """
    faction = faction.lower()
    if faction not in {'castle', 'rampart', 'tower', 'inferno', 'necropolis',
                       'dungeon', 'stronghold', 'fortress', 'conflux', 'cove'}:
        print('Wrong faction name')
        return

    if faction == 'castle':
        move_mouse_and_click(585, 530)
    if faction == 'rampart':
        move_mouse_and_click(825, 500)
    if faction == 'tower':
        move_mouse_and_click(1000, 580)
    if faction == 'inferno':
        move_mouse_and_click(700, 500)
    if faction == 'necropolis':
        move_mouse_and_click(1160, 450)
    if faction == 'dungeon':
        move_mouse_and_click(810, 570)
    if faction == 'stronghold':
        move_mouse_and_click(820, 560)
    if faction == 'fortress':
        move_mouse_and_click(1315, 510)
    if faction == 'conflux':
        move_mouse_and_click(1150, 500)
    if faction == 'cove':
        move_mouse_and_click(630, 560)


def click_mage_guild(faction):
    """
    click on the mage guild

    :param faction: your current faction
    """
    faction = faction.lower()
    if faction not in {'castle', 'rampart', 'tower', 'inferno', 'necropolis',
                       'dungeon', 'stronghold', 'fortress', 'conflux', 'cove'}:
        print('Wrong faction name')
        return

    if faction == 'castle':
        move_mouse_and_click(1320, 480)
    if faction == 'rampart':
        move_mouse_and_click(1100, 500)
    if faction == 'tower':
        move_mouse_and_click(1233, 432)
    if faction == 'inferno':
        move_mouse_and_click(1300, 440)
    if faction == 'necropolis':
        move_mouse_and_click(970, 380)
    if faction == 'dungeon':
        move_mouse_and_click(770, 420)
    if faction == 'stronghold':
        move_mouse_and_click(1085, 335)
    if faction == 'fortress':
        move_mouse_and_click(615, 490)
    if faction == 'conflux':
        move_mouse_and_click(820, 490)
    if faction == 'cove':
        move_mouse_and_click(930, 400)


def click_blacksmith(faction):
    """
    click on the blacksmith

    :param faction: your current faction
    """
    faction = faction.lower()
    if faction not in {'castle', 'rampart', 'tower', 'inferno', 'necropolis',
                       'dungeon', 'stronghold', 'fortress', 'conflux', 'cove'}:
        print('Wrong faction name')
        return

    if faction == 'castle':
        move_mouse_and_click(865, 560)
    if faction == 'rampart':
        move_mouse_and_click(1210, 405)
    if faction == 'tower':
        move_mouse_and_click(1100, 560)
    if faction == 'inferno':
        move_mouse_and_click(1300, 580)
    if faction == 'necropolis':
        move_mouse_and_click(995, 525)
    if faction == 'dungeon':
        move_mouse_and_click(1145, 540)
    if faction == 'stronghold':
        move_mouse_and_click(1280, 570)
    if faction == 'fortress':
        move_mouse_and_click(960, 450)
    if faction == 'conflux':
        move_mouse_and_click(1060, 470)
    if faction == 'cove':
        move_mouse_and_click(1290, 565)


def click_magic(tier: int, id: int):
    """
    click on magic

    :param tier: magic tier 1-5
    :param id: number of spell left to right, top to bottom
    """
    if tier == 1:
        mouse.move(815 + 95*id, 715, duration=0)
        time.sleep(0.1)
        mouse.click()
    elif tier == 2:
        mouse.move(650, 320 + 95*id, duration=0)
        time.sleep(0.1)
        mouse.click()
    elif tier == 3:
        mouse.move(1170 + 105*(id % 2), 350 + 75*int(id/2), duration=0)
        time.sleep(0.1)
        mouse.click()
    elif tier == 4:
        mouse.move(782, 310 + 100*id, duration=0)
        time.sleep(0.1)
        mouse.click()
    elif tier == 5:
        mouse.move(1090 + 100*id, 590, duration=0)
        time.sleep(0.1)
        mouse.click()


def click_artifact_merchant(faction):
    """
    click on artifact merchant

    :param faction: your current faction
    """
    faction = faction.lower()
    if faction not in {'tower', 'dungeon', 'conflux'}:
        print('Wrong faction name')
        return

    if faction == 'tower':
        move_mouse_and_click(1260, 560)
    if faction == 'dungeon':
        move_mouse_and_click(1330, 580)
    if faction == 'conflux':
        move_mouse_and_click(885, 535)


def use_castle_gate(id):
    """
    Use castle gate
    Inferno only

    :param id: number of the town you go to
    """
    move_mouse_and_click(820, 424)
    move_mouse_and_click(880, 436 + 32*id)
    kb.send('enter')


def transform_skeleton(id: str):
    """
    Transform skeletons
    Necropolis only. id='all' for every unit, write id as id='1+3+5+...' otherwise

    :param id: id of units to change from left to right
    """
    move_mouse_and_click(850, 530)
    id = id.replace(" ", "")  # Remove all accidental whitespaces
    id_split = id.split('+')

    for i in id_split:
        if i == 'all':
            move_mouse_and_click(830, 740)
            break
        temp = int(i)
        if temp == 7:
            move_mouse_and_click(815, 645)
            move_mouse_and_click(815 + 290, 645)
            continue

        move_mouse_and_click(732 + 85*(temp % 3), 448 + 100*int(temp/3))
        move_mouse_and_click(732 + 290, 448)
    move_mouse_and_click(960, 740)
    kb.send('esc')


def buy_ballista_from_yard():
    """
    Stronghold only
    """
    move_mouse_and_click(1210, 585)


def use_freelancers_guild(unit_id: int, resource_id: int, amount: int):
    """Stronghold only

    :param unit_id: unit id left to right 1-7
    :param resource_id: left to right and top to bottom
    :param amount: amount of units to sell
    """
    move_mouse_and_click(1870, 560)

    if unit_id == 7:
        move_mouse_and_click(815, 600)
    else:
        move_mouse_and_click(730 + 85*(unit_id % 3), 400 + 95*int(unit_id/3))

    if resource_id == 7:
        move_mouse_and_click(1100, 600)
    else:
        move_mouse_and_click(1020 + 80*(resource_id % 3), 450 + 80*int(resource_id/3))
    mouse.move(1020, 740, duration=0)
    time.sleep(0.1)
    while amount > 0:
        mouse.click()
        time.sleep(0.1)
        amount -= 1
    move_mouse_and_click(1000, 780)


def learn_elemental_magic_town(name):
    """
    Conflux only. Can chain buy by using + name='air+water+...
    Learn elemental magic conflux only

    :param name: one of 'fire', 'water', 'earth', 'air' or added together with a +
    """
    name = name.lower()
    if name not in {'fire', 'water', 'earth', 'air'}:
        print("Arguments can be: 'fire', 'water', 'earth', 'air'")
    move_mouse_and_click(755, 470)

    name = name.replace(" ", "")  # Remove all accidental whitespaces
    name_split = name.split('+')

    for n in name_split:
        if n == 'fire':
            move_mouse_and_click(800, 600)
            move_mouse_and_click(900, 660)
        elif n == 'air':
            move_mouse_and_click(900, 600)
            move_mouse_and_click(900, 660)
        elif n == 'water':
            move_mouse_and_click(1000, 600)
            move_mouse_and_click(900, 660)
        else:
            move_mouse_and_click(1100, 600)
            move_mouse_and_click(900, 660)


def hire_hero(id: int):
    """
    Hires a hero in a tavern,

    :param id: id=0 hires the left one, id=1 hires the right one
    """
    if id == 0:
        move_mouse_and_click(865, 620)
    elif id == 1:
        move_mouse_and_click(950, 620)
    else:
        print("Id can be either 0 or 1.")
    kb.send('enter')
