"""Script that contains functions used in battle image recognition"""
import image_processing.ocr
from image_processing.ocr import battle_unit_count, read_text, read_generic_text

import cv2
import numpy as np
from image_processing.screen_slicing import temp_move
from data.BattleAI_environment_needs import Obstacle, CreatureBox
from image_processing.CNN_learning import CNN, DumbNN
from image_processing.dictionaries import battle_dict
from image_processing.screen_slicing import ScreenStorage
from misc.timing import timing
import time
from mss import mss
from data.creature import Creature
from copy import deepcopy
import re
from mouse import move

def initialize_BNN():
    """
    function creating neural network object

    :return: neural network object
    """
    BNN = CNN((17, 9, 3), "image_processing/model/battle1/", 2)
    BNN.load_model()
    return BNN


def initialize_QNN():
    """
    function creating neural network object

    :return: neural network object
    """
    QNN = DumbNN((38, 36, 1), "image_processing/model/queue/", 166)
    QNN.load_model()
    return QNN
def initialize_UNN():
    """
    function creating neural network object

    :return: neural network object
    """
    QNN = DumbNN((53,59,1), "image_processing/model/unit/", 166)
    QNN.load_model()
    return QNN
def initialize_SNN():
    """
    function creating neural network object

    :return: neural network object
    """
    QNN = DumbNN((35, 47, 1), "image_processing/model/spells/", 79)
    QNN.load_model()
    return QNN
# def next_turn(queue: DumbNN, creatures: CNN, screen: ScreenStorage):
#     screen.take_battle_map()
#     screen.take_queue()
#     units = queue.model.predict(np.array(screen.queue), batch_size=15)
#     battle_map = creatures.model.predict(screen.battle_cells, batch_size=165)
#     # here translate allowing only values from units
#     units2 = []
#     for i in range(15):
#         units2.append(int((np.where(units[i] == np.amax(units[i])))[0]))
#     columns = list(range(0, 166))
#     columns = list(set(columns) - set(units2))
#     for i in columns:
#         battle_map[:, i] = 0
#     battle_map2 = []
#     for i in range(165):
#         battle_map2.append(int((np.where(battle_map[i] == np.amax(battle_map[i])))[0]))
#     return battle_map2


# def first_turn(queue: DumbNN, creatures: CNN, screen: ScreenStorage):
#     screen.take_battle_map_first()
#     screen.take_queue()
#     units = queue.model.predict(np.array(screen.queue), batch_size=15)
#     battle_map = creatures.model.predict(screen.battle_cells, batch_size=165)
#     # here translate allowing only values from units
#     units2 = []
#     for i in range(15):
#         units2.append(int((np.where(units[i] == np.amax(units[i])))[0]))
#     columns = list(range(0, 163))
#     columns = list(set(columns) - set(units2))
#     for i in columns:
#         battle_map[:, i] = 0
#     battle_map2 = []
#     for i in range(165):
#         battle_map2.append(int((np.where(battle_map[i] == np.amax(battle_map[i])))[0]))
#     return battle_map2


# def fill_battle_map(cells):
#     cells = np.array(cells)
#     cells = np.array([*map(battle_dict.get, cells)])
#     obstacles = []
#     units = []
#     cells = cells.reshape(11, 15)
#     for y in range(11):
#         for x in range(15):
#             if isinstance(cells[y, x], str):
#                 if cells[y, x] == "obstacle":
#                     obstacles.append(Obstacle((x, y)))
#             else:
#                 if cells[y, x].size == 1:
#                     units.append(CreatureBox(cells[y, x], (x, y), 0, True))
#                 elif x != 14 and cells[y, x + 1] == cells[y, x]:
#                     continue
#                 else:
#                     units.append(CreatureBox(cells[y, x], (x, y), 0, True))
#     pack = [units, obstacles]
#     return pack


# def fill_battle_map_first(cells):
#     cells = np.array(cells)
#     cells = np.array([*map(battle_dict.get, cells)])
#     obstacles = []
#     units = []
#     cells = cells.reshape(11, 15)
#     for y in range(11):
#         if y != 0:
#             for x in range(15):
#                 if isinstance(cells[y, x], str):
#                     if cells[y, x] == "obstacle":
#                         obstacles.append(Obstacle((x, y)))
#                 else:
#                     if cells[y, x].size == 1:
#                         units.append(CreatureBox(cells[y, x], (x, y), 0, True))
#                     elif x != 14 and cells[y, x + 1] == cells[y, x]:
#                         continue
#                     else:
#                         units.append(CreatureBox(cells[y, x], (x, y), 0, True))
#     pack = [units, obstacles]
#     return pack


# def first_turn_alliance(pack):
#     for x in pack[0]:
#         if x.field[0] > 2:
#             x.allied = False
#     return pack
#
#
# def next_turn_alliance_and_obstacles(pack_new, pack_old, creature_moved):
#     for x in pack_new[0]:
#         for y in pack_old[0]:
#             if x.creatureType == y.creatureType and x.hexField != y.hexField:
#                 if y.allied == True:
#                     if creature_moved == x:
#                         x.allied = True
#                         y.hexField = x.hexField
#                         x.quantity = y.quantity
#                         break
#                 elif y.allied == False:
#                     x.allied = False
#                     y.hexField = x.hexField
#                     x.quantity = y.quantity
#                     break
#     pack_old[0] = list(set(pack_old[0], pack_new[0]))
#     pack_old[1] = list(set(pack_old[1], pack_new[1]))
#     # for x in pack_new[1]:
#     #     t=True
#     #     for y in pack_old[1]:
#     #         if x.hexField == y.hexField:
#     #             t = False
#     #     if t:
#     #         y.append(x)
#     # pack = [pack_new[0],pack_old[1]]
#     return pack_old


# def first_battle_turn(queue: DumbNN, creatures: CNN, screen: ScreenStorage):
#     map = first_turn(queue, creatures, screen)
#     map2 = fill_battle_map_first(map)
#     out = first_turn_alliance(map2)
#     # here we need tesseract functions to apply unit counts
#     return out


# def next_battle_turn(queue: DumbNN, creatures: CNN, screen: ScreenStorage, pack_old, Creature_moved):
#     map = next_turn(queue, creatures, screen)
#     map2 = fill_battle_map(map)
#     out = next_turn_alliance_and_obstacles(map2, pack_old, Creature_moved)
#     # here we need tesseract functions to apply unit counts
#     return out


def distance(point, points):
    """
    :param point: point for which we are detecting nearest element
    :param points: list of points with names
    :return: name of nearest field from point to given point
    """
    dst = []
    for x in points:
        y = x[0]
        dst.append(((point[0] - y[0]) ** 2) + ((point[1] - y[1]) ** 2) + ((point[2] - y[2]) ** 2))
    dst = np.array(dst)
    dst = np.sqrt(dst)
    result = np.where(dst == np.amin(dst))
    return points[int(result[0])][1]


def distance2(point, points):
    """
    :param point: point for which we are detecting nearest element, different input data than distance function
    :param points: list of points with names
    :return: name of nearest field from point to given point
    """
    dst = []
    for y in points:
        dst.append(((point[0] - y[0]) ** 2) + ((point[1] - y[1]) ** 2) + ((point[2] - y[2]) ** 2))
    dst = np.array(dst)
    dst = np.sqrt(dst)
    result = np.where(dst == np.amin(dst))
    return result[0]


def checkIfTurnIsOurs(screen):
    """
    function checking if currently is our turn

    :param screen: screenslicing object
    :return: value telling if the turn is ours or not
    """
    screen.take_firstFromQueue()
    color = distance(np.median(screen.queue_color[0], (0, 1)), screen.stripsInQueueColorImages)
    if color == screen.our_color:
        return True
    return False


# def matching(template_list,smallpoints,screen):
#     positions = []
#     screen.take_battle_templates()
#     for template in template_list:
#         img = screen.screen.copy()
#         method = eval("cv2.TM_CCOEFF_NORMED")
#         res = cv2.matchTemplate(img, template, method)
#         for i in range(15):  # taking only points that are connected to hexes on map
#             smallpoints[0, i] = np.amax(res[0:6, 14 + i * 44: 30 + i * 44])
#             smallpoints[1, i] = np.amax(res[35:47, 0 + i * 44:3 + i * 44])
#             smallpoints[2, i] = np.amax(res[78:90, 14 + i * 44: 30 + i * 44])
#             smallpoints[3, i] = np.amax(res[119:131, 0 + i * 44:3 + i * 44])
#             smallpoints[4, i] = np.amax(res[162:174, 14 + i * 44: 30 + i * 44])
#             smallpoints[5, i] = np.amax(res[203:215, 0 + i * 44:3 + i * 44])
#             smallpoints[6, i] = np.amax(res[246:258, 14 + i * 44: 30 + i * 44])
#             smallpoints[7, i] = np.amax(res[287:299, 0 + i * 44:3 + i * 44])
#             smallpoints[8, i] = np.amax(res[330:342, 14 + i * 44: 30 + i * 44])
#             smallpoints[9, i] = np.amax(res[371:383, 0 + i * 44:3 + i * 44])
#             smallpoints[10, i] = np.amax(res[414:420, 14 + i * 44: 30 + i * 44])
#
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(smallpoints)
#
#         if max_val > 0.3:  # it should take only real positions and ignore all later units, value needs change and some work on templates to better differentiate real units from terrain
#             top_left = max_loc
#             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#             top = max_loc
#             bottom_right = (top[0] + 45, top[1] + 85)
#             cv2.rectangle(screen.screen, top, bottom_right, (100, 100, 100),
#                           -1)  # change to image to eliminate unit which is detected by this match
#             positions.append(top_left)
#             i = i + 1
#         else:
#             i = i + 1
#             positions.append((-1,-1))
#     return positions


# @timing
# def template_battle(qnn: DumbNN,
#                     screen: ScreenStorage):  # needs some change for later turns, simple check for minimal value of match instead taking only units before next turn
#     colors = screen.stripsInQueueColorImages
#     smallpoints = np.ones((11, 15))
#     screen.take_queue()
#
#     screen.take_unit_quantity()
#     units = qnn.model.predict(np.array(screen.queue), batch_size=15)
#     units2 = []
#     color = []
#     for i in range(15):
#         units2.append(int((np.where(units[i] == np.amax(units[i])))[0]))
#         color.append(distance(np.median(screen.queue_color[i], (0, 1)), colors))  # checking player controling unit
#     x = 0
#     templates = screen.templates
#     template_list = []
#     ally = []
#     i = 0
#     units = []
#     quantity = []
#     for x in units2:  # preparing list of templates to use
#         if x >= 164:
#             pass
#         else:
#             units.append(x)
#             if color[i] == "red":
#                 template_list.append(templates[x])
#                 quantity.append(battle_unit_count(screen.quantity[i],red_unit=True))
#                 ally.append(1)
#             else:
#                 template_list.append(cv2.flip(templates[x].copy(), 1))
#                 quantity.append(battle_unit_count(screen.quantity[i]))
#                 ally.append(0)
#         i = i + 1
#     i = 0
#
#     pos = []
#     # 2 checks for eliminating errors from animating units
#     first = matching(template_list,smallpoints,screen)
#     time.sleep(0.5)
#     second = matching(template_list, smallpoints,screen)
#     for i in range(len(first)):
#         if first[i][0]==-1:
#             pos.append(second[i])
#         else:
#             pos.append(first[i])
#     out = []
#     units = np.array([*map(battle_dict.get, units)])
#     for i in range(len(pos)):
#
#         if ally[i] == 1:
#             temp = True
#         else:
#             temp = False
#         out.append(CreatureBox(units[i], pos[i], quantity[i], temp))  # combining all parts of detection to form output, need adding tesseract function to chceck quantity (tesseract installation needed)
#     return out

def check_terrain(bnn: CNN, screen: ScreenStorage, units):
    """
    function for detecting obstacles at beginning of battle

    :param bnn: neural network object
    :param screen: screen slicing object
    :param units: list of units on map
    :return: list of potential obstacles on map
    """
    screen.take_battle_map_first()
    out = []
    land = bnn.model.predict(np.array(screen.battle_cells),
                             batch_size=165)  # should be good enough, in testing only problems were detecting obstalcle when part of unit is on image
    land = land.reshape(11, 15, 2)[:, 2:-2, 0]

    unitTiles = []
    for unit in units:
        unitTiles.append(unit.field)
        if unit.type.size == 2 and unit.ally:
            unitTiles.append(tuple(np.array(unit.field) + np.array((-1, 0))))
        elif unit.type.size == 2 and not unit.ally:
            unitTiles.append(tuple(np.array(unit.field) + np.array((1, 0))))

    for y in range(11):
        for x in range(11):
            if land[y, x] > 0.8:
                if (x + 2, y) not in unitTiles:
                    out.append(Obstacle((x + 2, y)))
    return out


def find_first_unit(screen: ScreenStorage):
    """
    function finding where is current first unit to find how many units are currently in battle

    :param screen: screenslicnig object
    :return: amount of queue tiles that we need to check
    """
    queue = []
    screen.take_one_from_queue(0)
    b = np.sum(screen.queue[0], (0, 1))
    out = 15
    for x in range(1, 15):
        screen.take_one_from_queue(x)
        a = np.sum(screen.queue[0] / 255, (0, 1))
        a = a
        queue.append(a)
    out = distance2(b, queue)
    out = out[0]
    return out + 1


def find_unit(x, y, base, screen, n):
    """
    function checking if there is unit on coordinates xy

    :param x: x index of tile in battle
    :param y: y index of tile in battle
    :param base: clear image of queue
    :param screen: screen slicing object
    :param n: number of units in queue
    :return: number of unit in queue we are currently pointing
    """
    screen.take_queue_to_find_unit(x, y)
    new_q = screen.queue
    test = []
    for i in range(n):
        img1 = cv2.cvtColor(new_q[i], cv2.COLOR_BGR2GRAY).copy()
        img2 = cv2.cvtColor(base[i], cv2.COLOR_BGR2GRAY).copy()
        img3 = cv2.absdiff(img1, img2)
        img3 = cv2.threshold(img3, 0, 5, cv2.THRESH_BINARY)
        test.append(cv2.bitwise_and(new_q[i], new_q[i], mask=img3[1]))
        test[i] = np.sum(test[i])
    result = np.where(test == np.amax(test))
    result = result[0]
    result = result[0]
    if test[result] < 100:
        unit = False
    else:
        unit = True
    return result, unit


@timing
def mouse_unit_check(qnn: DumbNN, screen: ScreenStorage, skills: list):
    """
    function checking units in battle

    :param qnn: neural network for checking units in battle
    :param screen: screen slicing object
    :param skills: list of SecondarySkills
    :return: list of creatureboxes
    """
    colors = screen.stripsInQueueColorImages
    screen.take_queue()
    screen.take_unit_quantity()
    units = qnn.model.predict(np.array(screen.queue), batch_size=15)
    units2 = []
    color = []
    boxes = []
    numbers = []
    numbers_max = []
    for y in range(11):
        numbers.append([])
        numbers_max.append(([]))
        for x in range(15):
            numbers[y].append(1)
            numbers_max[y].append(1)
    quantity = []
    allied = []
    first = find_first_unit(screen)
    for i in range(first):
        units2.append(int((np.where(units[i] == np.amax(units[i])))[0]))
        boxes.append([])
    units = np.array([*map(battle_dict.get, units2)])
    war_machines = {10: {"Creature": battle_dict[167],
                         "position_ally": (0, 3),
                         "position_enemy": (14, 3)},
                    51: {"Creature": battle_dict[169],
                         "position_ally": (0, 9),
                         "position_enemy": (14, 9)},
                    }
    if "Ballistics" in skills:
        war_machines[19] = {"Creature": battle_dict[168],
                            "position_ally": (0, 7),
                            "position_enemy": (14, 7)}
    # units = np.array([unit if units2[i] not in war_machines.keys() else war_machines[units2[i]] for i, unit in enumerate(units)])
    war_machines_in_battle = [(war_machines[units2[i]], i) for i, unit in enumerate(units) if
                              units2[i] in war_machines.keys()]
    for i in range(first):
        color.append(distance(np.median(screen.queue_color[i], (0, 1)), colors))
        if color[i] == screen.our_color:
            quantity.append(battle_unit_count(screen.quantity[i], red_unit=True))
        else:
            quantity.append(battle_unit_count(screen.quantity[i]))
        if color[i] == screen.our_color:
            allied.append(1)
        else:
            allied.append(0)

        screen.take_battle_map(i)
        bmap = screen.battle_cells
        for y in range(11):
            for x in range(15):
                numbers[y][x] = bmap[y * 15 + x]
                numbers_max[y][x] = cv2.addWeighted(numbers[y][x], 0.5, numbers_max[y][x], 0.5, 0.0)
    for y in range(11):
        for x in range(15):
            numbers_max[y][x] = np.sum(numbers_max[y][x])
            if numbers_max[y][x] < 100:
                numbers_max[y][x] = 0
    possible_units = np.nonzero(numbers_max)
    screen.take_queue_to_find_unit_raw()
    base_queue = screen.queue
    for i in range(len(possible_units[0])):
        number, check = find_unit(possible_units[1][i], possible_units[0][i], base_queue, screen, first)
        if check:
            if isinstance(units[number], Creature):
                boxes[number].append(CreatureBox(units[number], (possible_units[1][i], possible_units[0][i]),
                                                 int(float(quantity[number])), bool(allied[number])))
    for x in range(len(boxes)):
        if len(boxes[x]) == 2:
            if boxes[x][0].ally == True:
                boxes[x] = boxes[x][1]
            else:
                boxes[x] = boxes[x][0]
        else:
            try:
                boxes[x] = boxes[x][0]
            except:
                x = x
            # result = np.where(numbers == np.amax(numbers))
            # result = (result[0][0], result[1][0])
            #
            # try:
            #     boxes.append(CreatureBox(units[i], result, int(quantity[i]), bool(allied[i])))
            # except:
            #     pass

    for machine in war_machines_in_battle:
        boxes[machine[1]] = CreatureBox(machine[0]["Creature"], machine[0]["position_ally"] if allied[machine[1]] else machine[0]["position_enemy"], 1,
                                        bool(allied[machine[1]]))
    return boxes


def checkForObstacle(target: tuple):
    """
    function chcecking if on select tile we really have obstacle

    :param target: tile coordinates to check
    :return: information if on tile is obstacle
    """
    x, y = target
    temp_move(x, y)
    time.sleep(0.1)
    with mss() as sct:
        monitor = {'top': 835, 'left': 850, 'width': 250, 'height': 20}
        screen = np.array(sct.grab(monitor))
        txt = read_text(screen)
        txt.strip()
        if len(txt) < 3:
            return True
        else:
            return False

# bnn = initialize_BNN()
# out1 = template_battle(qnn,screen)
# out2 = check_terrain(bnn,screen)
# print(1)
# def find_possible(screen: ScreenStorage,terrain):
#     possible = screen.take_possible_units(terrain)
#     return possible
def near_enough(img1,img2):
    img1 = (cv2.resize(img1,(1,1))[0][0]).astype(int)
    img2 = (cv2.resize(img2, (1, 1))[0][0]).astype(int)
    dst = ((img1[0] - img2[0]) ** 2) + ((img1[1] - img2[1]) ** 2) + ((img1[2] - img2[2]) ** 2)
    if dst < 20:
        return True
    else:
        return False


def determine_unit(img,qnn,snn):
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGBA2GRAY)
    img = cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
    unit = img_gray[5:58,8:67] # 63,59
    #unit = cv2.resize(unit,(63, 38))
    count = img[55:68,30:67]
    attack = img[75:86,25:70]
    defence = img[86:100,25:70]
    dmg = img[100:110,30:70]
    spell1 = img_gray[168:203,14:61]#47,35
    spell2 = img_gray[206:241,14:61]
    spell3 = img_gray[244:279,14:61]
    cv2.imwrite("./spells_test/1_spelltest.png",spell1)
    cv2.imwrite("./spells_test/2_spelltest.png", spell2)
    cv2.imwrite("./spells_test/3_spelltest.png", spell3)
    count = read_generic_text(count)
    try:
        count = int(re.sub('[^0-9]+', '', count))
    except:
        count = 10
    # attack = read_generic_text(attack)
    # attack = attack.partition("(")[1]
    # attack = attack.partition(")")[0]
    # attack = int(attack)
    # defence = read_generic_text(defence)
    # defence = defence.partition("(")[1]
    # defence = defence.partition(")")[0]
    # defence = int(defence)
    # dmg = read_generic_text(dmg)
    # dmg = dmg.partition("-")
    # dmg = (dmg[0],dmg[1])
    creature = qnn.model.predict(np.array([unit]), batch_size=1)[0]
    creature = (np.where(creature == np.amax(creature)))[0]
    creature = [*map(battle_dict.get, creature)]
    spells = [spell1,spell2,spell3]
    spells = snn.model.predict(np.array(spells),batch_size = 3)
    spells2 = []
    for i in range(3):
        spells2.append(int((np.where(spells[i] == np.amax(spells[i])))[0]))
    #spells = np.array([*map(spelldict.get, spells2)])
    spells = spells2
    buffed_creature = deepcopy(creature)
    # buffed_creature.attack = attack
    # buffed_creature.defense = defence
    # buffed_creature.damage = dmg
    return buffed_creature[0],spells,count


def queue_partial_detection(qnn: DumbNN,screen: ScreenStorage):
    colors = screen.stripsInQueueColorImages
    screen.take_queue()
    units = qnn.model.predict(np.array(screen.queue), batch_size=15)
    units2 = []
    color = []
    allied = []
    for i in range(15):
        units2.append(int((np.where(units[i] == np.amax(units[i])))[0]))
    units = list([*map(battle_dict.get, units2)])
    for i in range(15):
        color.append(distance(np.median(screen.queue_color[i], (0, 1)), colors))
        if color[i] == screen.our_color:
            allied.append(1)
        else:
            allied.append(0)
    return units,allied


def new_unit_detection_system(qnn: DumbNN, unn: DumbNN, snn: DumbNN, screen: ScreenStorage, skills=None):
    if skills is None:
        skills = []
    screen.take_possible_units()
    move(0, 0)
    time.sleep(0.03)
    with mss() as sct:
        monitor = {'top': 492, 'left': 478, 'width': 75, 'height': 285}
        ally_clr = np.array(sct.grab(monitor))
        monitor = {'top': 492, 'left': 1366, 'width': 75, 'height': 285}
        enemy_clr = np.array(sct.grab(monitor))
    units = []
    for y in range(11):
        for x in range(15):
            if screen.possible_units[x+15*y]:
                temp_move(x, y)
                time.sleep(0.04)
                with mss() as sct:
                    monitor = {'top': 492, 'left': 478, 'width': 75, 'height': 285}
                    ally = np.array(sct.grab(monitor))
                    if not near_enough(ally,ally_clr):
                        side = True
                        unit,spells,amount = determine_unit(ally,unn,snn)
                        if unit != 'ammo_cart':
                            units.append(CreatureBox(unit,(x,y),amount,side,spells))
                    else:
                        monitor = {'top': 492, 'left': 1366, 'width': 75, 'height': 285}
                        enemy = np.array(sct.grab(monitor))
                        if not near_enough(enemy, enemy_clr):
                            side = False
                            unit,spells,amount = determine_unit(enemy,unn,snn)
                            if unit != 'ammo_cart':
                                units.append(CreatureBox(unit, (x, y), amount, side,spells))
    # probably 2 hex units
    to_remove = []
    for i,box in enumerate(units):
        unit = box.type
        x1 = box.field[0]
        y1 = box.field[1]
        for box2 in units:
            unit2 = box2.type
            x2 = box2.field[0]
            y2 = box2.field[1]
            if unit == unit2:
                if not box.ally and box.ally == box2.ally:
                    if y1==y2 and x1 == (x2 + 1):
                        to_remove.append(i)
                        break
                elif box.ally == box2.ally:
                    if y1==y2 and x1 == (x2 - 1):
                        to_remove.append(i)
                        break
    for x in reversed(to_remove):
        units.pop(x)
    move(0, 0)
    time.sleep(0.03)
    queue,allied = queue_partial_detection(qnn,screen)

    temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # if "Artillery" in skills:
    #     units.append(CreatureBox(battle_dict[167], (0, 3), amount, True,[]))
    # units.append(CreatureBox(battle_dict[167], (14, 3), amount, False, []))
    # if "First_Aid" in skills:
    #     units.append(CreatureBox(battle_dict[169], (0, 9), amount, True, []))
    # units.append(CreatureBox(battle_dict[169], (14, 9), amount, False, []))
    # if "Ballistics" in skills:
    #     units.append(CreatureBox(battle_dict[168], (0, 7), amount, True, []))
    # units.append(CreatureBox(battle_dict[167], (14, 7), amount, False, []))
    for x in units:
        for i in range(len(queue)):
            if x.type == queue[i] and x.ally == allied[i]:
                temp[i] = x
                queue[i]=Creature("", 1, 10, 10, (2, 3), 250, 1, 126, 1, 24, True, False, "Neutral", ("None",), [])
                break
        else:
            temp.append(x)
    result = []
    for x in temp:
        if isinstance(x,int):
            pass
        else:
            result.append(x)
    screen.last_turn_units = []

    for x in result:
        screen.last_turn_units.append(x.field)
    print(result)
    return result

