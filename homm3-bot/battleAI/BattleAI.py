import cv2
from mss import mss
from battleAI.reinforcmentLearningTest import Environment, divideIntoAllyAndEnemy
from data.BattleAI_environment_needs import *
from image_processing.battle_image_processing import mouse_unit_check, check_terrain, initialize_BNN, initialize_QNN, \
    ScreenStorage, checkIfTurnIsOurs, checkForObstacle, new_unit_detection_system, initialize_SNN, initialize_UNN
from battleAI.deepQlearning import DQNAgent, policy
from GUI_handling.BattleGUI import *
import numpy as np
import random as rd
import time
import mouse
import keyboard as kb
import os
import copy
from data.hero_specialities import specialities
from data.casting_spells import Use_magic
import win32gui
import win32ui

if __name__ == "__main__":
    os.chdir('../')


# This class is helpful in connecting creatures detected by neural network with creatures in queue
class CreatureMove:
    def __init__(self, detectedMob: CreatureBox):

        self.detectedInstance = detectedMob
        self.fromQueueInstance = None
        self.candidates = []  # list with queue indexes of candidates

    def findCandidates(self, queue):
        for i, mob in enumerate(reversed(queue)):
            if mob.ally:
                break
            if mob.type.name == self.detectedInstance.type.name:
                self.candidates.append(len(queue) - i - 1)


def fitted(mobs: list):
    for mob in mobs:
        if len(mob.candidates) != 1:
            return False
    return True


def take_whole_queue():
    """
    Takes screenshot of the entire queue

    :return: np.array - screenshot of the entire queue
    """
    monitor = {'top': 779, 'left': 662, 'width': 15 * 40, 'height': 38}
    screen = np.array(mss().grab(monitor))
    return screen


def bookAvailable():
    """
    Checks if we can use the spell or not

    :return: bool - True if available, False otherwise
    """
    book_available = 85  # mean value of spell book icon when it's possible to use it
    book_used = 57  # mean value of spell book icon when it's not possible to use it

    monitor = {'top': 780, 'left': 1311, 'width': 46, 'height': 37}
    screen = np.array(mss().grab(monitor))
    screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
    mean = np.mean(screen)

    if abs(mean - book_available) < abs(mean - book_used):
        #TODO WROCIC NA TRUE
        return False
    else:
        return False


def arePicturesTheSame(pictureA, pictureB):
    """
    Checks if pictures are exactly the same

    :param pictureA: np.array - image
    :param pictureB: np.array - image
    :return: bool - are pictures the same
    """
    return not (np.bitwise_xor(pictureA, pictureB).any())


def arePicturesSimilar(pictureA, pictureB, percent):
    """
    Checks if pictures are similar

    :param pictureA: np.array - image
    :param pictureB: np.array - image
    :param percent: float - acceptable percent of difference between pictures
    :return: bool - are pictures similiar
    """
    truthTable = pictureA == pictureB
    truthTable = truthTable.reshape(-1)

    difference = len(truthTable[truthTable == False]) / len(truthTable)
    if difference < percent / 100:
        return True
    else:
        return False


def take_side_window():
    """
    Takes screenshot of the side window that pops up when we hover over enemy

    :return: np.array - screenshot of the side window
    """
    monitor = {'top': 492, 'left': 1366, 'width': 1441 - 1366, 'height': 777 - 492}
    screen = np.array(mss().grab(monitor))
    img = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
    return img


# Checks if the battle has ended by detecting if "ok" button has appeared
def checkIfEnd(ok_button_img):
    """
    Checks if the battle has ended

    :param ok_button_img: np.array - image of ok button to look for
    :return: boot - has the battle ended
    """
    monitor = {'top': 765, 'left': 1109, 'width': 1176 - 1109, 'height': 798 - 765}
    img = np.array(mss().grab(monitor))
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    if arePicturesTheSame(ok_button_img, img):
        return True
    else:
        return False


def colorDistance(checked, reference):
    """
    Calculates the distance in color space between two colors

    :param checked: 3 element list - checked color
    :param reference: 3 element list - reference color
    :return: distance in color space between two colors
    """
    return np.sqrt(
        (checked[0] - reference[0]) ** 2 + (checked[1] - reference[1]) ** 2 + (checked[2] - reference[2]) ** 2)


def checkTerrainType():
    """
    Checks whether the terrain we are fighting on is Grass or Dirt

    :return: str - terrain we are fighting on
    """
    dirt_terrain_color = [66, 90, 115]
    grass_terrain_color = [24, 90, 82]
    y = 730
    x = 560
    w = 50
    h = 45
    monitor = {'top': y, 'left': x, 'width': w, 'height': h}
    terrain_snippet = np.array(mss().grab(monitor))
    mean_color_value = np.median(terrain_snippet, (0, 1))
    distance1 = colorDistance(mean_color_value, dirt_terrain_color)
    distance2 = colorDistance(mean_color_value, grass_terrain_color)
    if distance1 < distance2:
        return "Dirt"
    else:
        return "Grass"


class BattleAI:

    def __init__(self,color = "Red"):
        # 1. Loading battle agent model which will be making decisions
        print(os.getcwd())
        self.agent = DQNAgent("DQNAgent", buffer_size=100, start_epsilon=0, min_epsilon=0, training=False)  # load model
        self.agent.mod.load_weights(f"{os.path.dirname(__file__)}/battleModelplayer_weights.h5")

        # 2. Initialize BattleNeuralNetwork and QueueNeuralNetwork which are processing image data from game and
        # extrude information about game state from it
        self.bnn = initialize_BNN()
        self.qnn = initialize_QNN()
        self.snn = initialize_SNN()
        self.unn = initialize_UNN()
        self.screen = ScreenStorage(color)
        self.terrain = None
        self.hero_name = None
        self.hero_skills = None
        self.spell_power = None

        self.fortification = None
        self.siege = False

        self.siege_walls = None
        self.moat = None
        self.destructible_walls = None
        self.not_masked_possible_moves = None

        # array containing hexagram image needed in detecting obstacles
        self.hex_img = np.load(r'./battleAI/hex.npy')

        self.__cursor_dict = {
            1.67: 0,  # ally
            1.84: 1,  # possible move walking
            2.59: 1,  # possible move flying
            3.04: 0,  # not possible move
            2.44: 1   # heal
        }

        # 3. Initialize environment
        self.env = None

    @staticmethod
    def __get_cursor():
        """
        Collects cursor icon

        return (np.array) 3D - cursor icon
        """
        hcursor = win32gui.GetCursorInfo()[1]
        hwnd = win32gui.GetForegroundWindow()
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(hwnd))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((10, 10), hcursor)

        bmpstr = hbmp.GetBitmapBits(True)
        cursor = np.frombuffer(bmpstr, dtype='uint8').reshape(32, 32, -1)

        win32gui.DeleteObject(hbmp.GetHandle())
        hdc.DeleteDC()

        return cursor

    def debunk_obstacles(self):
        """
        Removes false positives from detected obstacles
        """
        for y in range(self.env.state.shape[1]):
            for x in range(self.env.state.shape[0]):
                if isinstance(self.env.state[x, y], Obstacle) and self.not_masked_possible_moves[x, y] == 1:
                    self.env.state[x, y] = 0
                    self.env.obstacles = [obstacle for obstacle in self.env.obstacles if obstacle.field != (x, y)]
                    print(f'Removed obstacle from {(x, y)}')

    def check_if_still_alive(self, target):
        """
        Checks if unit we attacked is still alive
        """
        move_mouse_to_tile(target[0], target[1], True)
        time.sleep(0.0001)
        cursor = self.__get_cursor()
        cursor_value = np.round(np.mean(cursor), 2)
        alive = cursor_value not in self.__cursor_dict.keys()   # attack icon

        return alive

    def get_possible_moves(self, update=True):
        """
        Get accurate possible moves based on cursor icon

        :param update: bool - update possible moves of the environment

        :return (np.array) 2D - non-zero elements are the tiles the unit can move on
        """
        possible_moves = np.zeros((15, 11))
        heal_target = False

        move_mouse_to_tile(0, 0, True)
        time.sleep(0.01)
        for p_y in range(11):
            for p_x in reversed(range(15)) if p_y % 2 != 0 else range(15):
                move_mouse_to_tile(p_x, p_y, True)
                time.sleep(0.02)
                cursor = self.__get_cursor()
                cursor_value = np.round(np.mean(cursor), 2)
                if cursor_value == 2.44:
                    heal_target = True
                possible_moves[p_x, p_y] = self.__cursor_dict[cursor_value] \
                    if cursor_value in self.__cursor_dict.keys() else 2  # attack

        if self.env.queue.queue[-1].type.name == "FirstAid" and not heal_target:
            # if there are no heal targets the first aid tent skips a turn
            self.env.queue.move()
        # current unit position
        if self.env.queue.queue[-1].type.name not in ["Catapult", "FirstAid", "Ballista"]:
            possible_moves[self.env.queue.queue[-1].field] = 1

        # all possible moves
        self.not_masked_possible_moves = np.where(possible_moves == 2, 1, possible_moves)

        # force to attack
        if 2 in possible_moves:
            possible_moves = np.where(possible_moves == 2, 1, 0)

        if update:
            self.env.possibleMoves = possible_moves

        return possible_moves

    def findObstacles(self, units):
        obstaclesList = check_terrain(self.bnn, self.screen, units)
        return obstaclesList

    def findUnits(self):
        # unitsList = mouse_unit_check(self.qnn, self.screen, self.hero_skills)
        unitsList = new_unit_detection_system(self.qnn, self.unn, self.snn, self.screen, self.hero_skills)
        uList = copy.deepcopy(unitsList)
        uList = [unit for unit in uList if not isinstance(unit, list)]

        return uList

    def start(self, setOfCreatures: list, setOfObstacles: list):
        self.env = Environment(setOfCreatures, setOfObstacles, self.agent.training)

    def simulateMoves(self, enemyCreatures: list):
        mobsInOrder = self.__fitDetectedCreaturesToQueueCreatures(enemyCreatures)
        for mob in mobsInOrder:
            self.env.moveCreature(mob.detectedInstance.field)

    def __fitDetectedCreaturesToQueueCreatures(self, enemyCreatures: list):
        # Algorithm
        # 1. Because we have information only about position we need to find all the creatures with the same name and
        # ally from queue. These creatures are candidates for moving
        # 2. We are searching for candidates for every enemy which was moved by opponent
        # 3. Then we are eliminating most distant candidates (further than speed of the creature)
        # 4. Then we look at moving possibilities and we are connecting everything in consistent whole
        # resources        -> mobs we need move to simulate opponent turn in proper order
        # moves            -> target positions we need mobs from resources to move on
        # listOfCandidates -> we need to find connection enemy->resource so listOfCandidates contains candidates for
        #                     these connections

        # 1. Initialise necessary structures and find candidates
        mobs = []
        for enemy in enemyCreatures:
            mob = CreatureMove(enemy)
            mob.findCandidates(self.env.queue.queue)
            mobs.append(mob)

        # 2. FIRST REDUCING PROCESS: Reducing candidates by calculating possible moves and checking if candidate
        # could reach target position
        for mob in mobs:
            if len(mob.candidates) != 1:
                # Iterate through candidates to find who could reach position of detected creature
                candidates = mob.candidates.copy()
                for candidate in candidates:
                    # possibleMoves = self.env.choosePossibleMoves(self.env.queue.queue[candidate])  # Get possible moves
                    possibleMoves = self.get_possible_moves(self.env.queue.queue[candidate])
                    if not possibleMoves[mob.detectedInstance.field]:
                        mob.candidates.remove(candidate)
        if fitted(mobs):
            mobs.sort(key=lambda x: x.candidates[0], reverse=True)
            return mobs

        # 3. SECOND REDUCE PROCESS Connecting detected creatures who has only one candidate with this candidate and
        # reduce these candidates from other candidates lists
        for mob in mobs:
            if len(mob.candidates) == 1:
                for i in range(len(mobs)):
                    if mob.candidates == mobs[i].candidates:
                        continue
                    elif mob.candidates[0] in mobs[i].candidates:
                        mobs[i].candidates.remove(mob.candidates[0])
        if fitted(mobs):
            mobs.sort(key=lambda x: x.candidates[0], reverse=True)
            return mobs

        # 4. THIRD REDUCE PROCESS We need to resolve some conflicts so firstly we check how many times candidate
        # appear in the candidates list: if candidate appear only once we have to use it in place we found it
        # When counting we can miss lists with length == 1

        # 4.1 Fill counter: two dimensional because we want to remember where we can find this candidate
        counter = np.zeros((len(self.env.queue.queue), 2), dtype=int)
        for i, mob in enumerate(mobs):
            if len(mob.candidates) != 1:
                for candidateIdx in mob.candidates:
                    if counter[candidateIdx][0] == 0:
                        for unit in mobs:
                            if candidateIdx in unit.candidates:
                                counter[candidateIdx][0] += 1
                                counter[candidateIdx][1] = i

        # 4.2 Reduction phase
        for i, pair in enumerate(counter):
            if pair[0] == 1:
                mobs[pair[1]].candidates = [i]

        if fitted(mobs):
            mobs.sort(key=lambda x: x.candidates[0], reverse=True)
            return mobs

        # 5. FOURTH REDUCE PROCESS: last process is resolve conflicts with quantity of the stacks
        # less quantity difference between stacks means that this is real one
        # We will use counter from the previous reduce process. If under index counter is -1 we cant take this candidate
        for mob in mobs:
            if len(mob.candidates) != 1:
                # Calculate differences
                quantityDiffs = np.zeros_like(mob.candidates)
                for i, candidate in enumerate(mob.candidates):
                    quantityDiffs[i] = abs(mob.detectedInstance.quantity - self.env.queue.queue[candidate].quantity)

                # Choose best candidate with minimum quantity difference
                minArg = np.argmin(quantityDiffs)
                bestCandidateIdx = mob.candidates[minArg]

                # If it is accessible take it, if not take something other
                while len(mob.candidates) != 1:
                    if counter[bestCandidateIdx][0] != -1:
                        # If true take it
                        mob.candidates = [bestCandidateIdx]
                        counter[bestCandidateIdx][0] = -1
                    else:
                        # If false remove this from candidate and find for new minimum quantity difference
                        mob.candidates.remove(bestCandidateIdx)
                        quantityDiffs = np.delete(quantityDiffs, minArg)
                        minArg = np.argmin(quantityDiffs)
                        bestCandidateIdx = mob.candidates[minArg]

            else:
                counter[mob.candidates[0]][0] = -1

        mobs.sort(key=lambda x: x.candidates[0], reverse=True)
        return mobs

    def makeMove(self, target: tuple):

        # 1. Make sure last mob from queue is ours
        # if mob.ally:
        # Move creature in environment
        neighbour = None
        if target is not None:
            target, neighbour = self.env.moveCreature(target, False)
        else:
            self.env.queue.move()

        # Move creature in game
        if neighbour is None:
            if target is not None:
                move_to_tile(target[0], target[1])
        else:
            attack_enemy(target[0], target[1], neighbour)

    def getAction(self, state):
        """
        Gets action from our agent

        :param state: 3D array - represents current state of our environment
        :return: tuple - chosen tile, current unit, actions probabilities calculated by our agent
        """
        mob = self.env.queue.queue[-1]

        (x, y), actIDX, possibleIdxs, actionsProbability, _ = policy(state, self.agent, self.env.possibleMoves,
                                                                    self.moat)

        return (x, y), mob, actionsProbability

    def getMoveFromNN(self):
        # 1. Start turn to actualize possibleMoves and prepare input for battle model

        state = self.env.prepareInputForNN(self.env.queue.queue[-1], False)

        # 2. Get actions probabilities and take the action with highest probability

        (x, y), mob, actionsProbability = self.getAction(state)
        # 3. If it is not possible to click in the highest probability hex then get another highest probability move
        if not self.checkPossibility((x, y), mob):
            while True:
                if (x, y) == mob.field:
                    actionsProbability[np.argmax(actionsProbability)] = -2.
                else:
                    actionsProbability[np.argmax(actionsProbability)] = -2.
                if self.checkPossibility((x, y), mob):
                    break
        self.env.printEnvironment()
        print("After While")

        target = None if (x, y) == mob.field else (x, y)
        if mob.type.size == 2 and (x + 1, y) == mob.field:
            target = None
        print("Choice ", (x, y), "Curr Pos ", mob.field)
        print(mob.field, " move to ", target)
        return target

    def checkPossibility(self, target, mob):
        x, y = target

        if not self.env.possibleMoves[x, y]:  # Basic condition (move has to be reachable)
            print("Not possible")
            return False

        elif (x, y) == mob.field or (
                mob.type.size == 2 and (x + 1, y) == mob.field):  # Condition for wait/defense execution
            # Wait is problematic, because of the possibility to make one wait per round
            # that's why if this condition is met just defend
            defend()
            print("Defend")
            return True

        else:
            print("Break")
            return True

    def skipEnemiesInQueue(self):
        while not self.env.queue.queue[-1].ally:
            self.env.queue.move()

    def actualizeQueue(self, setOfCreatures: list):
        self.env.queue.queue = []
        for unit in reversed(setOfCreatures):
            self.env.queue.queue.append(unit)

    def fight(self, hero_name, skills, spell_power):
        self.hero_skills = skills
        self.hero_name = hero_name
        self.spell_power = spell_power

        ok_button_img = cv2.imread(r'./battleAI/ok_button.png')
        # --- FIRST TURN ---
        while not checkIfTurnIsOurs(self.screen):
            time.sleep(1)

        self.terrain = checkTerrainType()
        # Create new environment, skill all the enemies from queue and do first move
        units = self.findUnits()

        self.start(units, self.findObstacles(units))

        self.env.allowDying = False
        self.skipEnemiesInQueue()

        # ------------------
        time.sleep(3)  # Wait for the end odf the move
        run = True
        counter = 0
        # ---- NEXT TURNS ----
        while run:
            # 1. Wait for our turn
            while not checkIfTurnIsOurs(self.screen):
                if checkIfEnd(ok_button_img):
                    run = False
                    move_mouse_and_click_battle(1150, 775)
                    break
                time.sleep(1)

            if not run:
                break


            # 2. When first mob in queue is not friendly we need to actualize environment (synchronize queue and game)
            if not self.env.queue.queue[-1].ally:
                # 2.1 When turn is ours, find units at the battlefield
                counter += 1
                units = self.findUnits()

                # 2.2 Actualize environment and queue
                self.env.resetEnv(units, self.env.obstacles)
                self.actualizeQueue(units)

                if bookAvailable():
                    spell_target, spell_name = Use_magic(units)

            # 3. Choose and make move
            while self.env.queue.queue[-1].ally:
                counter = 0
                mouse.move(0, 0, duration=0)
                while mouse.get_position() != (0, 0):
                    pass
                time.sleep(1)
                # save queue image before moving
                queue_before = take_whole_queue()

                current_position = self.env.queue.queue[-1].field

                _ = self.get_possible_moves(self.env.state[current_position])

                if self.env.queue.queue[-1].type.name != "Catapult":
                    self.debunk_obstacles()

                target = self.getMoveFromNN()
                if checkIfEnd(ok_button_img):
                    run = False

                if self.env.state[current_position].type.name == "FirstAid":
                    healed = False
                    while not healed:
                        self.makeMove(target)
                        # move mouse to the corner just to be sure it's not on queue or creature
                        mouse.move(0, 0, duration=0)
                        while mouse.get_position() != (0, 0):
                            pass
                        time.sleep(1)
                        # save queue image after moving
                        queue_after = take_whole_queue()

                        if arePicturesSimilar(queue_before, queue_after, 6):
                            self.env.queue.undoMove()
                            self.env.possibleMoves[target] = 0
                        else:
                            healed = True
                else:
                    self.makeMove(target)
                    if target is not None:
                        self.screen.last_turn_units.append(target)
                time.sleep(3)  # Wait for the end of the move

                # check if the target we just attacked is still alive
                # required in case we got additional turn after killing enemy
                # because in this case the queue will change even though it didn't move
                if isinstance(self.env.state[target], CreatureBox) and not self.env.state[target].ally:
                    alive = self.check_if_still_alive(target)
                    # if the target died we need to scan the battle field again
                    if not alive:
                        break

                # move mouse to the corner just to be sure it's not on queue or creature
                mouse.move(0, 0, duration=0)
                while mouse.get_position() != (0, 0):
                    pass
                time.sleep(1)
                # save queue image after moving
                queue_after = take_whole_queue()
                # if we get additional turn undo moving the queue
                if arePicturesSimilar(queue_before, queue_after, 6):
                    self.env.queue.undoMove()
                if checkIfEnd(ok_button_img):
                    run = False
                    move_mouse_and_click_battle(1150, 775)
                    break


if __name__ == "__main__":
    battleAI = BattleAI()
    battleAI.fight("Brissa", {"Ballistics": 0}, 2)
