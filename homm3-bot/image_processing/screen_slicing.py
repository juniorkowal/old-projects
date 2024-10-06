"""Script containing classes and functions needed for extracting elements that are present on the screen"""
import time
from GUI_handling.BattleGUI import move_to_portrait
import cv2
import numpy as np
# import tesserocr
from mss import mss
import os
from mouse import move
from image_processing.ocr import read_generic_numbers
from data.building import Cost


class ScreenStorage:
    def __init__(self,color = "Red"):
        """
        initialization of all storage elements and some loading of files for color checking functions
        """
        self.our_color = color
        self.cells = np.empty((54, 32))
        self.battle_cells_even = np.empty((5, 11))
        self.battle_cells_odd = np.empty((6, 11))
        self.resources = []
        self.units_small = []
        self.queue = []
        self.screen_even = np.empty((420, 660, 3))
        self.screen_odd = np.empty((504, 660, 3))
        self.screen = []
        self.screen_even_old = np.empty((420, 660, 3),dtype=np.uint8)
        self.screen_odd_old = np.empty((504, 660, 3),dtype=np.uint8)
        self.battle_cells = np.empty((11, 15))
        self.quantity = []
        self.queue_color = []
        self.screen_admap = []
        self.stripsInQueueColorImages = readColors()
        self.adventure_map = []
        self.test = []
        self.colors_small_map = readColors2()
        self.hero_positions = []
        self.possible_units = []
        self.last_turn_units = []

    def take_adventure_map(self):
        """
        function taking screenshot and slicing it a way to have each tile of adventure map under different index in list
        """
        with mss() as sct:
            monitor = {'top': 40, 'left': 32, 'width': 1664, 'height': 960}
            screen = np.array(sct.grab(monitor))
            screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
            self.cells = screen.reshape(30, 32, 52, 32, 3)
            self.cells = self.cells.swapaxes(1, 2)
            temp1 = []
            for y in range(30):
                z = self.cells[y]
                for x in range(52):
                    img = cv2.resize(z[x], (11, 11))
                    temp1.append(img)
            self.cells = np.array(temp1)

    def take_battle_templates(self):
        """
        function taking screenshot of battle image
        """
        with mss() as sct:
            monitor = {'top': 263, 'left': 618, 'width': 683, 'height': 505}
            self.screen = np.array(sct.grab(monitor))
            self.screen = cv2.cvtColor(self.screen, cv2.COLOR_RGBA2RGB)

    def take_adventure_templates(self):
        """
        function taking image of adventure map
        """
        with mss() as sct:
            monitor = {'top': 35, 'left': 27, 'width': 1674, 'height': 970}
            self.screen_admap = np.array(sct.grab(monitor))
            self.screen_admap = cv2.cvtColor(self.screen_admap, cv2.COLOR_RGBA2RGB)

    def take_battle(self):
        """
        function creating a list with each possible place for unit in battle with image of that place
        """
        with mss() as sct:
            self.screen_odd_old = self.screen_odd
            self.screen_even_old = self.screen_even
            monitor_odd = {'top': 263, 'left': 640, 'width': 660, 'height': 504}
            self.screen_odd = np.array(sct.grab(monitor_odd))
            monitor_even = {'top': 305, 'left': 618, 'width': 660, 'height': 420}
            self.screen_even = np.array(sct.grab(monitor_even))
            self.screen_odd = cv2.cvtColor(self.screen_odd, cv2.COLOR_RGBA2RGB)
            self.screen_even = cv2.cvtColor(self.screen_even, cv2.COLOR_RGBA2RGB)
            screen1 = self.screen_odd_old.copy()
            screen2 = self.screen_odd.copy()
            screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGR2GRAY)
            screen3 = cv2.absdiff(screen1, screen2)
            screen3 = cv2.threshold(screen3, 0, 15, cv2.THRESH_BINARY)
            screen1 = cv2.bitwise_and(self.screen_odd, self.screen_odd, mask=screen3[1])
            self.battle_cells_odd = screen1.reshape(6, 84, 15, 44, 3)
            screen1 = self.screen_even_old.copy()
            screen2 = self.screen_even.copy()
            screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGR2GRAY)
            screen3 = cv2.absdiff(screen1, screen2)
            screen3 = cv2.threshold(screen3, 0, 15, cv2.THRESH_BINARY)
            screen1 = cv2.bitwise_and(self.screen_even, self.screen_even, mask=screen3[1])
            self.battle_cells_even = screen1.reshape(5, 84, 15, 44, 3)
            self.battle_cells_even = self.battle_cells_even.swapaxes(1, 2)

            self.battle_cells_odd = self.battle_cells_odd.swapaxes(1, 2)
            self.battle_cells = [[self.battle_cells_odd[0]], [self.battle_cells_even[0]],
                                 [self.battle_cells_odd[1]],
                                 [self.battle_cells_even[1]], [self.battle_cells_odd[2]],
                                 [self.battle_cells_even[2]],
                                 [self.battle_cells_odd[3]], [self.battle_cells_even[3]],
                                 [self.battle_cells_odd[4]],
                                 [self.battle_cells_even[4]], [self.battle_cells_odd[5]]]
            self.battle_cells_even = self.battle_cells_even.swapaxes(0, 1)
            self.battle_cells_odd = self.battle_cells_odd.swapaxes(0, 1)
            temp1 = []
            for y in range(11):
                z = self.battle_cells[y]
                z = z[0]
                for x in range(15):
                    img = z[x].copy()
                    img = cv2.resize(img, (9, 17))
                    temp1.append(img)
            self.battle_cells = np.array(temp1)

    def take_possible_units(self):
        """
        function creating a list with each possible place for unit in battle
        """
        with mss() as sct:
            monitor_odd = {'top': 263, 'left': 640, 'width': 660, 'height': 504}
            self.screen_odd = np.array(sct.grab(monitor_odd))
            monitor_even = {'top': 305, 'left': 618, 'width': 660, 'height': 420}
            self.screen_even = np.array(sct.grab(monitor_even))
            self.screen_odd = cv2.cvtColor(self.screen_odd, cv2.COLOR_RGBA2RGB)
            self.screen_even = cv2.cvtColor(self.screen_even, cv2.COLOR_RGBA2RGB)
            screen1 = self.screen_odd_old.copy()
            screen2 = self.screen_odd.copy()
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGR2GRAY)
            screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
            screen3 = cv2.absdiff(screen1, screen2)
            #screen3 = cv2.threshold(screen3, 0, 15, cv2.THRESH_BINARY)
            #screen1 = cv2.bitwise_and(self.screen_odd, self.screen_odd, mask=screen3[1])
            self.battle_cells_odd = screen3.reshape(6, 84, 15, 44)
            screen1 = self.screen_even_old.copy()
            screen2 = self.screen_even.copy()
            screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGR2GRAY)
            screen3 = cv2.absdiff(screen1, screen2)
            #screen3 = cv2.threshold(screen3, 0, 15, cv2.THRESH_BINARY)
            #screen1 = cv2.bitwise_and(self.screen_even, self.screen_even, mask=screen3[1])
            self.battle_cells_even = screen3.reshape(5, 84, 15, 44)
            self.battle_cells_even = self.battle_cells_even.swapaxes(1, 2)

            self.battle_cells_odd = self.battle_cells_odd.swapaxes(1, 2)
            self.battle_cells = [[self.battle_cells_odd[0]], [self.battle_cells_even[0]],
                                 [self.battle_cells_odd[1]],
                                 [self.battle_cells_even[1]], [self.battle_cells_odd[2]],
                                 [self.battle_cells_even[2]],
                                 [self.battle_cells_odd[3]], [self.battle_cells_even[3]],
                                 [self.battle_cells_odd[4]],
                                 [self.battle_cells_even[4]], [self.battle_cells_odd[5]]]
            self.battle_cells_even = self.battle_cells_even.swapaxes(0, 1)
            self.battle_cells_odd = self.battle_cells_odd.swapaxes(0, 1)
            temp1 = []
            for y in range(11):
                z = self.battle_cells[y]
                z = z[0]
                for x in range(15):
                    img = z[x].copy()
                    img = cv2.resize(img, (1, 1))
                    if img > 10:
                        temp1.append(True)
                    else:
                        temp1.append(False)
            for x in self.last_turn_units:
                temp1[15*x[1]+x[0]] = True
            self.possible_units = np.array(temp1)
            self.screen_even_old=self.screen_even
            self.screen_odd_old = self.screen_odd

    def take_possible_units_temp(self, terrain):
        """
        function creating a list with each possible place for unit in battle
        """
        with mss() as sct:
            terrain_even = terrain
            terrain_odd = terrain
            monitor_odd = {'top': 263, 'left': 640, 'width': 660, 'height': 504}
            self.screen_odd = np.array(sct.grab(monitor_odd))
            monitor_even = {'top': 305, 'left': 618, 'width': 660, 'height': 420}
            self.screen_even = np.array(sct.grab(monitor_even))
            self.screen_odd = cv2.cvtColor(self.screen_odd, cv2.COLOR_RGBA2RGB)
            self.screen_even = cv2.cvtColor(self.screen_even, cv2.COLOR_RGBA2RGB)
            screen1 = terrain_odd.copy()
            screen2 = self.screen_odd.copy()
            screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGR2GRAY)
            screen3 = cv2.absdiff(screen1, screen2)
            screen3 = cv2.threshold(screen3, 0, 15, cv2.THRESH_BINARY)
            screen1 = cv2.bitwise_and(self.screen_odd, self.screen_odd, mask=screen3[1])
            self.battle_cells_odd = screen1.reshape(6, 84, 15, 44, 3)
            screen1 = terrain_even.copy()
            screen2 = self.screen_even.copy()
            screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGR2GRAY)
            screen3 = cv2.absdiff(screen1, screen2)
            screen3 = cv2.threshold(screen3, 0, 15, cv2.THRESH_BINARY)
            screen1 = cv2.bitwise_and(self.screen_even, self.screen_even, mask=screen3[1])
            self.battle_cells_even = screen1.reshape(5, 84, 15, 44, 3)
            self.battle_cells_even = self.battle_cells_even.swapaxes(1, 2)

            self.battle_cells_odd = self.battle_cells_odd.swapaxes(1, 2)
            self.battle_cells = [[self.battle_cells_odd[0]], [self.battle_cells_even[0]],
                                 [self.battle_cells_odd[1]],
                                 [self.battle_cells_even[1]], [self.battle_cells_odd[2]],
                                 [self.battle_cells_even[2]],
                                 [self.battle_cells_odd[3]], [self.battle_cells_even[3]],
                                 [self.battle_cells_odd[4]],
                                 [self.battle_cells_even[4]], [self.battle_cells_odd[5]]]
            self.battle_cells_even = self.battle_cells_even.swapaxes(0, 1)
            self.battle_cells_odd = self.battle_cells_odd.swapaxes(0, 1)
            temp1 = []
            for y in range(11):
                z = self.battle_cells[y]
                z = z[0]
                for x in range(15):
                    img = z[x].copy()
                    img = cv2.resize(img, (1, 1))
                    if img > 20:
                        temp1.append(True)
                    else:
                        temp1.append(False)
            self.possible_units = np.array(temp1)

    def take_queue_to_find_unit_raw(self):
        """
        function creating list of unit portraits from queue
        """
        move(0, 0, duration=0)
        time.sleep(0.08)
        self.queue = []
        self.queue_color = []
        with mss() as sct:
            monitor = {'top': 776, 'left': 660, 'width': 600, 'height': 56}
            screen = np.array(sct.grab(monitor))
            screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
            screen = np.reshape(screen, (56, 15, 40, 3))
            screen = screen.swapaxes(0, 1)
            for x in range(15):
                img = screen[x]
                cv2.rectangle(img, (3, 3), (37, 53), (0, 0, 0), -1)
                self.queue.append(img)

    def take_queue_to_find_unit(self, x, y):
        """
        function taking unit borders from queue to find at which unit we are pointing

        :param x: x index of tile in battle
        :param y: y index of tile in battle
        """
        self.queue = []
        self.queue_color = []
        temp_move(x, y)
        time.sleep(0.08)
        with mss() as sct:
            for x in range(15):
                monitor = {'top': 776, 'left': 660 + x * 40, 'width': 40, 'height': 56}
                screen = np.array(sct.grab(monitor))
                screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
                cv2.rectangle(screen, (3, 3), (37, 53), (0, 0, 0), -1)
                self.queue.append(screen)

    def take_battle_map(self, num):
        """
        function taking differential image between battle when we are pointing to current unit and selected unit other than that similar to take_battle

        :param num: number of unit for which we are checking posiible places
        """
        with mss() as sct:
            move_to_portrait(0)
            time.sleep(0.08)
            monitor_odd = {'top': 263, 'left': 640, 'width': 660, 'height': 504}
            self.screen_odd = np.array(sct.grab(monitor_odd))
            monitor_even = {'top': 305, 'left': 618, 'width': 660, 'height': 420}
            self.screen_even = np.array(sct.grab(monitor_even))
            self.screen_odd = cv2.cvtColor(self.screen_odd, cv2.COLOR_RGBA2RGB)
            self.screen_even = cv2.cvtColor(self.screen_even, cv2.COLOR_RGBA2RGB)
            self.screen_odd, g, r = cv2.split(self.screen_odd)
            self.screen_even, g, r = cv2.split(self.screen_even)
            # self.screen_odd = canny(self.screen_odd)
            # self.screen_even = canny(self.screen_even)
            screen11 = self.screen_odd.copy()
            screen12 = self.screen_even.copy()
            move_to_portrait(num)
            time.sleep(0.08)
            self.screen_odd = np.array(sct.grab(monitor_odd))
            self.screen_even = np.array(sct.grab(monitor_even))
            self.screen_odd = cv2.cvtColor(self.screen_odd, cv2.COLOR_RGBA2RGB)
            self.screen_even = cv2.cvtColor(self.screen_even, cv2.COLOR_RGBA2RGB)
            self.screen_odd, g, r = cv2.split(self.screen_odd)
            self.screen_even, g, r = cv2.split(self.screen_even)
            # self.screen_odd = canny(self.screen_odd)
            # self.screen_even = canny(self.screen_even)
            screen21 = self.screen_odd.copy()
            # screen11 = cv2.cvtColor(screen11, cv2.COLOR_BGR2GRAY)
            # screen21 = cv2.cvtColor(screen21, cv2.COLOR_BGR2GRAY)
            screen31 = cv2.absdiff(screen11, screen21)
            screen31 = cv2.threshold(screen31, 0, 5, cv2.THRESH_BINARY)
            screen11 = cv2.bitwise_and(self.screen_odd, self.screen_odd, mask=screen31[1])

            self.test.append(screen11)
            self.battle_cells_odd = screen11.reshape(6, 84, 15, 44, 1)
            screen22 = self.screen_even.copy()
            # screen12 = cv2.cvtColor(screen12, cv2.COLOR_BGR2GRAY)
            # screen22 = cv2.cvtColor(screen22, cv2.COLOR_BGR2GRAY)
            screen32 = cv2.absdiff(screen12, screen22)
            screen32 = cv2.threshold(screen32, 0, 20, cv2.THRESH_BINARY)
            screen12 = cv2.bitwise_and(self.screen_even, self.screen_even, mask=screen32[1])
            self.battle_cells_even = screen12.reshape(5, 84, 15, 44, 1)
            self.battle_cells_even = self.battle_cells_even.swapaxes(1, 2)

            self.battle_cells_odd = self.battle_cells_odd.swapaxes(1, 2)
            self.battle_cells = [[self.battle_cells_odd[0]], [self.battle_cells_even[0]], [self.battle_cells_odd[1]],
                                 [self.battle_cells_even[1]], [self.battle_cells_odd[2]], [self.battle_cells_even[2]],
                                 [self.battle_cells_odd[3]], [self.battle_cells_even[3]], [self.battle_cells_odd[4]],
                                 [self.battle_cells_even[4]], [self.battle_cells_odd[5]]]
            self.battle_cells_even = self.battle_cells_even.swapaxes(0, 1)
            self.battle_cells_odd = self.battle_cells_odd.swapaxes(0, 1)
            temp1 = []
            for y in range(11):
                z = self.battle_cells[y]
                z = z[0]
                for x in range(15):
                    img = z[x].copy()
                    # img = cv2.resize(img, (9, 17))
                    temp1.append(img)
            self.battle_cells = np.array(temp1)

    def take_battle_map_first(self):
        """
        obsolete function for taking battle image
        """
        with mss() as sct:
            self.screen_odd_old = self.screen_odd
            self.screen_even_old = self.screen_even
            monitor_odd = {'top': 263, 'left': 640, 'width': 660, 'height': 504}
            self.screen_odd = np.array(sct.grab(monitor_odd))
            monitor_even = {'top': 305, 'left': 618, 'width': 660, 'height': 420}
            self.screen_even = np.array(sct.grab(monitor_even))
            self.screen_odd = cv2.cvtColor(self.screen_odd, cv2.COLOR_RGBA2RGB)
            self.screen_even = cv2.cvtColor(self.screen_even, cv2.COLOR_RGBA2RGB)
            self.battle_cells_odd = self.screen_odd.reshape(6, 84, 15, 44, 3)
            self.battle_cells_even = self.screen_even.reshape(5, 84, 15, 44, 3)
            self.battle_cells_even = self.battle_cells_even.swapaxes(1, 2)

            self.battle_cells_odd = self.battle_cells_odd.swapaxes(1, 2)
            self.battle_cells = [[self.battle_cells_odd[0]], [self.battle_cells_even[0]], [self.battle_cells_odd[1]],
                                 [self.battle_cells_even[1]], [self.battle_cells_odd[2]], [self.battle_cells_even[2]],
                                 [self.battle_cells_odd[3]], [self.battle_cells_even[3]], [self.battle_cells_odd[4]],
                                 [self.battle_cells_even[4]], [self.battle_cells_odd[5]]]
            self.battle_cells_even = self.battle_cells_even.swapaxes(0, 1)
            self.battle_cells_odd = self.battle_cells_odd.swapaxes(0, 1)
            temp1 = []
            for y in range(11):
                z = self.battle_cells[y]
                z = z[0]
                for x in range(15):
                    img = z[x].copy()
                    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    #
                    # img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
                    #
                    # edges = cv2.Canny(image=img_blur, threshold1=50, threshold2=200)
                    #
                    # erosion = cv2.erode(edges, (0.7, 0.7), iterations=1)
                    #
                    # img = cv2.dilate(erosion, (0.7, 0.7), iterations=10)
                    # img = cv2.bitwise_and(z[x], z[x], mask=img)
                    img = cv2.resize(img, (9, 17))
                    temp1.append(img)
            self.battle_cells = np.array(temp1)

    def take_resources(self):
        """
        function taking image of resource bar
        """
        with mss() as sct:
            monitor = {'top': 1058, 'left': 7, 'width': 595, 'height': 15}
            self.resources = np.array(sct.grab(monitor))

    def take_adventure_map_units_window(self):
        """
        function taking image of unit portraits from adventure map
        """
        with mss() as sct:
            monitor = {'top': 536, 'left': 1769, 'width': 99, 'height': 33}
            screen = np.array(sct.grab(monitor))
            screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
            screen = screen.reshape(1, 33, 3, 33, 3)
            screen = screen.swapaxes(1, 2)
            monitor = {'top': 584, 'left': 1751, 'width': 132, 'height': 33}
            screen2 = np.array(sct.grab(monitor))
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_RGBA2RGB)
            screen2 = screen2.reshape(1, 33, 4, 33, 3)
            screen2 = screen2.swapaxes(1, 2)
            self.units_small = [screen[0, 0], screen[0, 1], screen[0, 2], screen2[0, 0], screen2[0, 1], screen2[0, 2],
                                screen2[0, 3]]

    def take_queue(self):
        """
        funtion creating list of unit portraits from queue (grayscale) and taking color and unit amount part of queue
        """
        with mss() as sct:
            self.queue = []
            self.queue_color = []
            monitor = {'top': 779, 'left': 662, 'width': 660, 'height': 38}
            screen = np.array(sct.grab(monitor))
            monitor2 = {'top': 817, 'left': 662, 'width': 660, 'height': 10}
            screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2GRAY)
            screen2 = np.array(sct.grab(monitor2))
            screen2 = cv2.cvtColor(screen2, cv2.COLOR_RGBA2RGB)
            for x in range(15):
                img = screen[:, 40 * x:40 * x + 36]
                # monitor = {'top': 779, 'left': 662 + x * 40, 'width': 36, 'height': 38}
                # screen = np.array(sct.grab(monitor))
                # monitor2 = {'top': 817, 'left': 662 + x * 40, 'width': 36, 'height': 10}
                # screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2GRAY)
                self.queue.append(img)
                # screen = np.array(sct.grab(monitor2))
                # screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
                img = screen2[:, 40 * x:40 * x + 36]
                self.queue_color.append(img)

    def take_one_from_queue(self, n):
        """
        funtion taking selected unit from queue

        :param n: number of unit in queue
        """
        with mss() as sct:
            self.queue = []
            move_to_portrait(n)
            time.sleep(0.08)
            monitor = {'top': 776, 'left': 660 + n * 40, 'width': 40, 'height': 56}
            screen = np.array(sct.grab(monitor))
            screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
            cv2.rectangle(screen, (3, 3), (37, 53), (0, 0, 0), -1)
            self.queue.append(screen)

    def take_firstFromQueue(self):
        """
        function taking image of first unit in queue (grayscale) and its amount and color part of graphic
        """
        with mss() as sct:
            self.queue = []
            self.queue_color = []
            monitor = {'top': 779, 'left': 662, 'width': 36, 'height': 38}
            screen = np.array(sct.grab(monitor))
            monitor2 = {'top': 817, 'left': 662, 'width': 36, 'height': 10}
            screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2GRAY)
            self.queue.append(screen)
            screen = np.array(sct.grab(monitor2))
            screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
            self.queue_color.append(screen)

    def take_unit_quantity(self):
        """
        function taking images of unit amounts from queue
        """
        with mss() as sct:
            self.quantity = []
            for x in range(15):
                monitor = {'top': 817, 'left': 662 + x * 40, 'width': 36, 'height': 15}
                screen = np.array(sct.grab(monitor))
                screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
                self.quantity.append(screen)


# class HeroMenu: # we dont use it in current version
#     def __init__(self):
#         self.units = []
#         self.head = []
#         self.cape = []
#         self.neck = []
#         self.right_hand = []
#         self.left_hand = []
#         self.ring = []
#         self.feet = []
#         self.torso = []
#         self.misc = []
#         self.backpack = []
#         self.lower_slots = []
#
#     def take_units(self):
#         with mss() as sct:
#             monitor = {'top': 730, 'left': 637, 'width': 462, 'height': 67}
#             img = np.array(sct.grab(monitor))
#             img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
#             img = img.reshape(67, 7, 66, 3)
#             self.units = img.swapaxes(0, 1)
#
#     def take_artifacts(self):
#         with mss() as sct:
#             monitor = {'top': 267, 'left': 940, 'width': 274, 'height': 382}
#             img = np.array(sct.grab(monitor))
#             img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
#             h = 45
#             w = 45
#             self.head = img[1:1 + h, 127:127 + w]
#             self.cape = img[213:213 + h, 186:186 + w]
#             self.neck = img[51:51 + h, 127:127 + w]
#             self.right_hand = img[40:40 + h, 1:1 + w]
#             self.left_hand = img[155:155 + h, 180:180 + w]
#             self.ring = [img[40:40 + h, 49:49 + w], img[155:155 + h, 228:228 + w]]
#             self.feet = img[266:266 + h, 133:133 + w]
#             self.torso = img[102:102 + h, 127:127 + w]
#             self.misc = [img[114:114 + h, 1:1 + w], img[164:164 + h, 17:17 + w], img[215:215 + h, 33:33 + w],
#                          img[266:266 + h, 49:49 + w], img[266:266 + h, 0:0 + w]]
#             y = 336
#             self.lower_slots = [img[y:y + h, 21:21 + w], img[y:y + h, 67:67 + w], img[y:y + h, 113:113 + w],
#                                 img[y:y + h, 159:159 + w], img[y:y + h, 205:205 + w]]
#
#     def take_backpack(self):
#         with mss() as sct:
#             monitor = {'top': 481, 'left': 888, 'width': 368, 'height': 368}
#             img = np.array(sct.grab(monitor))
#             img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
#             img = img.reshape(8, 46, 8, 46, 3)
#             img = img.swapaxes(1, 2)
#             self.backpack = list()
#             for i in range(8):
#                 for j in range(8):
#                     self.backpack.append(img[i, j])


# def read_city_building(x, y, building):
#     with mss() as sct:
#         monitor = {'top': y, 'left': x, 'width': 595, 'height': 15}
#         img = np.array(sct.grab(monitor))
#         color = img[0, 0]
#         # (find nearest color)
#         # (change information)


# def read_current_resources(image_source: ScreenStorage):
#     time.sleep(5)
#     image_source.take_resources()
#     img = cv2.cvtColor(image_source.resources, cv2.COLOR_RGBA2GRAY)
#     img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY_INV)
#     img = img[1].reshape(15, 7, 85)
#     img = img.swapaxes(0, 1)
#     res_list = []
#     with tesserocr.PyTessBaseAPI(oem=tesserocr.OEM.LSTM_ONLY) as api:
#         for x in range(7):
#             temp = img[x]
#             temp = cv2.resize(temp, (255, 45))
#             im_pil = Image.fromarray(temp)
#             # res_list.append(tesserocr.image_to_text(im_pil))
#             api.SetImage(im_pil)
#             res_list.append(api.GetUTF8Text())
#
#     return res_list

def readTemplates():
    """
    old function for reading templates from files

    :return: list of images
    """
    templates = []
    for filename in os.listdir(os.path.join("template/")):
        img = cv2.imread(os.path.join("template/", filename))
        templates.append(img)

    return templates


def readColors():
    """
    function reading player colors from battle

    :return: list of pixels with names to compare our future images to color
    """
    colors = []
    for filename in os.listdir(os.path.join("colors2/")):
        img = cv2.imread(os.path.join("colors2/", filename))
        img = np.median(img, (0, 1))
        colors.append((img, filename[:-4]))

    return colors


def readColors2():
    """
    function reading player colors from world view

    :return: list of pixels with names to compare our future images to color
    """
    colors = []
    for filename in os.listdir(os.path.join("colors_small_map/")):
        img = cv2.imread(os.path.join("colors_small_map/", filename))
        img = np.median(img, (0, 1))
        colors.append((img, filename[:-4]))

    return colors


# def slice_battle():
#     ss = ScreenStorage()
#     ss.take_battle_map_first()
#     cells = []
#     for i in range(15):
#         for j in range(5):
#             cells.append(ss.battle_cells_even[i, j])
#         for j in range(6):
#             cells.append(ss.battle_cells_odd[i, j])
#     for i, x in enumerate(cells):
#         cv2.imwrite("battle1_11_" + str(i) + '.jpg', x)


# def slice_map():
#     ss = ScreenStorage()
#     ss.take_adventure_map()
#     cells = []
#     for i in range(52):
#         for j in range(30):
#             cells.append(ss.cells[i, j])
#     for i, x in enumerate(cells):
#         cv2.imwrite("ts_structure_0_" + str(i) + '.jpg', x)


def slice_queue():
    """
    function saving images of unit queue in current folder
    """
    ss = ScreenStorage()
    ss.take_queue()
    cells = []
    for i in range(15):
        cells.append(ss.queue_color[i])
    for i, x in enumerate(cells):
        cv2.imwrite("ts_queue_color_2_" + str(i) + '.jpg', x)


# def slice_hero_units():
#     units = HeroMenu()
#     units.take_units()
#     cells = []
#     for i in range(7):
#         cells.append(units.units[i])
#     for i, x in enumerate(cells):
#         cv2.imwrite("ts_hero_0_" + str(i) + '.jpg', x)
#
#
# def slice_hero_artifacts():
#     units = HeroMenu()
#     units.take_artifacts()
#     cells = [units.head, units.cape, units.neck, units.right_hand, units.left_hand, units.ring[0], units.ring[1],
#              units.feet, units.torso, units.misc[0], units.misc[1], units.misc[2], units.misc[3], units.misc[4],
#              units.lower_slots[0], units.lower_slots[1], units.lower_slots[2], units.lower_slots[3],
#              units.lower_slots[4]]
#     for i, x in enumerate(cells):
#         cv2.imwrite("ts_hero_art_0_" + str(i) + '.jpg', x)


# def canny(image):
#     img = image.copy()
#     #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     #img_blur = cv2.GaussianBlur(img, (3, 3), 0)
#     edges = cv2.Canny(image=img, threshold1=100, threshold2=200)
#     # erosion = cv2.erode(edges, (0.7, 0.7), iterations=1)
#     # img = cv2.dilate(erosion, (0.7, 0.7), iterations=10)
#     img = cv2.bitwise_and(image, image, mask=edges)
#     return img

def temp_move(x: int, y: int):
    """
    function moving mouse to select tile in battle

    :param x: x coordinate of hex in battle
    :param y: y coordinate of hex in battle
    """
    if y % 2 == 1:
        beginning = (640, 330)
    else:
        beginning = (660, 330)
    expected_move = (beginning[0] + x * 44, beginning[1] + y * 42)
    move(expected_move[0], expected_move[1], duration=0)


def take_console():
    """
    function taking image of game console

    :return: image of console
    """
    with mss() as sct:
        monitor = {'top': 1035, 'left': 700, 'width': 400, 'height': 20}
        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
        return screen


def take_small_map():
    """
    function taking image of world view

    :return: list of tiles from world view corresponding to tiles in full map
    """
    with mss() as sct:
        monitor = {'top': 124, 'left': 468, 'width': 792, 'height': 792}
        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
        screen = screen.reshape(72, 11, 72, 11, 3)
        screen = screen.swapaxes(1, 2)
        screen2 = [[]]
        for x in range(72):
            screen2.append([])
            for y in range(72):
                screen2[x].append(np.median(screen[x, y], (0, 1)))
        # temp1 = []
        # for y in range(72):
        #     z = screen[y]
        #     for x in range(72):
        #         temp1.append(z[x])
        # cells = np.array(temp1)
        # return cells
        screen2 = np.array(screen2)
        return screen2


def save_small_map():
    """
    Saves world viev
    """
    list = take_small_map()
    for i in range(72):
        for j in range(72):
            cv2.imwrite("ts_small_map_" + str(i) + "_" + str(j) + '.jpg', list[i, j])


def take_resources_():
    """
    function taking image of resource bar
    """
    with mss() as sct:
        monitor = {'top': 1058, 'left': 7, 'width': 595, 'height': 15}
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        img = np.reshape(img, (15, 7, 85, 3))
        return img.swapaxes(0, 1)


def check_resources(player, res_range: tuple, generic: Cost = Cost(0, 0, 0, 0, 0, 0, 0), only_one=False, n=0):
    """
        Function that is responsible for updating player's resources..

        :param player: Player object
        :param res_range: Range of the given resource (size on screen)
        :param generic: objecgt of class cost containing value of minimal added resources for case when ocr cannot read our resources
        """
    resource = take_resources_()
    possible_resources = [0, 0, 0, 0, 0, 0, 0]
    if only_one:
        i = n
        res = resource[n]
        res = np.delete(res, np.s_[0:26], axis=1)
        banned_psm = []
        good_number = False
        tries = 0
        while not good_number and tries < 2:
            resources, psm = read_generic_numbers(res, 4, banned_psm, True)
            banned_psm.append(psm)
            try:
                if res_range[i][0] <= int(resources) <= res_range[i][1]:
                    good_number = True
                tries += 1
            except Exception:
                tries += 1
        if good_number:
            possible_resources[i] = int(resources)
        else:
            possible_resources[i] = 0
    else:
        for i, res in enumerate(resource):
            res = np.delete(res, np.s_[0:26], axis=1)
            banned_psm = []
            good_number = False
            tries = 0
            while not good_number and tries < 2:
                resources, psm = read_generic_numbers(res, 4, banned_psm, True)
                banned_psm.append(psm)
                try:
                    if res_range[i][0] <= int(resources) <= res_range[i][1]:
                        good_number = True
                    tries += 1
                except Exception:
                    tries += 1
            if good_number:
                possible_resources[i] = int(resources)
            else:
                possible_resources[i] = 0
    if possible_resources[6] != 0:
        player.gold = possible_resources[6]
    else:
        player.gold += generic.gold
    if possible_resources[0] != 0:
        player.wood = possible_resources[0]
    else:
        player.wood += generic.wood
    if possible_resources[1] != 0:
        player.mercury = possible_resources[1]
    else:
        player.mercury += generic.mercury
    if possible_resources[2] != 0:
        player.ore = possible_resources[2]
    else:
        player.ore += generic.ore
    if possible_resources[3] != 0:
        player.sulfur = possible_resources[3]
    else:
        player.sulfur += generic.sulfur
    if possible_resources[4] != 0:
        player.crystal = possible_resources[4]
    else:
        player.crystal += generic.crystal
    if possible_resources[5] != 0:
        player.gems = possible_resources[5]
    else:
        player.gems += generic.gems
