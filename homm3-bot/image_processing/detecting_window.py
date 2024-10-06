"""Script containing classes and functions responsible for detecting and handling window pop ups."""
import numpy as np
import cv2 as cv
import pyautogui
import time
import keyboard
import pytesseract
import battleAI.BattleAI
import image_processing.ocr as ocr
from mss import mss

from image_processing.ok_detection import check_ok
from difflib import get_close_matches
from GUI_handling.AdventureGUI import level_up_choose_skill, accept_offer
from data.hero_specialities import specialities

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
battle_ai_object = battleAI.BattleAI.BattleAI("Red") # change here if playing as another color


class SecondarySkill:
    def __init__(self, lvl: int = 0, name: str = '', value: int = 0):
        """
        Class representing a secondary skill.

        :param lvl: Level of the skill
        :param name: Name of the skill
        :param value: Value of the skill
        """
        self.lvl = lvl
        self.name = name
        self.value = value

    def __eq__(self, other):
        if isinstance(other,str):
            return self.name==other
        return self.name==other.name

    def __hash__(self):
        return hash((self.lvl,self.name,self.value))


def compare(result, result_image, image):
    """
    Single function to detect if the best match image is exact same as we need

    :param result: image of the best match
    :param result_image: stock image (e.g. battle_result.png)
    :param image: screenshot
    :return: returning 1 if its exact the same
    """
    is_on_image = 0
    mn, _, mnLoc, _ = cv.minMaxLoc(result)
    MPx, MPy = mnLoc
    trows, tcols = result_image.shape[:2]
    ok_compare = image[MPy:MPy + trows, MPx:MPx + tcols]

    # comparing to the normal icon image
    compare1 = cv.compare(result_image, ok_compare, 0)
    if compare1.all():
        is_on_image = 1
    return is_on_image


def which_window():
    """
    Making screenshot, matching windows with the best match using cv2,
    comparing it with actual image to decide which window popped on screen

    :return:  1 -> followers, 2 -> battle, 3 -> pursue, 4-> diplomacy window, 5 -> insulted units
    """
    which = 0
    battle_result_image = cv.imread(r'.\image_processing\battle_result.png')
    diplomacy_image = cv.imread(r'.\image_processing\diplomacy.png')
    insulting_image = cv.imread(r'.\image_processing\insulted.png')
    
    timeout = time.time() + 5
    
    while not which:
        if time.time() > timeout:
            break    
        image_scr = pyautogui.screenshot()
        image_scr = cv.cvtColor(np.array(image_scr), cv.COLOR_RGB2BGR)
        method = cv.TM_SQDIFF_NORMED
        result_battle = cv.matchTemplate(battle_result_image, image_scr, method)
        is_battle = compare(result_battle, battle_result_image, image_scr)
        result_diplomacy = cv.matchTemplate(diplomacy_image, image_scr, method)
        is_diplomacy = compare(result_diplomacy, diplomacy_image, image_scr)
        result_insulting = cv.matchTemplate(insulting_image, image_scr, method)
        is_insulting = compare(result_insulting, insulting_image, image_scr)
        if is_battle == 1:
            which = 2
            # print('battle window')
        elif is_diplomacy == 1:
            which = 4
        elif is_insulting == 1:
            which = 5
        else:
            b = pursue_check(image_scr)
            c = follow_check(image_scr)
            if b == 1:
                which = 3
                # print('pursue window')
            elif c == 1:
                which = 1
                # print('followers window')
    return which


def read_gray_image(path):
    """ Utility function for reading image and converting it to gray scale

    :param path: path to an image

    :return: gray scale image
    """
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    return image


def check_fortification():
    """
    Checks what type of fortification does the opponent have

    :return: Either "fort", "citadel" or "castle" string
    """
    x, y = 954, 365     # TODO: set coordinates to a location of enemy's town
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown(button='right')

    with mss() as sct:
        monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        screen = np.array(sct.grab(monitor))
        screen = cv.cvtColor(screen, cv.COLOR_BGRA2GRAY)

    pyautogui.mouseUp(button='right')
    building_dict = {"fort": read_gray_image(r"..\fortifications\fort.png"),
                     "castle": read_gray_image(r"..\fortifications\castle.png"),
                     "citadel": read_gray_image(r"..\fortifications\citadel.png")}

    values = {}
    for name, building in zip(building_dict.keys(), building_dict.values()):
        res = cv.matchTemplate(screen, building, cv.TM_CCOEFF)
        values[name] = np.max(res)

    return f'{max(values, key=values.get)}'


def action_window(which, hero):
    """
    Deciding which key to press depending on the window we detected

    :param which: 1 -> followers, 2 -> battle, 3 -> pursue, 4-> diplomacy window, 5 -> insulted units
    """
    Tactics = SecondarySkill(0, "Tactics", 3)
    Necromancy = SecondarySkill(0, "Necromancy", 5)
    print("[WINDOW INFO]")
    print(f"    WHICH: {which}")
    walkaa =False # true jest walka False nie ma walki
    if which == 1:
        keyboard.press_and_release('esc')
        time.sleep(3)
        d = which_window()
        action_window(d, hero)




    elif which == 2:
        if walkaa:
            keyboard.press_and_release('esc')
            time.sleep(6)
            print("bitwa")
            if Tactics in hero.skills.secondary_skills:
                print("taktyka")
                accept_offer()
                time.sleep(3)
                accept_offer()
            time.sleep(1)

            hero_name = get_close_matches(hero.name, specialities.keys())[0]
            # making a dict of hero skills
            skill_dict = {}
            for skill in hero.skills.secondary_skills:
                skill_dict.update({skill.name: skill.lvl})
            battle_ai_object.fight(hero_name, skill_dict, hero.spellpower)

            time.sleep(1)
            skills_window(hero)
            time.sleep(0.5)
            if Necromancy in hero.skills.secondary_skills:
                print("nekro")
                accept_offer()
        else:
            keyboard.press_and_release('enter')
            time.sleep(6)
            print("bitwa skip")
            time.sleep(1)
            skills_window(hero)
            time.sleep(0.5)
            if Necromancy in hero.skills.secondary_skills:
                print("nekro")
                accept_offer()

    elif which == 3:
        keyboard.press_and_release('esc')
        time.sleep(3)
        c = which_window()
        action_window(c, hero)

    elif which == 4:
        keyboard.press_and_release('esc')
        time.sleep(3)
        c = which_window()
        action_window(c, hero)

    elif which == 5:
        keyboard.press_and_release('enter')
        time.sleep(3)
        c = which_window()
        action_window(c, hero)


def action_window_enemy_turn(which, hero):
    """
    Deciding which key to press depending on the window we detected

    :param which: 1 -> followers, 2 -> battle, 3 -> pursue, 4-> diplomacy window, 5 -> insulted units
    """
    Tactics = SecondarySkill(0, "Tactics", 3)
    Necromancy = SecondarySkill(0, "Necromancy", 5)
    print("[WINDOW INFO]")
    print(f"    WHICH: {which}")
    if which == 1:
        keyboard.press_and_release('esc')
        time.sleep(3)
        d = which_window()
        action_window(d, hero)

    elif which == 2:
        keyboard.press_and_release('enter')
        time.sleep(6)
        print("bitwa")
        # if Tactics in hero.skills.secondary_skills:
        #     print("taktyka")
        #     accept_offer()
        #     time.sleep(3)
        #     accept_offer()
        # time.sleep(1)
        #
        # hero_name = get_close_matches(hero.name, specialities.keys())[0]
        # # making a dict of hero skills
        # skill_dict = {}
        # for skill in hero.skills.secondary_skills:
        #     skill_dict.update({skill.name: skill.lvl})
        # battle_ai_object.fight(hero_name, skill_dict, hero.spellpower)
        time.sleep(1)
        skills_window(hero)
        time.sleep(0.5)
        if Necromancy in hero.skills.secondary_skills:
            print("nekro")
            accept_offer()

    elif which == 3:
        keyboard.press_and_release('esc')
        time.sleep(3)
        c = which_window()
        action_window(c, hero)

    elif which == 4:
        keyboard.press_and_release('esc')
        time.sleep(3)
        c = which_window()
        action_window(c, hero)

    elif which == 5:
        keyboard.press_and_release('enter')
        time.sleep(3)
        c = which_window()
        action_window(c, hero)


def pursue_check(img_source):
    """
    Using tesseract to detect if there is word 'pursue' in the window

    :param img_source: screenshot
    :return: 1 if detects word 'pursue', 0 if it is not detected
    """
    img_source = pyautogui.screenshot()
    img_source = cv.cvtColor(np.array(img_source), cv.COLOR_RGB2BGR)
    img_source = img_source[400:600, 800:1200]
    # custom_config = r'--oem 3 --psm 4'
    # string_window = (pytesseract.image_to_string(img_source, config=custom_config))
    string_window = ocr.read_generic_text(img_source)

    if 'pursue' in string_window:
        return 1
    else:
        return 0


def follow_check(img_source):
    """
    Using tesseract to detect if there is word 'follow' in the window

    :param img_source: screenshot
    :return: 1 if detects word 'pursue', 0 if it is not detected
    """
    img_source = pyautogui.screenshot()
    img_source = cv.cvtColor(np.array(img_source), cv.COLOR_RGB2BGR)
    img_source = img_source[400:600, 800:1200]
    custom_config = r'--oem 3 --psm 6'
    string_window = (pytesseract.image_to_string(img_source, config=custom_config))
    if 'Followers' in string_window:
        return 1
    else:
        return 0


def execute_detecting(Hero):
    """
    Executing whole program
    """
    time.sleep(2)
    a = which_window()
    action_window(a, Hero)


def execute_detecting_enemy_turn(Hero):
    """
    Executing whole program
    """
    time.sleep(2)
    a = which_window()
    action_window_enemy_turn(a, Hero)


def skills_window(h):
    """
    Very crude, yet working solution for our skills picking needs for our heroes.
    First, it checks for an 'okey' sign on our screen. After detection, if there
    indeed is an 'okey' here - we check certain positions and use optical character recognition
    on them to get our skills' names. Then we pick the best skill according to our calculations
    and click it on our screen in game. Parameter h is our hero and it gets updated with picked
    skill.

    :param h: our Hero that gets updated with new skill
    """
    Air_Magic = SecondarySkill(0, "Air_Magic", 5)
    Archery = SecondarySkill(0, "Archery", 4)
    Armorer = SecondarySkill(0, "Armorer", 5)
    Artillery = SecondarySkill(0, "Artillery", 1)
    Ballistics = SecondarySkill(0, "Ballistics", 1)
    Diplomacy = SecondarySkill(0, "Diplomacy", 4)
    Eagle_Eye = SecondarySkill(0, "Eagle_Eye", 0)
    Earth_Magic = SecondarySkill(0, "Earth_Magic", 5)
    Estates = SecondarySkill(0, "Estates", 5)
    Fire_Magic = SecondarySkill(0, "Fire_Magic", 4)
    First_Aid = SecondarySkill(0, "First_Aid", 0)
    Intelligence = SecondarySkill(0, "Intelligence", 3)
    Leadership = SecondarySkill(0, "Leadership", 3)
    Learning = SecondarySkill(0, "Learning", 0)
    Logistics = SecondarySkill(0, "Logistics", 5)
    Luck = SecondarySkill(0, "Luck", 2)
    Mysticism = SecondarySkill(0, "Mysticism", 2)
    Navigation = SecondarySkill(0, "Navigation", 3)
    Necromancy = SecondarySkill(0, "Necromancy", 5)
    Offense = SecondarySkill(0, "Offense", 5)
    Pathfinding = SecondarySkill(0, "Pathfinding", 3)
    Resistance = SecondarySkill(0, "Resistance", 3)
    Scholar = SecondarySkill(0, "Scholar", 3)
    Scouting = SecondarySkill(0, "Scouting", 4)
    Sorcery = SecondarySkill(0, "Sorcery", 2)
    Tactics = SecondarySkill(0, "Tactics", 3)
    Water_Magic = SecondarySkill(0, "Water_Magic", 4)
    Wisdom = SecondarySkill(0, "Wisdom", 4)
    Interference = SecondarySkill(0, "Interference", 3)
    main_hero_skills = [Logistics, Earth_Magic, Air_Magic, Armorer, Necromancy, Offense, Archery,
                        Water_Magic, Diplomacy, Estates, Fire_Magic, Scouting, Wisdom, Intelligence, Leadership,
                        Navigation,
                        Pathfinding, Resistance, Scholar, Tactics, Interference, Luck, Mysticism, Sorcery, Artillery,
                        Ballistics, Eagle_Eye, First_Aid, Learning]
    skill_value_dict = {"Air_Magic": 5, "Archery": 4, "Armorer": 5, "Artillery": 1, "Ballistics": 1,
                        "Diplomacy": 4, "Eagle_Eye": 0, "Earth_Magic": 5, "Estates": 5, "Fire_Magic": 4,
                        "First_Aid": 0, "Intelligence": 3, "Leadership": 3, "Learning": 0, "Logistics": 5,
                        "Luck": 2, "Mysticism": 2, "Navigation": 3, "Necromancy": 5, "Offense": 5,
                        "Pathfinding": 3, "Resistance": 3, "Scholar": 3, "Scouting": 4, "Sorcery": 2,
                        "Tactics": 3, "Water_Magic": 4, "Wisdom": 4, "Interference": 3}

    if check_ok() != 3:
        print('to nie jest okienko lvl upa/wybierania skillsow')
        return
    test = []
    skills = []
    with mss() as sct:
        for i in range(2):
            monitor = {'top': 678, 'left': 869 + i * 94, 'width': 83,
                       'height': 46}
            screen = np.array(sct.grab(monitor))
            test.append(screen)

            screen = cv.cvtColor(screen, cv.COLOR_BGRA2BGR)
            text = ocr.read_text(screen)
            text = text.replace('\n', ' ')
            text = text.strip()
            for char in ["',.`;:\"-_‘"]:
                text = text.replace(char, '')

            if not text:
                print('nwm to chyba nie jest okienko do wyboru skillsow ziom')
                break
            level = text.split()[0]
            name = text.replace(level + ' ', "")
            name = name.replace(' ', '_')

            if level == 'Basic':
                level = 1
            elif level == 'Advanced':
                level = 2
            else:
                level = 3

            name = get_close_matches(name, skill_value_dict, 1)[0]

            if name[0] == 'S' and name[-1] == 'g':  # The most common problems when finding the correct skill
                name = 'Scouting'
            if name == "Artilery":
                name = "Artillery"
            skills.append((name, level))

    picked_skill = ''

    if h.herotype.lower() == 'main':
        if skills[0][0] in main_hero_skills and skills[1][0] in main_hero_skills:
            if main_hero_skills.index(skills[0][0]) < main_hero_skills.index(skills[1][0]):
                picked_skill = skills[0][0]
            else:
                picked_skill = skills[1][0]
        elif skills[0][0] in main_hero_skills and skills[1][0] not in main_hero_skills:
            picked_skill = skills[0][0]
        elif skills[0][0] not in main_hero_skills and skills[1][0] in main_hero_skills:
            picked_skill = skills[1][0]
        else:
            picked_skill = skills[0][0]
    else:
        picked_skill = skills[0][0]

    skill = []
    skill.append(skills[0][0])
    skill.append(skills[1][0])

    # print(skill.index(picked_skill))
    # print(picked_skill)

    # KLIKNIECIE NA ODPOWIEDNIEGO SKILLA
    level_up_choose_skill(skill.index(picked_skill) + 1)

    # print(skills[skill.index(picked_skill)][1])
    do_we_have_this_skill = False
    # DODAC UPDATE SKILLA W HERO
    for hero_skill in h.skills.secondary_skills:
        # jesli mamy tego skilla w skillach to updatujemy mu lvl
        if hero_skill.name == picked_skill:
            hero_skill.lvl = skills[skill.index(picked_skill)][1]
            do_we_have_this_skill = True

    if not do_we_have_this_skill:
        for hero_skill in h.skills.secondary_skills:
            if hero_skill.name == '':
                hero_skill.name = picked_skill
                hero_skill.lvl = skills[skill.index(picked_skill)][1]
                # hero_skill.value=0
                break

    time.sleep(0.5)
    skills_window(h)
