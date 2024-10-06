"""Script containing functions essential for handling  adventure GUI."""
import time
import keyboard as kb
import mouse
import image_processing.ok_detection


# Each tile has (33, 33) pixels on adventure map

# Each tile has (45, 54) pixels on battle map

# Battlefield point (0, 0) has coordinates (660, 330) pixels

# Adventure map ends at (1720, 1032) pixels

# Border around the screen has 6 px

# There are (54, 32) tiles visible on adventure map


def move_mouse_and_click_adventure(x: int, y: int):
    """
    move mouse to the given coordinates and press on it

    :param x: "x" coordinate of the location to be clicked
    :param y: "y" coordinate of the location to be clicked
    """
    mouse.move(x, y, duration=0)
    time.sleep(0.1)
    mouse.click()


def leave_screen():
    """
    leave screen
    """
    time.sleep(0.1)
    kb.send('esc')
    time.sleep(0.1)


def accept_offer():
    """
    accept offer
    """
    kb.send('enter')


def generic_proposal(accept: bool):
    """
    Accept or reject proposal on screen
    """
    if accept:
        accept_offer()
    else:
        leave_screen()


def center_on_hero():
    """
    center camera on hero
    """
    kb.send('enter')


def press_hero(number):
    """
    press hero

    :param number: hero number on the hero list
    """
    move_mouse_and_click_adventure(1760, 210 + 32 * number)


def move_mouse_over_hero(number):
    """
    move mouse over hero

    :param number: hero number on the hero list
    """
    mouse.move(1890, 230 + 32 * number, duration=0)
    time.sleep(0.1)
    mouse.move(1760, 210 + 32 * number, duration=0)
    time.sleep(0.1)


def move_mouse_over_town(number):
    """
    move mouse over town

    :param number: town number on the town list
    """


    mouse.move(1760, 210 + 32 * number, duration=0)
    time.sleep(0.05)
    mouse.move(1890, 230 + 32 * number, duration=0)
    time.sleep(0.05)


def press_town(number):
    """
    press town

    :param number: town number on the town list
    """
    move_mouse_and_click_adventure(1890, 230 + 32 * number)


def press_enter():
    """
    presses enter

    :param number:
    """
    kb.send('enter')


def enter_town(number):
    """
    enter town

    :param number:
    """
    press_town(number)
    kb.send('enter')


def scroll_town_up():
    """
    scroll the town listing upwards
    """
    move_mouse_and_click_adventure(1890, 200)


def scroll_town_down():
    """
    scroll the town listing downwards
    """
    move_mouse_and_click_adventure(1890, 440)


def press_kingdom_overview():
    """
    press kingdom overview
    """
    kb.send('k')


def press_underworld_view():
    """
    press underw
    """
    kb.send('u')


def view_world():
    """
    view world
    """
    kb.send('v')


def press_replay_opponent_turn():
    """
    press replay opponent turn
    """
    move_mouse_and_click_adventure(1845, 240)


def view_puzzle():
    """
    view puzzle
    """
    kb.send('p')


def dig():
    """
    dig
    """
    kb.send('d')


def questlog():
    """
    open questlog
    """
    kb.send('q')


def put_hero_to_sleep():
    """
    put hero to sleep
    """
    kb.send('z')


def wake_hero_up():
    """
    wake hero up
    """
    kb.send('w')


def move_hero():
    """
    Finishes the movement
    """
    kb.send('m')
    time.sleep(1)

def max_unit_buy():
    """
    selects amx amount of units in habitat
    """
    kb.press('m')
    time.sleep(0.1)
    kb.release('m')

def click_cast_spell():
    """
    click cast spell
    """
    kb.send('c')


def view_scenario_info():
    """
    view scenario info
    """
    kb.send('i')


def system_options():
    """
    system options
    """
    kb.send('o')


def next_hero():
    """
    next hero
    """
    kb.send('h')


def end_turn():
    """
    end turn
    """
    kb.send('e')


def click_on_tile_adventure(x: int, y: int):
    """
    Hero is expected to be in the middle of the screen (x=0, y=0)

    :param x: "x" coordinate of the location to be clicked
    :param y: "y" coordinate of the location to be clicked
    """
    center = (848, 534)
    expected_move = (center[0] + x * 32, center[1] + y * 32)
    move_mouse_and_click_adventure(expected_move[0], expected_move[1])


def move_mouse_to_tile_adventure(x: int, y: int):
    """
    Move_mouse_to_tile on adventure
    Hero is expected to be in the middle of the screen (x=0, y=0)

    :param x: "x" coordinate of the location to be clicked
    :param y: "y" coordinate of the location to be clicked
    """
    center = (848, 534)
    expected_move = (center[0] + x * 32, center[1] + y * 32)
    mouse.move(expected_move[0], expected_move[1])


def move_mouse_by_pixel_relative(x: int, y: int):
    """
    Function for moving mouse by some pixel relative to the current mouse position

    :param x: x pixel shift
    :param y: y pixel shift
    """
    mx, my = mouse.get_position()
    mouse.move(mx + x, my + y)


def move_to_tile_adventure(x: int, y: int):
    """
    move_to_tile_adventure

    :param x: "x" coordinate of the location to be clicked
    :param y: "y" coordinate of the location to be clicked
    """
    click_on_tile_adventure(x, y)
    move_hero()


def enter_current_tile():
    """
    enter_current_tile
    """
    kb.send('space')


def save_in_game(savefile_name):
    """
    save game

    :param savefile_name: name of the saved file
    """
    # max lenght of savefile_name
    if len(savefile_name) > 50:
        savefile_name = savefile_name[0:50]
    kb.send('s')
    # deletion of the current name
    for i in range(60):
        time.sleep(0.01)
        kb.press('backspace')
    # naming the file
    for char in savefile_name:
        time.sleep(0.01)
        kb.send(char)
    # press save
    time.sleep(0.1)
    kb.send('enter')
    # check if filename is exists and overwtite it, and click ok
    detected = image_processing.ok_detection.check_ok()
    while detected:
        time.sleep(0.1)
        kb.send('enter')
        detected = image_processing.ok_detection.check_ok()


def access_marketplace():
    """
    access_marketplace
    """
    kb.send('b')


def move_hero_up():
    """
    move hero up
    """
    kb.send('up')


def move_hero_down():
    """
    move hero down
    """
    kb.send('down')


def move_hero_left():
    """
    move hero left
    """
    kb.send('left')


def move_hero_right():
    """
    move hero right
    """
    kb.send('right')


def move_hero_top_right():
    """
    move hero top right
    """
    kb.send('pageup')


def move_hero_top_left():
    """
    move hero top left
    """
    kb.send('home')


def move_hero_bottom_right():
    """
    move hero bottom right
    """
    kb.send('pagedown')


def move_hero_bottom_left():
    """
    move hero bottom left
    """
    kb.send('end')


def move_camera_left():
    """
    move camera left
    """
    kb.send('ctrl+left')


def move_camera_right():
    """
    move camera right
    """
    kb.send('ctrl+right')


def move_camera_up():
    """
    move camera up
    """
    kb.send('ctrl+up')


def move_camera_down():
    """
    move camera down
    """
    kb.send('ctrl+down')


def level_up_choose_skill(number):
    """
    Choose skill
    Left skill is number 1, right one is number 2

    :param number: (int) left -> 1, right -> 2
    """
    if number == 1:
        kb.send('1')
    else:
        kb.send('2')
    time.sleep(0.1)
    kb.send('enter')


def accept_retreat(accept: bool):
    """
    Accept retreat

    :param accept: (Boolean) Yes -> True, No -> False
    """
    if accept:
        move_mouse_and_click_adventure(1000, 600)
    else:
        move_mouse_and_click_adventure(910, 600)


def accept_battle_result(accept: bool):
    """
    accept battle result

    :param accept: (Boolean) Yes -> True, No -> False
    """
    if accept:
        move_mouse_and_click_adventure(1140, 780)
    else:
        move_mouse_and_click_adventure(780, 780)


def choose_chest(choice: str):
    """
    choose chest

    :param choice: (str) "gold", "exp" or "experience" is the correct value
    """
    choice = choice.lower()
    if choice in {'gold', 'exp', 'experience'}:
        if choice == 'gold':
            move_mouse_and_click_adventure(890, 590)
        else:
            move_mouse_and_click_adventure(1020, 590)
        move_mouse_and_click_adventure(960, 690)
    else:
        print("No correct value given, accepted values are: gold, exp or experience")


def recruit_unit(amount: int):
    """
    Recruits a specified amount of units from a habitat if there is free space.
    To recruit all units the amount should be: -1
    This function expects you to have all necessary resources

    :param amount: amount of units to be recruited
    """

    if amount == -1:
        move_mouse_and_click_adventure(870, 585)
    else:
        while amount > 1:
            move_mouse_and_click_adventure(1005, 543)
            time.sleep(0.1)
            amount -= amount
    move_mouse_and_click_adventure(945, 585)


def artifact_coordinates(slot_id, artifacts, additional_id):
    """
    Inside function shouldn't be touched

    :param slot_id:
    :param artifacts:
    :param additional_id:
    :return:
    """
    if slot_id == artifacts[1] or slot_id == 1:
        return 1090, 290
    elif slot_id == artifacts[2] or slot_id == 2:
        return 1145, 500
    elif slot_id == artifacts[3] or slot_id == 3:
        return 1090, 340
    elif slot_id == artifacts[4] or slot_id == 4:
        return 960, 330
    elif slot_id == artifacts[5] or slot_id == 5:
        return 1140, 445
    elif slot_id == artifacts[6] or slot_id == 6:
        return 1090, 390
    elif slot_id == artifacts[7] or slot_id == 7:
        if additional_id == 0:
            return 1010, 330
        else:
            return 1200, 440
    elif slot_id == artifacts[8] or slot_id == 8:
        return 1095, 555
    elif slot_id == artifacts[9] or slot_id == 9:
        if additional_id == 4:
            return 960, 555
        else:
            return 965 + 15*additional_id, 400 + 50*additional_id
    elif slot_id == artifacts[10] or slot_id == 10:
        return 1145, 290
    elif slot_id == artifacts[11] or slot_id == 11:
        return 1190, 290
    elif slot_id == artifacts[12] or slot_id == 12:
        return 1190, 335
    elif slot_id == artifacts[13] or slot_id == 13:
        return 1190, 380
    elif slot_id == artifacts[14] or slot_id == 14:
        return 1190, 570
    elif slot_id == artifacts[15] or slot_id == 15:
        return 910 + 45*(additional_id % 8), 328 + 47*int(additional_id / 8)


def click_artifact(slot_id, artifacts, additional_id):
    """
    click on a given artifact inside function

    :param slot_id:
    :param artifacts:
    :param additional_id:
    """
    coords = artifact_coordinates(slot_id, artifacts, additional_id)
    move_mouse_and_click_adventure(coords[0], coords[1])


def change_artifact(slot_id_from, slot_id_to, additional_id=0):
    """
    Artifacts are labeled according to https://heroes.thelazy.net/index.php/Artifact
    you can either pass in the slot number or the slot name
    additional_id is the number given to miscellaneous or ring artifacts and ones in the backpack

    :param slot_id_from: can be either slot number according to the dict or the slot name as str
    :param slot_id_to: can be either slot number according to the dict or the slot name as str
    :param additional_id: needed when inputting ring, misc or backpack, id of the additional slot
    """
    artifacts = {1: 'helmet', 2: 'cape', 3: 'necklace', 4: 'right hand', 5: 'left hand', 6: 'torso',
                 7: 'ring', 8: 'feet', 9: 'miscellaneous', 10: 'ballista', 11: 'ammo cart',
                 12: 'first aid tent', 13: 'catapult', 14: 'spell book', 15: 'backpack'}

    if slot_id_from == 15 or slot_id_from == artifacts[15]:
        move_mouse_and_click_adventure(1080, 695)
    click_artifact(slot_id_from, artifacts, additional_id)
    if slot_id_to == 15 or slot_id_to == artifacts[15]:
        move_mouse_and_click_adventure(1080, 695)
    click_artifact(slot_id_to, artifacts, additional_id)


def click_unit_tile(nr):
    """
    Inside hero's inventory

    :param nr: number of a unit
    """
    move_mouse_and_click_adventure(667 + 65*nr, 763)


def change_units(nr1, nr2):
    """Inside hero's inventory

    :param nr1: unit no 1
    :param nr2: unit no 2
    """
    click_unit_tile(nr1)
    click_unit_tile(nr2)


def set_combat_formation(formation: str):
    """
    set combat formation

    :param formation: loose or tight
    :return: does nothing
    """
    if formation not in {'loose', 'tight'}:
        print('Wrong formation name')
        return
    if formation == 'loose':
        move_mouse_and_click_adventure(1140, 745)
    else:
        move_mouse_and_click_adventure(1140, 782)


def dismiss_hero():
    """
    Dismiss hero First enter his inventory
    """
    move_mouse_and_click_adventure(1190, 700)


def upgrade_unit_hill_fort(tile_number):
    """
    Upgrade unit in a hill fort
    Specify a number or write a string 'all'

    :param tile_number: tile number
    """
    if tile_number == 'all':
        move_mouse_and_click_adventure(690, 610)
    move_mouse_and_click_adventure(770 + 75*tile_number, 550)


def town_gate_adventure(town_id):
    """
    use town gate on the adventure map

    :param town_id: id of town we want to move to
    """
    move_mouse_and_click_adventure(880, 436 + 32 * town_id)
    time.sleep(0.1)
    kb.send('enter')


def change_unit_make_room_when_join(inner_tile, outer_tile):
    """
    change units when a unit joins you and you have full unit

    :param inner_tile: number of inner tile
    :param outer_tile: number of outer tile
    """
    move_mouse_and_click_adventure(805 + 60*outer_tile, 500)
    move_mouse_and_click_adventure(805 + 60 * inner_tile, 600)


def choose_skill_upgrade(side):
    """
    Old function no touchy

    :param side: left or right side
    :return: does nothing
    """
    if side not in {'left', 'right'}:
        print('Side can be: left or right')
        return
    if side == 'left':
        move_mouse_and_click_adventure(900, 600)
    else:
        move_mouse_and_click_adventure(1000, 600)
    time.sleep(0.1)
    kb.send('enter')


def seafaring_academy(ability_id):
    """
    Choose seafaring academy skill

    :param ability_id: Ability id
    """
    move_mouse_and_click_adventure(850 + 100*ability_id, 600)
    kb.send('enter')
    kb.send('enter')


def cast_spell_adventure(id):
    """
    cast spell on the adventure map

    :param id: Spell id
    """
    click_cast_spell()
    move_mouse_and_click_adventure(705 + 90*(id % 3), 330 + 90*int(id / 3))
