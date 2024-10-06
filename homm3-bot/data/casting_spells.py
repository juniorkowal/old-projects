import keyboard
from data.magic import *
from GUI_handling.BattleGUI import cast_spell_battle, attack_enemy, move_mouse_and_click_battle
from battleAI.reinforcmentLearningTest import divideIntoAllyAndEnemy
import image_processing.ocr as ocr
import pyautogui
import cv2 as cv
import numpy as np
from data.spell_database import list_of_spell_names, list_of_spells_lists, spell_ranking
from difflib import get_close_matches
import time
from image_processing.ok_detection import check_ok


def Choose_spell(spells, spells_database_classes, mana_costs, spell_levels, our_mana, target_priority):
    target_type_magic = 0
    offence_or_defence = 0
    chosen_spell = -1
    chosen_spell_name = ""
    highest_spell_level = max(spell_levels)
    for i in range(len(spell_ranking)):
        for j in range(len(spells_database_classes)):
            if spells_database_classes[j] != 'NULL':
                if spell_ranking[i] == spells_database_classes[j][0].class_of_spell.name:
                    if spell_levels[j] == highest_spell_level:
                        if target_priority == spells_database_classes[j][spell_levels[j]].type_offence_defence:
                            chosen_spell = j
                            break
        if chosen_spell != -1:
            break

    if chosen_spell == -1:
        for i in range(len(spell_ranking)):
            for j in range(len(spells_database_classes)):
                if spells_database_classes[j] != 'NULL':
                    if spell_ranking[i] == spells_database_classes[j][0].class_of_spell.name:
                        if spell_levels[j] == highest_spell_level:
                            chosen_spell = j
                            break
            if chosen_spell != -1:
                break

    if chosen_spell == -1:
        return -1, -1, -1, -1
    else:
        if spells_database_classes[chosen_spell][0].power == spell_levels[chosen_spell]:
            target_type_magic = spells_database_classes[chosen_spell][0].type_target
            offence_or_defence = spells_database_classes[chosen_spell][0].type_offence_defence
            chosen_spell_name = spells_database_classes[chosen_spell][0].class_of_spell.name

        elif spells_database_classes[chosen_spell][1].power == spell_levels[chosen_spell]:
            target_type_magic = spells_database_classes[chosen_spell][1].type_target
            offence_or_defence = spells_database_classes[chosen_spell][1].type_offence_defence
            chosen_spell_name = spells_database_classes[chosen_spell][1].class_of_spell.name

        elif spells_database_classes[chosen_spell][2].power == spell_levels[chosen_spell]:
            target_type_magic = spells_database_classes[chosen_spell][2].type_target
            offence_or_defence = spells_database_classes[chosen_spell][2].type_offence_defence
            chosen_spell_name = spells_database_classes[chosen_spell][2].class_of_spell.name
        return chosen_spell, chosen_spell_name, offence_or_defence, target_type_magic


def Detect_spells():
    """
    Taking a screenshot to detect all the possible spells we are able to use, and stores:
    - Mana status
    - Spell levels
    - Classes of available spells

    :return: spells(classes), database of spells(also with classes), mana costs of each spell, levels of spells, current mana
    """
    move_mouse_and_click_battle(655, 292)
    move_mouse_and_click_battle(655, 292)
    img_source = pyautogui.screenshot()
    img_source = cv.cvtColor(np.array(img_source), cv.COLOR_RGB2BGR)
    # img_source = cv.imread(r'spellbook_screen.png')

    img_mana = img_source[710:745, 1100:1130]
    current_mana = ocr.read_generic_text(img_mana)
    print("Our current mana: ", current_mana)

    spells_database_classes = []
    our_spells_classes = []
    spells_names_list = []
    detected_names_of_spells = []
    mana_costs_tab = []
    levels_of_spells = []

    print("Our available spells:")
    print(f"|           Name           | Lvl | Cost |")
    for z in range(2):
        for j in range(4):
            for i in range(3):
                mov_x = 95 * i
                mov_y = 96 * j
                if z == 0:
                    img_spell_1 = img_source[355 + mov_y:390 + mov_y, 665 + mov_x:750 + mov_x]
                elif z == 1:
                    img_spell_1 = img_source[355 + mov_y:390 + mov_y, 990 + mov_x:1075 + mov_x]
                current_spell = ocr.read_generic_text(img_spell_1)
                if len(current_spell) > 0:
                    level_of_spell = 0
                    if 'Ad' in current_spell:
                        level_of_spell = 1
                    elif 'Ex' in current_spell:
                        level_of_spell = 2
                    levels_of_spells.append(level_of_spell)
                    idx = current_spell.find(':')
                    do_continue = 1
                    if current_spell[idx + 2] == 'S':
                        first_cost = 5
                    elif current_spell[idx + 2] == '$':
                        first_cost = 8
                    elif current_spell[idx + 2].isnumeric():
                        first_cost = int(current_spell[idx + 2])
                    else:
                        mana_costs_tab.append(-1)
                        spells_names_list.append('NULL')
                        do_continue = 0
                    if do_continue == 1:
                        second_cost = 0
                        if len(current_spell) == idx + 4:
                            if current_spell[idx + 3] == 'S':
                                mana_cost = first_cost
                            else:
                                second_cost = int(current_spell[idx + 3])
                                mana_cost = first_cost * 10 + second_cost
                        else:
                            mana_cost = first_cost
                        mana_costs_tab.append(mana_cost)

                        current_spell = ocr.read_text(img_spell_1)
                        name_of_spell = current_spell.partition('\n')[0]
                        detected_names_of_spells.append(name_of_spell)
                        most_likely_spell = get_close_matches(name_of_spell, list_of_spell_names, 1)
                        if len(most_likely_spell) == 0:
                            spells_names_list.append('NULL')
                        else:
                            spells_names_list.append(most_likely_spell[0])
                            print(f"|{most_likely_spell[0]:25} |", f"{level_of_spell:2}  |", f"{mana_cost:3}  |")
    for k in range(2):
        if len(spells_names_list) == 24 or len(spells_names_list) == 48:
            move_mouse_and_click_battle(1260, 292)
            time.sleep(0.5)
            img_source = pyautogui.screenshot()
            img_source = cv.cvtColor(np.array(img_source), cv.COLOR_RGB2BGR)
            for z in range(2):
                for j in range(4):
                    for i in range(3):
                        mov_x = 95 * i
                        mov_y = 96 * j
                        if z == 0:
                            img_spell_1 = img_source[355 + mov_y:390 + mov_y, 665 + mov_x:750 + mov_x]
                        elif z == 1:
                            img_spell_1 = img_source[355 + mov_y:390 + mov_y, 990 + mov_x:1075 + mov_x]
                        current_spell = ocr.read_generic_text(img_spell_1)
                        if len(current_spell) > 0:
                            level_of_spell = 0
                            if 'Ad' in current_spell:
                                level_of_spell = 1
                            elif 'Ex' in current_spell:
                                level_of_spell = 2
                            levels_of_spells.append(level_of_spell)
                            idx = current_spell.find(':')
                            do_continue = 1
                            if current_spell[idx + 2] == 'S':
                                first_cost = 5
                            elif current_spell[idx + 2] == '$':
                                first_cost = 8
                            elif current_spell[idx + 2].isnumeric():
                                first_cost = int(current_spell[idx + 2])
                            else:
                                mana_costs_tab.append(-1)
                                spells_names_list.append('NULL')
                                do_continue = 0
                            if do_continue == 1:
                                second_cost = 0
                                if len(current_spell) == idx + 4:
                                    if current_spell[idx + 3] == 'S':
                                        mana_cost = first_cost
                                    else:
                                        second_cost = int(current_spell[idx + 3])
                                        mana_cost = first_cost * 10 + second_cost
                                else:
                                    mana_cost = first_cost
                                mana_costs_tab.append(mana_cost)

                                current_spell = ocr.read_text(img_spell_1)
                                name_of_spell = current_spell.partition('\n')[0]
                                detected_names_of_spells.append(name_of_spell)
                                most_likely_spell = get_close_matches(name_of_spell, list_of_spell_names, 1)
                                if len(most_likely_spell) == 0:
                                    spells_names_list.append('NULL')
                                else:
                                    spells_names_list.append(most_likely_spell[0])
                                    print(f"|{most_likely_spell[0]:25} |", f"{level_of_spell:2}  |", f"{mana_cost:3}  |")
    time.sleep(0.5)
    move_mouse_and_click_battle(655, 292)
    move_mouse_and_click_battle(655, 292)
    for j in range(len(spells_names_list)):
        name = 0
        for i in range(len(list_of_spells_lists)):
            if list_of_spells_lists[i][0].class_of_spell.name == spells_names_list[j]:
                our_spells_classes.append(list_of_spells_lists[i][0].class_of_spell.name)
                spells_database_classes.append(list_of_spells_lists[i])
                name = 1
                break
        if name == 0:
            our_spells_classes.append('NULL')
            spells_database_classes.append('NULL')

    print()
    print("Number of available spells: ", len(spells_names_list))
    print("Spell classes: ", our_spells_classes)
    # print("Mana cost for each spell: ", mana_costs_tab)
    # print("Level of each spell: ", levels_of_spells)
    return our_spells_classes, spells_database_classes, mana_costs_tab, levels_of_spells, current_mana


def Use_magic(setOfCreatures):
    """
    Uses function to find all available spells, picks the best out of spell ranking, throws a spell at ally or enemy,
    if spell won't affect anyone it will skip throwing spells, if we can't throw any spell it will also skip

    :param setOfCreatures: List of ally and enemy creatures on map
    :return:
    """
    ally, enemy = divideIntoAllyAndEnemy(setOfCreatures)
    x_enemy, y_enemy = enemy[0].field
    x_ally, y_ally = ally[0].field
    keyboard.press_and_release('c')
    time.sleep(0.5)
    spells, spells_database_classes, mana_costs, spell_levels, our_mana = Detect_spells()

    # 0 -> prioritize ally, 1 -> prioritize enemy,  2 -> prioritize nobody
    target_priority = 2
    if len(ally) > len(enemy) + 1:
        target_priority = 0
    elif len(ally) < len(enemy) + 1:
        target_priority = 1

    chosen_spell, chosen_spell_name, offence_or_defence, target_type_magic = Choose_spell(spells, spells_database_classes, mana_costs, spell_levels, our_mana, target_priority)
    if chosen_spell == -1:
        keyboard.press_and_release('esc')
        return (-1, -1), ""

    else:
        print('Name of spell: ', chosen_spell_name)
        print('Spell number: ', chosen_spell)
        time.sleep(0.5)
        cast_spell_battle(chosen_spell)
        time.sleep(0.5)

        for i in range(72):
            time.sleep(2)
            if check_ok() != 0:
                print('This spell affected nobody')
                time.sleep(0.5)
                keyboard.press_and_release('enter')
                time.sleep(0.5)
                spells_database_classes[chosen_spell] = 'NULL'
                chosen_spell, chosen_spell_name, offence_or_defence, target_type_magic = Choose_spell(spells, spells_database_classes, mana_costs, spell_levels, our_mana, target_priority)
                print('Name of spell: ', chosen_spell_name)
                print('Spell number: ', chosen_spell)
                time.sleep(0.5)
                keyboard.press_and_release('c')
                time.sleep(2)
                cast_spell_battle(chosen_spell)
            else:
                break

        if offence_or_defence == 0:
            if target_type_magic == 0:
                print('Targeting ally')
                attack_enemy(x_ally, y_ally, 'right')
            return (x_ally, y_ally), chosen_spell_name
        elif offence_or_defence == 1:
            if target_type_magic == 0:
                print('Targeting enemy')
                attack_enemy(x_enemy, y_enemy, 'left')
            return (x_enemy, y_enemy), chosen_spell_name
        else:
            return (-1, -1), chosen_spell_name

















