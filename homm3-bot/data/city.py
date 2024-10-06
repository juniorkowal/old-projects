"""Script containing city class representing casles in the game"""
import time
from copy import deepcopy

import cv2
import numpy as np
from colorama import Fore
from mss import mss

import GUI_handling.AdventureGUI
import image_processing.detecting_window
import image_processing.ok_detection
from GUI_handling import TownGUI as GUI
from data.building import *
from data.hero import Hero
from image_processing import ocr


class City:
    def __init__(self, mage_guild: MageGuild, fort: Fort, city_hall: CityHall, tavern: Tavern,
                 marketplace: Marketplace, resource_silo: ResourceSilo, blacksmith: Building, graal: bool = False,
                 upper_hero: Hero = Hero(0, "", "", 0, 0, 0, 0), lower_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 owned_by: str = 'neutral',
                 t1=Habitat((Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0)),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),0,Cost(0, 0, 0, 0, 0, 0, 0),Cost(0, 0, 0, 0, 0, 0, 0), 0, 0, "t1"),
                 t2=Habitat((Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0)),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),0,Cost(0, 0, 0, 0, 0, 0, 0),Cost(0, 0, 0, 0, 0, 0, 0), 0, 0, "t2"),
                 t3=Habitat((Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0)),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),0,Cost(0, 0, 0, 0, 0, 0, 0),Cost(0, 0, 0, 0, 0, 0, 0), 0, 0, "t3"),
                 t4=Habitat((Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0)),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),0,Cost(0, 0, 0, 0, 0, 0, 0),Cost(0, 0, 0, 0, 0, 0, 0), 0, 0, "t4"),
                 t5=Habitat((Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0)),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),0,Cost(0, 0, 0, 0, 0, 0, 0),Cost(0, 0, 0, 0, 0, 0, 0), 0, 0, "t5"),
                 t6=Habitat((Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0)),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),0,Cost(0, 0, 0, 0, 0, 0, 0),Cost(0, 0, 0, 0, 0, 0, 0), 0, 0, "t6"),
                 t7=Habitat((Cost(0, 0, 0, 0, 0, 0, 0), Cost(0, 0, 0, 0, 0, 0, 0)),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),Creature("", 0, 0, 0, (0, 0), 0, 0, 0, 0, 0, False, False, "",()),0,Cost(0, 0, 0, 0, 0, 0, 0),Cost(0, 0, 0, 0, 0, 0, 0), 0, 0, "t7"),):

        """
        Init function for a City Class.

        :param mage_guild: Mage guild object
        :param fort: Fort object
        :param city_hall: City hall object
        :param tavern: Tavern object
        :param marketplace: Marketplace object
        :param resource_silo: Resource silo object
        :param blacksmith: Blacksmith object
        :param graal: Boolean True - graal, False - no graal
        :param upper_hero: Hero object that is present in the higher row of the city slot bar
        :param lower_hero: Hero object that is present in the lower row of the city slot bar
        :param owned_by: Which player owns the building
        """

        self.creature_dwellings = [deepcopy(t1), deepcopy(t2), deepcopy(t3), deepcopy(t4), deepcopy(t5), deepcopy(t6),
                                   deepcopy(t7)]
        self.city = "City"
        self.fort = fort
        self.city_hall = city_hall
        self.mage_guild = mage_guild
        self.tavern = tavern
        self.marketplace = marketplace
        self.blacksmith = blacksmith
        self.name_of_city = ""
        self.resource_silo = resource_silo
        self.need_read = False
        self.graal = graal

        self.city_hero = upper_hero
        self.arriving_hero = lower_hero
        self.owned_by = owned_by
        self.value = 0
        self.textbox_width = int(150)
        self.textbox_height = int(16)
        self.position = (0,0)


    def end_day(self,player):
        """
        Buffer function
        """
        if self.city_hall.lvl == 1:
            player.gold += 500
        if self.city_hall.lvl == 2:
            player.gold += 1000
        if self.city_hall.lvl == 3:
            player.gold += 2000
        if self.city_hall.lvl == 4:
            player.gold += 4000

    def take_screenshot(self):
        """
        Takes a screenshot.

        :return: screenshot image
        """
        with mss() as sct:
            monitor = sct.monitors[1]
            img = np.array(sct.grab(monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            #cv2.imshow('win', img)
            #cv2.waitKey(0)
            return img

    def read_text(self, img):
        """
        Reads text from an image.

        :param img: input image
        :return: read text
        """
        text: str = ocr.read_generic_text(img, 2)
        return text

    def check_color(self, img):
        """
        Checks background color of an image where the text is.

        :param img: input image
        :return: one of four strings: 'green', 'yellow', 'red', 'gray'
        """
        if (img[0, 0, 0] == 123 and
            img[0, 0, 1] == 181 and
           img[0, 0, 2] == 115):
            return 'green'
        elif (img[0, 0, 0] == 99 and
              img[0, 0, 1] == 189 and
              img[0, 0, 2] == 231):
            return 'yellow'
        elif (img[0, 0, 0] == 123 and
              img[0, 0, 1] == 123 and
              img[0, 0, 2] == 255):
            return 'red'
        else:
            return 'gray'

    def give_text_and_color(self, img):
        """
        Returns text and color of the text's background.

        :param img: input image
        :return: name, color
        """
        name: str = self.read_text(img)
        color = self.check_color(img)
        return name, color

    def crop_city_hall(self, img):
        """
        Cropps city hall

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 594:594 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_citadel(self, img):
        """
        Cropps citadel

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 788:788 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_tavern(self, img):
        """
        Cropps tavern

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 982:982 + self.textbox_width]
        return 'Tavern', self.check_color(img_copy)

    def crop_blacksmith(self, img):
        """
        Cropps blacksmith

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 1176:1176 + self.textbox_width]
        return 'Blacksmith', self.check_color(img_copy)

    def crop_t1(self, img):
        """
        Cropps tier one unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 594:594 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t2(self, img):
        """
        Cropps tier two unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 788:788 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t3(self, img):
        """
        Cropps tier three unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 982:982 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t4(self, img):
        """
        Cropps tier four unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 1176:1176 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t5(self, img):
        """
        Cropps tier five unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[765:765 + self.textbox_height, 691:691 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t6(self, img):
        """
        Cropps tier six unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[765:765 + self.textbox_height, 885:885 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t7(self, img):
        """
        Cropps tier seven unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[765:765 + self.textbox_height, 1079:1079 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def action(self, player, hero: Hero, okay=0):
        """
        Responsible for buying units

        :param okay: Okay parameter  -> which okay window popped up
        :param player: player object
        :param hero: Hero object
        """
        print(hero)
        if self not in player.cities:
            image_processing.detecting_window.execute_detecting(hero)
            player.cities.append(self)
            self.need_read = True

        detected = 1
        while detected == 1:
            detected = image_processing.ok_detection.check_ok()
            if detected == 1:
                GUI_handling.AdventureGUI.accept_offer()

        creatures = [0, 0, 0, 0, 0, 0, 0]
        amounts = [0, 0, 0, 0, 0, 0, 0]
        upgraded = False
        print("###################### [START BUY/UPGRADE] ##################################")
        print(Fore.LIGHTMAGENTA_EX, f"[UPGRADING UNITS]", Fore.RESET)
        for habitat in reversed(self.creature_dwellings):  # upgrade all possible units
            if habitat.lvl == 2:
                for i, slot in enumerate(hero.slots.slots):
                    if slot.unit == habitat.unit_type and player.gold > slot.amount * (
                            habitat.unit_cost_up.gold - habitat.unit_cost.gold):
                        GUI.upgrade_unit(9 + i)
                        upgraded = True
                        player.gold -= slot.amount * (
                                habitat.unit_cost_up.gold - habitat.unit_cost.gold)
                        print(Fore.YELLOW, f"{slot.unit} {slot.amount}", Fore.RESET)

        print(Fore.LIGHTMAGENTA_EX, f"[BUYING UNITS]", Fore.RESET)
        print(Fore.LIGHTYELLOW_EX, f"[GOLD BEFORE BUY]: {player.gold}", Fore.RESET)

        for i, habitat in enumerate(
                reversed(self.creature_dwellings)):  # buy all possible  units from highest tier to lowest
            if habitat.lvl == 1:

                cost = 0
                amount = 0
                while player.gold > cost and amount < habitat.unit_ready:  # only gold because most units cost only gold
                    amount += 1
                    cost += habitat.unit_cost.gold

                player.gold -= cost
                amounts[i] = amount
                creatures[i] = habitat.unit_type
                print(Fore.GREEN, f"UNIT: {habitat.unit_type}", Fore.RESET)
                print(Fore.LIGHTYELLOW_EX, f"GOLD: {cost}", Fore.RESET)
                print(Fore.LIGHTCYAN_EX, f"AMOUNT: {amount}", Fore.RESET)
            elif habitat.lvl == 2:
                cost = 0
                amount = 0
                while player.gold > cost and amount < habitat.unit_ready:  # only gold because most units cost only gold
                    amount += 1
                    cost += habitat.unit_cost_up.gold
                player.gold -= cost
                amounts[i] = amount
                creatures[i] = habitat.unit_type_up
                print(Fore.GREEN, f"UNIT: {habitat.unit_type}", Fore.RESET)
                print(Fore.LIGHTYELLOW_EX, f"GOLD: {cost}", Fore.RESET)
                print(Fore.LIGHTCYAN_EX, f"AMOUNT: {amount}", Fore.RESET)
        if upgraded:
            for i in range(8, 16):
                GUI.merge_stacks_unit(i)
                time.sleep(0.1)

        slot = 0
        for i in range(7):
            if amounts[i] != 0:
                slot = -1
                for j, x in enumerate(self.city_hero.slots.slots):
                    if x.unit.name == creatures[i].name:
                        slot = j
                        break
                if slot == -1:
                    for j, x in enumerate(self.city_hero.slots.slots):
                        if x.unit.name == "":
                            x.amount = 0
                            slot = j
                            break
                if slot != -1:
                    self.city_hero.slots.slots[slot].unit = creatures[i]
                    self.city_hero.slots.slots[slot].amount = amounts[i] + self.city_hero.slots.slots[slot].amount

        for y in self.city_hero.slots.slots:
            slot = -1
            for i, x in enumerate(hero.slots.slots):
                if x.unit.name == y.unit.name:
                    slot = i
            if slot == -1:
                for i, x in enumerate(hero.slots.slots):
                    if x.unit.name == "":
                        if slot == -1:
                            x.amount = 0
                            slot = i
            if slot != -1:
                hero.slots.slots[slot].amount = y.amount + hero.slots.slots[slot].amount
                hero.slots.slots[slot].unit = y.unit
        time.sleep(0.1)
        GUI.recruit_unit("all")
        time.sleep(0.1)
        GUI.move_all_units_to_other_side(1)
        from GUI_handling.AdventureGUI import leave_screen
        leave_screen()

        for i, habitat in enumerate(reversed(self.creature_dwellings)):
            habitat.unit_ready -= amounts[i]

        print(f"[PLAYER GOLD AFTER]:{Fore.LIGHTYELLOW_EX} {player.gold}", Fore.RESET)
        print("######################## [END BUY/UPGRADE] ################################")

    def __eq__(self, other):
        if issubclass(type(other), City):
            return self.name_of_city == other.name_of_city
        else:
            return False







