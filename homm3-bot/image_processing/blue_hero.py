from GUI_handling.AdventureGUI import center_on_hero, move_to_tile_adventure, next_hero, move_camera_right, \
    move_camera_left, move_camera_up, move_camera_down, move_mouse_to_tile_adventure
from data.hero import hero_dict, Hero, Slot, Slots
from time import sleep
from mss import mss
import numpy as np
import cv2
import image_processing.ocr as ocr
from difflib import get_close_matches
from data.player_data import Player
from data.classes_const import *
import random
import mouse

# Little bit of global variables never hurt nobody
castles_dict = {'Castle': ('Knight', 'Cleric'), 'Rampart': ('Ranger', 'Druid'), 'Tower': ('Alchemist', 'Wizard'),
                    'Inferno': ('Demoniac', 'Heretic'), 'Necropolis': ('Death Knight', 'Necromancer'),
                    'Dungeon': ('Overlord', 'Warlock'), 'Stronghold': ('Barbarian', 'Battle Mage'),
                    'Fortress': ('Beastmaster', 'Witch'), 'Conflux': ('Planeswalker', 'Elementalist'),
                    'Cove':('Captain', 'Navigator')}

enemies_dict = {'Castle': (Pikeman, Halberdier, Archer, Marksman, Griffin, Royal_Griffin, Swordsman, Crusader,
                           Monk, Zealot, Cavalier, Champion, Angel, Archangel),
                'Rampart': (Centaur, Centaur_Captain, Dwarf, Battle_Dwarf, Wood_Elf, Grand_Elf,
                            Pegasus, Silver_Pegasus, Dendroid_Guard, Dendroid_Soldier,
                            Unicorn, War_Unicorn, Green_Dragon, Gold_Dragon),
                'Tower': (Gremlin, Master_Gremlin, Stone_Gargoyle, Obsidian_Gargoyle, Stone_Golem, Iron_Golem,
                          Mage, Arch_Mage, Genie, Master_Genie, Naga, Naga_Queen, Giant, Titan),
                'Inferno': (Imp, Familiar, Gog, Magog, Hell_Hound, Cerberus, Demon, Horned_Demon,
                            Pit_Fiend, Pit_Lord, Efreeti, Efreet_Sultan, Devil, Arch_Devil),
                'Necropolis': (Skeleton, Skeleton_Warrior, Walking_Dead, Zombie, Wight, Wraith,
                               Vampire, Vampire_Lord, Lich, Power_Lich, Black_Knight, Dread_Knight,
                               Bone_Dragon, Ghost_Dragon),
                'Dungeon': (Troglodyte, Infernal_Troglodyte, Harpy, Harpy_Hag, Beholder, Evil_Eye, Medusa,
                            Medusa_Queen, Minotaur, Minotaur_King, Manticore, Scorpicore, Red_Dragon, Black_Dragon),
                'Stronghold': (Goblin, Hobgoblin, Wolf_Rider, Wolf_Raider, Orc, Orc_Chieftain, Ogre, Ogre_Mage,
                               Roc, Thunderbird, Cyclops, Cyclops_King, Behemoth, Ancient_Behemoth),
                'Fortress': (Gnoll, Gnoll_Marauder, Lizardman, Lizard_Warrior, Serpent_Fly, Dragon_Fly,
                             Basilisk, Greater_Basilisk, Gorgon, Mighty_Gorgon, Wyvern, Wyvern_Monarch,
                             Hydra, Chaos_Hydra),
                'Conflux': (Pixie, Sprite, Air_Elemental, Storm_Elemental, Water_Elemental, Ice_Elemental,
                            Fire_Elemental, Energy_Elemental, Earth_Elemental, Magma_Elemental,
                            Psychic_Elemental, Magic_Elemental, Firebird, Phoenix),
                # Sea dog is gone (insert crab rave meme)
                'Cove': (Nymph, Oceanid, Crew_Mate, Seaman, Pirate, Corsair, Stormbird, Ayssid, Sea_Witch,
                         Sorceress, Nix, Nix_Warrior, Sea_Serpent, Haspid),
                # Added for completion’s sake
                'Neutral': (Peasant, Halfling, Rogue, Boar, Leprechaun, Nomad, Mummy, Sharpshooter, Satyr,
                            Steel_Golem, Troll, Gold_Golem, Fangarm, Diamond_Golem, Enchanter, Faerie_Dragon,
                            Rust_Dragon, Crystal_Dragon, Azure_Dragon)}


def moveCameraToTarget(target: tuple, player):
    """
    Move camera to target

    :param target: Target coordinates
    :param player: Our player
    """
    sleep(0.2)
    tx, ty = target
    cx, cy = player.camera
    print("[BLUE CAMERA MOVE]")
    print(f"    FROM: {cx, cy}")
    print(f"    DESTINATION: {tx, ty}")
    while abs(cx - tx) >= 3 or abs(cy - ty) >= 3:
        if cx - tx >= 3:
            move_camera_left()
            cx -= 3
        elif cx - tx <= -3:
            move_camera_right()
            cx += 3
        elif cy - ty >= 3:
            move_camera_up()
            cy -= 3
        elif cy - ty <= -3:
            move_camera_down()
            cy += 3
        sleep(0.05)
    player.camera = (cx, cy)


def ocr_name(screen):
    """
    Function that helps read the name of the hero

    :param screen:
    :return: Found name
    """
    scale = 3
    width = screen.shape[1]
    height = screen.shape[0]
    screen = cv2.resize(screen, (width * scale, height * scale))
    b, g, r = cv2.split(screen)
    search = np.where((b > 85) &
                      (g > 160) &
                      (r > 170))

    mask = np.full((height * scale, width * scale, 3), 0, dtype=np.uint8)
    mask[search] = [255, 255, 255]
    screen = 255 - mask
    text = ocr.read_text(screen, 6, False, True)
    text = text.replace('\n', ' ')
    text = text.strip()
    for char in "',.`;:\"-_‘":
        text = text.replace(char, '')

    return text


def check_if_blue_hero_exists(player, enemy_coordinates: tuple):
    """
    Check all found blue heroes and find whether they exist or not 

    :param player: Current player
    :param enemy_coordinates: Checked enemy coordinates
    :return: tuple (True/False, Hero_name) (Hero exists, his name is None when no hero found)
    """

    moveCameraToTarget(enemy_coordinates, player)
    sleep(0.4)
    camX, camY = player.camera
    x, y = enemy_coordinates
    move_mouse_to_tile_adventure(x - camX, y - camY)
    sleep(0.2)
    with mss() as sct:
        monitor = {'top': 1035, 'left': 680, 'width': 320, 'height': 18}
        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)

    text = ocr_name(screen)

    if text == '':
        return False, None
    try:
        text = text.split()
        text = get_close_matches(text[0], hero_dict, 1)[0]
    except Exception:
        text = None

    if text is not None:
        return True, text
    else:
        return False, text


def get_creature_numbers(shiftX, shiftY):
    """
    Get numbers of enemy units

    :return: List of numbers of enemy units
    """
    with mss() as sct:
        amount_list = []
        screens = []
        for i in range(7):
            if i < 3:
                monitor = {'top': 536 + 32 * shiftY, 'left': 779 + i*36 + 32 * shiftX, 'width': 34, 'height': 12}
            else:
                monitor = {'top': 584 + 32 * shiftY, 'left': 761 + (i-3)*36 + 32 * shiftX, 'width': 34, 'height': 12}
            screen = np.array(sct.grab(monitor))
            screens.append(screen)

        for screen in screens:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
            text = ocr.read_text_faster(screen, 4)
            text = text.replace('\n', ' ')
            text = text.strip()
            if not text:
                amount_list.append('-')
            else:
                # The text more than often comes out as for example 1014 instead of 10-19
                # the fist number is usually right, so I do it like that
                try:
                    number = int(text)
                    if number == 99:  # Came up from testing
                        text = '50-99'
                    elif number == 649:
                        text = '5-9'
                    elif number == 9:
                        text = '5-9'
                    elif number < 20:
                        text = '1-4'
                    elif number < 100:
                        text = '5-9'
                    elif number < 1500:
                        text = '10-19'
                    elif number < 5000:
                        text = '20-49'
                    elif number < 10000:
                        text = '50-99'
                    elif number < 150000:
                        text = '100-249'
                    elif number < 300000:
                        text = '250-499'
                    elif number < 600000:
                        text = '500-999'
                    elif number < 1000000:
                        text = '1000-'
                    else:
                        text = '5-9'
                except ValueError:
                    pass
                amount_list.append(text)
        return amount_list


def fill_enemy_hero(player: Player, enemy_coordinates: tuple):
    """
    Fills enemy hero should be used only as it also checks if it exists first

    :param player: Our hero
    :param enemy_coordinates: Enemy coordinates
    :return: Nothing
    """
    exists, hero_name = check_if_blue_hero_exists(player, enemy_coordinates)
    if not exists:
        return None

    hero = Hero(1, 'enemy', hero_name, 1, 1, 1, 1)
    hero.position = enemy_coordinates
    mouse.press(button='right')
    x, y = enemy_coordinates
    camX, camY = player.camera
    hero_units = get_creature_numbers(x - camX, y - camY)
    mouse.release(button='right')

    curr_week = player.week
    curr_month = player.month

    slots = Slots()
    for i, unit in enumerate(hero_units):
        if curr_week < 3:
            if unit == '-':
                slots.slots[i] = Slot()
            elif unit == '1-4':
                number = random.randint(1, 4)
                slots.slots[i] = Slot(Monk, number)
            elif unit == '5-9':
                number = random.randint(5, 9)
                slots.slots[i] = Slot(Crusader, number)
            elif unit == '10-19':
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Griffin, number)
            elif unit == '20-49':
                number = random.randint(20, 49)
                slots.slots[i] = Slot(Archer, number)
            elif unit == '50-99':
                number = random.randint(50, 99)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '100-249':
                number = random.randint(100, 249)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '250-499':
                number = random.randint(250, 499)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '500-999':
                number = random.randint(500, 999)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '1000-':
                number = random.randint(1000, 3000)
                slots.slots[i] = Slot(Pikeman, number)
            else:  # Just to be safe in case text didn't work any random amount
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Griffin, number)

        elif curr_week < 4:
            if unit == '-':
                slots.slots[i] = Slot()
            elif unit == '1-4':
                number = random.randint(1, 4)
                slots.slots[i] = Slot(Cavalier, number)
            elif unit == '5-9':
                number = random.randint(5, 9)
                slots.slots[i] = Slot(Crusader, number)
            elif unit == '10-19':
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Crusader, number)
            elif unit == '20-49':
                number = random.randint(20, 49)
                slots.slots[i] = Slot(Archer, number)
            elif unit == '50-99':
                number = random.randint(50, 99)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '100-249':
                number = random.randint(100, 249)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '250-499':
                number = random.randint(250, 499)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '500-999':
                number = random.randint(500, 999)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '1000-':
                number = random.randint(1000, 3000)
                slots.slots[i] = Slot(Pikeman, number)
            else:  # Just to be safe in case text didn't work any random amount
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Griffin, number)

        elif curr_week < 6:
            if unit == '-':
                slots.slots[i] = Slot()
            elif unit == '1-4':
                number = random.randint(1, 4)
                slots.slots[i] = Slot(Archangel, number)
            elif unit == '5-9':
                number = random.randint(5, 9)
                slots.slots[i] = Slot(Champion, number)
            elif unit == '10-19':
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Monk, number)
            elif unit == '20-49':
                number = random.randint(20, 49)
                slots.slots[i] = Slot(Crusader, number)
            elif unit == '50-99':
                number = random.randint(50, 99)
                slots.slots[i] = Slot(Archer, number)
            elif unit == '100-249':
                number = random.randint(100, 249)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '250-499':
                number = random.randint(250, 499)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '500-999':
                number = random.randint(500, 999)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '1000-':
                number = random.randint(1000, 3000)
                slots.slots[i] = Slot(Pikeman, number)
            else:  # Just to be safe in case text didn't work any random amount
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Griffin, number)

        else:
            if unit == '-':
                slots.slots[i] = Slot()
            elif unit == '1-4':
                number = random.randint(1, 4)
                slots.slots[i] = Slot(Archangel, number)
            elif unit == '5-9':
                number = random.randint(5, 9)
                slots.slots[i] = Slot(Archangel, number)
            elif unit == '10-19':
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Cavalier, number)
            elif unit == '20-49':
                number = random.randint(20, 49)
                slots.slots[i] = Slot(Swordsman, number)
            elif unit == '50-99':
                number = random.randint(50, 99)
                slots.slots[i] = Slot(Griffin, number)
            elif unit == '100-249':
                number = random.randint(100, 249)
                slots.slots[i] = Slot(Archer, number)
            elif unit == '250-499':
                number = random.randint(250, 499)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '500-999':
                number = random.randint(500, 999)
                slots.slots[i] = Slot(Pikeman, number)
            elif unit == '1000-':
                number = random.randint(1000, 3000)
                slots.slots[i] = Slot(Pikeman, number)
            else:  # Just to be safe in case text didn't work any random amount
                number = random.randint(10, 19)
                slots.slots[i] = Slot(Griffin, number)

    hero.slots = slots
    if hero not in player.enemies:
        player.enemies.append(hero)

    print("[DETECTED ENEMY HERO]")
    for unit in hero.slots.slots:
        print(f"     UNIT: {unit.unit.name}, {unit.amount}")




