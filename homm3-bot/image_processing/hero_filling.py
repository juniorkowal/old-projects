import math
from data.hero import Hero, SecondarySkill, Slot, hero_dict
from battleAI.BattleAI import initialize_QNN
from mss import mss
import numpy as np
import cv2
import image_processing.ocr as ocr
from image_processing.dictionaries import battle_dict
from image_processing.ok_detection import check_ok
from difflib import get_close_matches
from GUI_handling.AdventureGUI import level_up_choose_skill


class Finder:
    def __init__(self):
        self.qnn = initialize_QNN()
        self._skill_value_dict = {"Air_Magic": 5, "Archery": 4, "Armorer": 5, "Artillery": 1, "Ballistics": 1,
                                  "Diplomacy": 4, "Eagle_Eye": 0, "Earth_Magic": 5, "Estates": 5, "Fire_Magic": 4,
                                  "First_Aid": 0, "Intelligence": 3, "Leadership": 3, "Learning": 0, "Logistics": 5,
                                  "Luck": 2, "Mysticism": 2, "Navigation": 3, "Necromancy": 5, "Offense": 5,
                                  "Pathfinding": 3, "Resistance": 3, "Scholar": 3, "Scouting": 4, "Sorcery": 2,
                                  "Tactics": 3, "Water_Magic": 4, "Wisdom": 4, "Interference": 3}
        self._to_replace = "',.`;:\"-_‘"
        self._might_class_names = ['Knight', 'Ranger', 'Alchemist', 'Demoniac', 'Death_Knight', 'Overlord',
                                   'Barbarian', 'Beastmaster', 'Planeswalker', 'Captain']
        self._magic_class_names = ['Cleric', 'Druid', 'Wizard', 'Heretic', 'Necromancer', 'Warlock',
                                   'Battle_Mage', 'Witch', 'Elementalist', 'Navigator']



    def find_all(self, h: Hero):
        """
        Combines all the functions inside the Finder class, so it's not necessary to use them independently if
        every function needs to be used

        :param h: Given hero
        """
        self.find_units(h)
        self.find_skills(h)
        self.find_main_attr(h)
        self.find_attributes(h)

    def find_units_portraits(self):  # model has to be already initialized
        """
        Finds which units our army consists of without finding their numbers. Before checking you have to enter
        the hero inventory

        :return: Either returns an instance of a found unit or None if no unit was found
        """
        screens = []
        with mss() as sct:
            for i in range(7):
                monitor = {'top': 732, 'left': 639 + i*66, 'width': 57, 'height': 63}
                screen = np.array(sct.grab(monitor))
                screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2GRAY)
                screen = cv2.resize(screen, (36, 38))
                screens.append(screen)
        a = np.array(screens)
        units = self.qnn.model.predict(np.array(screens), batch_size=7)  #TODO: inny model pewnie
        units2 = []
        for i in range(7):
            units2.append(int((np.where(units[i] == np.amax(units[i])))[0]))
        units = np.array([*map(battle_dict.get, units2)])
        units_proper = []
        for unit in units:
            if unit != 'obstacle':
                units_proper.append(unit)
            else:
                units_proper.append(None)
        return units_proper

    def find_units_amount(self):
        """
        Finds the exact amount of certain units a hero has. It checks all the spaces from left to right, up to down
        and return their value. There's no need to enter the hero inventory, as long as the units are visible on the
        right side of the screen.

        :return: Number of units in hero slots. Returns 0 if no number was found
        """
        screens = []
        amounts = []
        with mss() as sct:
            coords = []
            for i in range(3):
                coords.append((571, 1769 + i*36, 34, 11))
            for i in range(4):
                coords.append((619, 1751 + i*36, 34, 11))
            for i in range(7):
                monitor = {'top': coords[i][0], 'left': coords[i][1], 'width': coords[i][2], 'height': coords[i][3]}
                screen = np.array(sct.grab(monitor))
                screens.append(screen)
        for screen in screens:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
            text = ocr.read_text_faster(screen, 4)
            text = text.replace('\n', ' ')
            text = text.strip()
            if not text:
                amounts.append(0)
            else:
                amounts.append(int(text))
        return amounts

    def find_units(self, h:Hero):
        """
        Combine find_units_portraits and find_units_amount and fill in the hero

        :param h: Our hero
        """
        units = self.find_units_portraits()
        amounts = self.find_units_amount()
        for i in range(7):
            if not units[i]:
                h.slots.slots[i] = Slot()
            else:
                h.slots.slots[i] = Slot(units[i], amounts[i])

    def find_attributes(self, h: Hero):  # Sometimes finds inaccurate numbers because of them being small
        """
        Find attack, defense, knowledge and spell power of a hero. Before checking you have to enter
        the hero inventory.

        :param h: Hero to insert the values to
        """
        with mss() as sct:
            for i in range(4):
                monitor = {'top': 406, 'left': 670 + i * 70, 'width': 13, 'height': 12}
                screen = np.array(sct.grab(monitor))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
                text = ocr.read_generic_text(screen, 2)
                if i == 0:
                    try:
                        h.attack = int(text)
                    except Exception:
                        h.attack = 0
                elif i == 1:
                    try:
                        h.defense = int(text)
                    except Exception:
                        h.defense = 0
                elif i == 2:
                    try:
                        h.spellpower = int(text)
                    except Exception:
                        h.spellpower = 0
                else:
                    try:
                        h.knowledge = int(text)
                    except Exception:
                        h.knowledge = 0

    def find_skills(self, h: Hero):  # TODO: Specialties or main skills are not defined
        """
        Finds the abilities of our hero. You need to be in the hero inventory. Inserts found skills into the appropriate
        skill slots, if no skill is found inserts a default SecondarySkill instance. Uses difflib.get_close_matches
        to make sure the found skill is always correct even if tesseract finds teh text slightly wrong

        :param h: Hero to insert the values to
        """
        test = []
        with mss() as sct:
            for i in range(8):
                monitor = {'top': 524 + int(math.floor(i / 2) * 48), 'left': 688 + (i % 2) * 143, 'width': 91,
                           'height': 42}
                screen = np.array(sct.grab(monitor))
                test.append(screen)
                text = self._hero_ocr(screen)
                if not text:
                    continue
                level = text.split()[0]
                name = text.replace(level + ' ', "")
                name = name.replace(' ', '_')
                if level == 'Basic':
                    level = 1
                elif level == 'Advanced':
                    level = 2
                else:
                    level = 3
                if name == "_fra-":
                    name = "necromancy"
                name = get_close_matches(name, self._skill_value_dict, 1)[0]
                try:
                    h.skills.secondary_skills[i] = SecondarySkill(level, name, self._skill_value_dict[name])
                except Exception as ex:
                    pass

    def find_main_attr(self, h: Hero):
        """
        Finds the name, hero_type and level of the chosen hero. You have to be inside the hero inventory.

        :param h: Hero to fill the values to
        """
        with mss() as sct:
            monitor = {'top': 272, 'left': 713, 'width': 202, 'height': 24}
            screen = np.array(sct.grab(monitor))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

            text = self._hero_ocr_name(screen)
            text = get_close_matches(text, hero_dict, 1)[0]
            h.name = text
            hero_attr = hero_dict[h.name]
            h.speciality = hero_attr[1]
            h.mspoints = hero_attr[5]
            monitor = {'top': 300, 'left': 713, 'width': 202, 'height': 24}
            screen = np.array(sct.grab(monitor))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
            text = self._hero_ocr(screen)
            split_text = text.split()
            h.lvl = int(split_text[1])
            if len(split_text) == 4:
                split_text[2] = split_text[2] + split_text[3]
                split_text[2].replace(' ', '_')
            if split_text[2] in self._might_class_names:
                h.heroclass = 'might'
            else:
                h.heroclass = 'magic'

    def _hero_ocr(self, screen):
        """
        Simple text reading with basic text edition afterwards

        :param screen: np.array that corresponds to a part of a screenshot
        :return: Found text without the leading and tailing whitespaces and with every \n exchanged to a whitespace
        """
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        text = ocr.read_text(screen)
        text = text.replace('\n', ' ')
        text = text.strip()
        for char in self._to_replace:
            text = text.replace(char, '')
        return text

    def _hero_ocr_name(self, screen):
        """
        Function that helps read the name of the hero

        :param screen:
        :return:
        """
        scale = 3
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
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
        for char in self._to_replace:
            text = text.replace(char, '')

        return text


# def skills_window(h):
#
#     skill_value_dict={"Air_Magic": 5, "Archery": 4, "Armorer": 5, "Artillery": 1, "Ballistics": 1,
#                                   "Diplomacy": 4, "Eagle_Eye": 0, "Earth_Magic": 5, "Estates": 5, "Fire_Magic": 4,
#                                   "First_Aid": 0, "Intelligence": 3, "Leadership": 3, "Learning": 0, "Logistics": 5,
#                                   "Luck": 2, "Mysticism": 2, "Navigation": 3, "Necromancy": 5, "Offense": 5,
#                                   "Pathfinding": 3, "Resistance": 3, "Scholar": 3, "Scouting": 4, "Sorcery": 2,
#                                   "Tactics": 3, "Water_Magic": 4, "Wisdom": 4, "Interference": 3}
#
#     if check_ok()!=3:
#         print('to nie jest okienko lvl upa/wybierania skillsow')
#         return
#     test = []
#     skills=[]
#     with mss() as sct:
#         for i in range(2):
#             monitor = {'top': 678, 'left': 869+i*94, 'width': 83,
#                         'height': 46}
#             screen = np.array(sct.grab(monitor))
#             test.append(screen)
#
#             screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
#             text = ocr.read_text(screen)
#             text = text.replace('\n', ' ')
#             text = text.strip()
#             for char in ["',.`;:\"-_‘"]:
#                 text = text.replace(char, '')
#
#             if not text:
#                 print('nwm to chyba nie jest okienko do wyboru skillsow ziom')
#                 break
#             level = text.split()[0]
#             name = text.replace(level + ' ', "")
#             name = name.replace(' ', '_')
#
#             if level == 'Basic':
#                 level = 1
#             elif level == 'Advanced':
#                 level = 2
#             else:
#                 level = 3
#
#             name = get_close_matches(name, skill_value_dict, 1)[0]
#
#             if name[0] == 'S' and name[-1] == 'g':  # The most common problems when finding the correct skill
#                 name = 'Scouting'
#             if name == "Artilery":
#                 name = "Artillery"
#             skills.append((name,level))
#
#     picked_skill=''
#
#     if h.herotype.lower()=='main':
#         if skills[0][0] in main_hero_skills and skills[1][0] in main_hero_skills:
#             if main_hero_skills.index(skills[0][0])>main_hero_skills.index(skills[1][0]):
#                 picked_skill=skills[1][0]
#             else:
#                 picked_skill=skills[1][0]
#         elif skills[0][0] in main_hero_skills and skills[1][0] not in main_hero_skills:
#             picked_skill=skills[0][0]
#         elif skills[0][0] not in main_hero_skills and skills[1][0] in main_hero_skills:
#             picked_skill=skills[1][0]
#         else:
#             picked_skill=skills[0][0]
#     else:
#         picked_skill=skills[0][0]
#
#     skill=[]
#     skill.append(skills[0][0])
#     skill.append(skills[1][0])
#
#     #print(skill.index(picked_skill))
#     #print(picked_skill)
#
#     # KLIKNIECIE NA ODPOWIEDNIEGO SKILLA
#     level_up_choose_skill(skill.index(picked_skill)+1)
#
#     #print(skills[skill.index(picked_skill)][1])
#     do_we_have_this_skill=False
#     # DODAC UPDATE SKILLA W HERO
#     for hero_skill in h.skills.secondary_skills:
#         # jesli mamy tego skilla w skillach to updatujemy mu lvl
#         if hero_skill.name==picked_skill:
#             hero_skill.lvl=skills[skill.index(picked_skill)][1]
#             do_we_have_this_skill=True
#
#     if not do_we_have_this_skill:
#         for hero_skill in h.skills.secondary_skills:
#             if hero_skill.name=='':
#                 hero_skill.name=picked_skill
#                 hero_skill.lvl=skills[skill.index(picked_skill)][1]
#                 #hero_skill.value=0
#                 break


