"""Script containing functions essential for handling battle GUI."""
import time
import keyboard as kb
import mouse
import ctypes

# Each tile has (45, 54) pixels on battle map

# Battlefield point (0, 0) has coordinates (660, 330) pixels

# There's (15, 11) tiles on the battle map


def move_mouse_and_click_battle(x: int, y: int):
    """
    move mouse and click during battle

    :param x: x coord
    :param y: y coord
    """
    mouse.move(x, y, duration=0)
    time.sleep(0.1)
    mouse.click()


def surrender():
    """
    surrender
    """
    kb.send('s')


def quick_combat():
    """
    quick combat
    """
    kb.send('q')


def wait():
    """
    wait
    """
    kb.send('w')


def retreat():
    """
    retreat
    """
    kb.send('r')


def show_current_unit_stats():
    """
    show unit stats
    """
    kb.send('t')


def show_heroes_stats():
    """
    show hero stats
    """
    kb.send('i')


def options():
    """
    click options
    """
    kb.send('o')


def auto_combat():
    """
    auto combat
    """
    kb.send('a')


def defend():
    """
    defend
    """
    kb.send('d')


def fight_log():
    """
    fight log
    """
    kb.send('h')


def show_hide_queue():
    """
    show or hide queue
    """
    kb.send('z')


def spell_book():
    """
    go into spell book
    """
    kb.send('c')


def move_mouse_to_tile(x: int, y: int, win_gui=False):
    """
    move mouse to tile

    :param x: x coord
    :param y: y coord
    :param win_gui: use win32gui
    """
    if y % 2 == 1:
        beginning = (640, 330)
    else:
        beginning = (660, 330)
    expected_move = (beginning[0] + x*44, beginning[1] + y*42)

    if win_gui:
        ctypes.windll.user32.SetCursorPos(int(expected_move[0]), int(expected_move[1]))
    else:
        mouse.move(expected_move[0], expected_move[1], duration=0)


def move_to_tile(x: int, y: int):
    """
    Top left corner is the (0, 0) point.
    Adding x moves the chosen tile to the right, adding y moves it downwards

    :param x: x coord
    :param y: y coord
    """
    if y % 2 == 1:
        beginning = (640, 330)
    else:
        beginning = (660, 330)
    expected_move = (beginning[0] + x*44, beginning[1] + y*42)

    move_mouse_and_click_battle(expected_move[0], expected_move[1])
    print('done')


def attack_enemy(x: int, y: int, direction: str):
    """
    Attacks the enemy on the given coordinates from a given direction. Possible directions are:
    'top', 'top_right', 'right', 'bottom_right', 'bottom', 'bottom_left', 'left', 'top_left'
    Works the same way as move_to_tile with additional direction

    :param x: x coord
    :param y: y coord
    :param direction: direction we want to attack from
    """
    direction = direction.lower()
    if y % 2 == 1:
        beginning = (640, 330)
    else:
        beginning = (660, 330)
    expected_move = (beginning[0] + x*44, beginning[1] + y*42)
    if direction in {'top', 'top_right', 'right', 'bottom_right', 'bottom', 'bottom_left', 'left', 'top_left'}:
        if direction == 'top':
            expected_move = (beginning[0] + x * 44, beginning[1] + y * 42 - 10)
        elif direction == 'top_right':
            expected_move = (beginning[0] + x * 44 + 10, beginning[1] + y * 42 - 10)
        elif direction == 'right':
            expected_move = (beginning[0] + x * 44 + 10, beginning[1] + y * 42)
        elif direction == 'bottom_right':
            expected_move = (beginning[0] + x * 44 + 10, beginning[1] + y * 42 + 10)
        elif direction == 'bottom':
            expected_move = (beginning[0] + x * 44, beginning[1] + y * 42 + 10)
        elif direction == 'bottom_left':
            expected_move = (beginning[0] + x * 44 - 10, beginning[1] + y * 42 + 10)
        elif direction == 'left':
            expected_move = (beginning[0] + x * 44 - 10, beginning[1] + y * 42)
        elif direction == 'top_left':
            expected_move = (beginning[0] + x * 44 - 10, beginning[1] + y * 42 - 10)
        move_mouse_and_click_battle(expected_move[0], expected_move[1])


def area_attack(x: int, y: int):
    """
    Attack area. For Magogs and Liches

    :param x: x coord
    :param y: y coord
    """
    kb.press('G')
    move_to_tile(x, y)
    time.sleep(0.1)
    kb.release('G')


def default_spell_book_position():
    """
    Returns to the leftmost page of the spellbook
    """
    move_mouse_and_click_battle(660, 292)
    time.sleep(0.1)
    mouse.click()


def cast_spell_battle(id):
    """
    Choose a spell. Its id is its position in the book, starting from 0, and not within the overall magic
    (If you have 3 spells of tier 1, 2 and 3 then tier 3 spell has id=2,
    because it lies on the 3rd position in the book)
    The spell is not played on the battlefield, its only chosen.

    :param id: (int) spell id
    """
    time.sleep(0.5)
    move_mouse_and_click_battle(655, 292)
    time.sleep(0.5)
    move_mouse_and_click_battle(655, 292)
    if id >= 48:
        move_mouse_and_click_battle(1260, 292)
        time.sleep(0.5)
        move_mouse_and_click_battle(1260, 292)
        time.sleep(0.5)
    elif id >= 24:
        move_mouse_and_click_battle(1260, 292)
        time.sleep(0.5)
    idx = id % 24
    if 0 <= idx <= 11:
        move_mouse_and_click_battle(705 + 90*(idx % 3), 330 + 90*int(idx / 3))
    else:
        move_mouse_and_click_battle(1015 + 90 * (idx % 3), 330 + 90 * int((idx-12) / 3))


def move_to_portrait(number):
    """
    move mouse to portrait in a queue

    :param number: hero number
    """
    mouse.move(678 + number*40, 800, duration=0)



