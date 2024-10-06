import random as rd

import numpy as np

from data.BattleAI_environment_needs import *
from battleAI.damage import baseDamage
from battleAI.queue_test import BattleQueue


def divideIntoAllyAndEnemy(setOfCreatures: list):
    """
    Function which divides list with all creatures into lists with allied creatures and hostile creatures

    :param setOfCreatures: list with all the creatures
    :return ally: list with allied creatures
    :return enemy: list with hostile creatures
    """
    ally = []
    enemy = []
    for mob in setOfCreatures:
        if mob.ally:
            ally.append(mob)
        else:
            enemy.append(mob)

    return ally, enemy


def even(x: int):
    """
    Returns True if value is even, False otherwise

    :rtype: int value
    """
    if x % 2 == 0:
        return True
    return False


def odd(x: int):
    """
    Returns True if value is odd, False otherwise

    :rtype: int value
    """
    if x % 2 != 0:
        return True
    return False


def getNeighbours(hexField: tuple):
    """
    Function which gets all the neighbours of specific tile at the hexagonal field

    :param hexField: input position
    :return neighbours: dictionary where key is tuple position and value is string which describes direction like
        "right", "left", "bottom_right" etc. It is needed for detecting direction when attacking.
    """
    x = hexField[0]
    y = hexField[1]

    # Selecting neighbours
    neighbours = {}
    if odd(y):
        if y < 10: neighbours["bottom_right"] = (x, y + 1)
        if y > 0: neighbours["top_right"] = (x, y - 1)
        if x < 14: neighbours["right"] = (x + 1, y)
        if x > 0:
            neighbours["left"] = (x - 1, y)
            if y > 0: neighbours["top_left"] = (x - 1, y - 1)
            if y < 10: neighbours["bottom_left"] = (x - 1, y + 1)

    else:
        if y < 10: neighbours["bottom_left"] = (x, y + 1)
        if y > 0: neighbours["top_left"] = (x, y - 1)
        if x > 0: neighbours["left"] = (x - 1, y)
        if x < 14:
            neighbours["right"] = (x + 1, y)
            if y < 10: neighbours["bottom_right"] = (x + 1, y + 1)
            if y > 0: neighbours["top_right"] = (x + 1, y - 1)

    return neighbours


# class for coloring text printed in console
class Colors:
    """
    Dataclass with defined colors of the text written in console. To use it just write
    print(Colors.<name_of_color> + text + Colors.ENDC). Colors.ENDC is necessary if we want back to the original color
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Environment:
    def __init__(self, setOfCreatures, setOfObstacles, training):
        """
        This class implements battle environment used in learning BattleAI and making predictions in game by it.

        :param setOfCreatures: list with all the creatures at the battlefield
        :param setOfObstacles: list with all the obstacles at the battlefield
        """
        self.state = None
        self.possibleMoves = np.zeros((15, 11))
        self.illegalMove = 0
        self.training = training

        self.resetEnv(setOfCreatures, setOfObstacles)

        # Temporary solution till queue will be upgraded
        ally, enemy = divideIntoAllyAndEnemy(setOfCreatures)
        self.queue = BattleQueue(ally, enemy)

        self.obstacles = setOfObstacles

        # Dealing damage contains a random element meaning our environment can sometimes decide
        # that our unit died from counterattack even if it didn't and delete it from the battlefield
        # set it to False to prevent that from happening
        self.allowDying = True

        self.siege_walls = None
        self.moat = None
        # {coordinates:hp}
        self.destructible_walls = None

    def resetEnv(self, setOfCreatures: list, setOfObstacles: list):
        """
        Function which resets the environment.

        :param setOfCreatures: list with all the creatures at the battlefield
        :param setOfObstacles: list with all the obstacles at the battlefield
        """
        self.state = np.zeros((15, 11), dtype=object)
        self.__initializeCreatures(setOfCreatures)
        self.__initializeObstacles(setOfObstacles)

    def __initializeCreatures(self, setOfCreatures: list):
        """
        Function which adds creatures to the game state (battlefield array)

        :param setOfCreatures: list with all the creatures at the battlefield
        """
        # Part of state definition, putting creatures to the environment
        for mob in setOfCreatures:
            x, y = mob.field
            self.state[x][y] = mob

            # If unit is 2hex size, we need to add additional "tail" of the creature
            if mob.type.size == 2:
                if mob.ally:
                    self.state[x - 1][y] = copy.deepcopy(mob)
                    self.state[x - 1][y].field = (x - 1, y)
                else:
                    self.state[x + 1][y] = copy.deepcopy(mob)
                    self.state[x + 1][y].field = (x + 1, y)

    def __initializeObstacles(self, setOfObstacles: list):
        """
        Function which adds obstacles to the game state (battlefield array).

        :param setOfObstacles: list with all the obstacles at the battlefield
        """
        # Part of state definition, putting obstacles to the environment (hexes we cannot move on)
        for obstacle in setOfObstacles:
            x, y = obstacle.field
            self.state[x][y] = obstacle

    def __swapCreatureWithEmptySlot(self, start: tuple, target: tuple):
        """
        Function which moves creature or creature part (for two hex units) with the empty space at the battlefield.

        :param start: creature or creature part position
        :param target: empty spaces we want to swap with creature
        """
        x1, y1 = start
        x2, y2 = target

        self.state[x2][y2] = self.state[x1][y1]
        self.state[x2][y2].field = (x2, y2)
        self.state[x1][y1] = 0

    def __del2HexFromState(self, target: tuple):
        """
        Function which deletes 2hex unit from game state

        :param target: (tuple) tail or head position of the unit we want delete
        """
        x, y = target
        if x == 0:
            self.state[x, y] = 0
            self.state[x + 1, y] = 0

        elif x == 14:
            self.state[x, y] = 0
            self.state[x - 1, y] = 0

        elif not self.state[x, y].eqLeft(self.state[x + 1, y]) and self.state[x, y].eqRight(self.state[x + 1, y]):
            self.state[x, y] = 0
            self.state[x + 1, y] = 0

        else:
            self.state[x, y] = 0
            self.state[x - 1, y] = 0

    def __unit2HexStatsActualization(self, target: tuple, newHP, newQuantity):
        """
        Function which actualize health points and quantity of the unit. Used after counterattack.

        :param target: (tuple) Position of the unit in battlefield we want to actualize
        :param newHP: (int) New health points for changing stackHP attribute
        :param newQuantity: (int) New quantity number for changing quantity attribute
        """
        x, y = target
        if x == 0:
            self.state[x, y].stackHP = newHP
            self.state[x, y].quantity = newQuantity
            self.state[x + 1, y].stackHP = newHP
            self.state[x + 1, y].quantity = newQuantity

        elif x == 14:
            self.state[x, y].stackHP = newHP
            self.state[x, y].quantity = newQuantity
            self.state[x - 1, y].stackHP = newHP
            self.state[x - 1, y].quantity = newQuantity

        elif not self.state[x, y].eqLeft(self.state[x + 1, y]) and self.state[x, y].eqRight(self.state[x + 1, y]):
            self.state[x, y].stackHP = newHP
            self.state[x, y].quantity = newQuantity
            self.state[x + 1, y].stackHP = newHP
            self.state[x + 1, y].quantity = newQuantity

        else:
            self.state[x, y].stackHP = newHP
            self.state[x, y].quantity = newQuantity
            self.state[x - 1, y].stackHP = newHP
            self.state[x - 1, y].quantity = newQuantity

    def __rangeAttack(self, target: tuple):
        """
        Function which simulates ranged attack. It takes as parameter only target of attack. Executor of the attack
        is the first

        :param target: (tuple) position of the target creature we want attack
        """
        # 1. Declaring attacker and defender
        attacker = self.queue.queue[0]
        defender = self.state[target]

        # 2. Attacker attacks defender
        damageAttack = baseDamage(attacker.type.damage[0], attacker.type.damage[1], attacker.quantity)
        DefenderNewHP = defender.stackHP - damageAttack
        DefenderNewQuantity = DefenderNewHP // defender.type.hp + 1

        # Decrease the amount of ammo
        self.queue.queue[0].type.ammo -= 1

        # 3. If hps less than zero, delete defender from environment
        if DefenderNewHP < 0 and self.allowDying:
            for i, mob in enumerate(self.queue.queue):
                if mob == defender:
                    # Delete unit from state
                    if defender.type.size == 2:
                        self.__del2HexFromState(target)
                    else:
                        self.state[target] = 0

                    # Delete from queue
                    del self.queue.queue[i]
                    break

        else:
            if DefenderNewHP < 0:
                DefenderNewHP = 0
            # Defender statistics actualization
            if defender.type.size == 2:  # Tail actualization
                self.__unit2HexStatsActualization(defender.field, DefenderNewHP, DefenderNewQuantity)
            else:
                self.state[target].stackHP = DefenderNewHP
                self.state[target].quantity = DefenderNewQuantity

    def __meleeAttack(self, target: tuple):
        """
        Simulates a melee attack

        :param target: (tuple) indices of the targeted tile
        """
        # 1. Declaring attacker and defender
        attacker = self.queue.queue[0]
        defender = self.state[target]

        # 2. Attacker attacks defender
        damageAttack = baseDamage(attacker.type.damage[0], attacker.type.damage[1], attacker.quantity)
        DefenderNewHP = defender.stackHP - damageAttack
        DefenderNewQuantity = DefenderNewHP // defender.type.hp + 1

        # 3. If hps less than zero, delete defender from environment
        if DefenderNewHP < 0 and self.allowDying:
            for i, mob in enumerate(self.queue.queue):
                if mob == defender:
                    # Delete unit from state
                    if defender.type.size == 2:
                        self.__del2HexFromState(target)
                    else:
                        self.state[target] = 0

                    # Delete from queue
                    del self.queue.queue[i]
                    break
        else:
            if DefenderNewHP < 0:
                DefenderNewHP = 0
            # 4. If defender is still alive, he counterattacks
            damageCounterAttack = baseDamage(defender.type.damage[0], defender.type.damage[1], DefenderNewQuantity)
            AttackerNewHP = attacker.stackHP - damageCounterAttack
            AttackerNewQuantity = AttackerNewHP // attacker.type.hp + 1

            # 5. If hps less than zero, delete attacker from environment
            if AttackerNewHP < 0 and self.allowDying:
                # Delete unit from state
                if attacker.type.size == 2:
                    self.__del2HexFromState(attacker.field)
                else:
                    self.state[attacker.field] = 0
                # Delete from queue
                del self.queue.queue[0]

            else:  # Attacker statistics actualization
                if AttackerNewHP < 0:
                    AttackerNewHP = 0
                if attacker.type.size == 2:  # 2Hex actualization
                    self.__unit2HexStatsActualization(attacker.field, AttackerNewHP, AttackerNewQuantity)
                else:
                    self.state[attacker.field].stackHP = AttackerNewHP
                    self.state[attacker.field].quantity = AttackerNewQuantity

            # Defender statistics actualization
            if defender.type.size == 2:  # Tail actualization
                self.__unit2HexStatsActualization(defender.field, DefenderNewHP, DefenderNewQuantity)
            else:
                self.state[target].stackHP = DefenderNewHP
                self.state[target].quantity = DefenderNewQuantity

    def __movingAndAttacking(self, startPos: tuple, target: tuple):
        """
        Performs action of moving and attacking 1-hex unit

        :param startPos: (tuple) starting indices of the attacker
        :param target:  (tuple) indices of the attack target
        :return: (str) side of the attack target we attack it from
        """
        neighbours = self.__getEmptyNeighbours(target)
        if len(neighbours) == 0:
            print("No neighbours, cant attack")
            self.illegalMove = 1
            return None

        key, endPos = rd.choice(list(neighbours.items()))
        return_after = False
        mob = None
        if "Strike and return" in self.queue.queue[-1].type.abilities:
            return_after = True
            mob = self.queue.queue[-1]
        self.__moving(startPos, endPos)
        self.__meleeAttack(target)
        if return_after and mob == self.queue.queue[0]:
            self.queue.undoMove()
            self.__moving(endPos, startPos)
        return key

    def __movingAndAttacking2Hex(self, startPos: tuple, target: tuple):
        """
        Performs action of moving and attacking 2-hex unit

        :param startPos: (tuple) starting indices of the attacker
        :param target:  (tuple) indices of the attack target
        :return: (str) side of the attack target we attack it from
        """
        # 1 Get neighbours and choose one randomly
        neighbours = self.__getEmptyNeighbours2Hex(target)
        if len(neighbours) == 0:
            print("No neighbours, cant attack")
            self.illegalMove = 1
            return None

        key, way = rd.choice(list(neighbours.items()))

        # 2. Make some corrections
        mob = self.queue.queue[-1]
        if mob.ally and (key == "bottom_right" or key == "top_right"):
            self.__moving2Hex(startPos, (way[0] + 1, way[1]))
        elif not mob.ally and (key == "bottom_left" or key == "top_left"):
            self.__moving2Hex(startPos, (way[0] - 1, way[1]))
        else:
            self.__moving2Hex(startPos, way)

        self.__meleeAttack(target)
        return key

    def __moving(self, start: tuple, target: tuple):  # Moving action
        """
        Performs moving action of a 1-hex unit

        :param start: (tuple) starting indices of a unit
        :param target: (tuple) target indices
        """
        # Case when we are in neighbourhood of the opponent and dont want to change our position but only attack him
        if self.state[target] != 0:
            self.queue.move()
        else:
            self.__swapCreatureWithEmptySlot(start, target)
            self.queue.queue[-1].field = target
            self.queue.move()

    def __moving2Hex(self, head: tuple, target: tuple):  # Moving action
        """
        Performs moving action of a 2-hex unit

        :param head: (tuple) starting indices of a unit's head
        :param target: (tuple) target indices
        :return: None - if the unit didn't move
        """
        x1, y1 = head
        x2, y2 = target
        # Case when we are in neighbourhood of the opponent and dont want to change our position but only attack him
        if self.state[target] != 0:
            # Move queue
            self.queue.move()
            return None

        # Initializing some variables for code reduction
        if self.queue.queue[-1].ally:
            tail = 1  # if mob is ally we need to check left side firstly
            start = 0  # for ally start of board is 0, this is needed for boundary cases execution
            end = 14
        else:
            tail = -1
            start = 14
            end = 0

        # Moving "tail" and "head" of the creature
        if x2 == start:  # Start of the map exception
            if self.state[x2 + tail, y2] == 0:
                self.__swapCreatureWithEmptySlot((x1 - tail, y1), (x2, y2))  # Moving tail
                self.__swapCreatureWithEmptySlot((x1, y1), (x2 + tail, y2))  # Moving head
            else:
                # print("I cant move on this hex")
                self.illegalMove = 1
                return None

        elif x2 == end:  # End of the map exception when only 1hex space
            if self.state[x2 - tail, y2] != 0:
                # print("I cant move on this hex")
                self.illegalMove = 1
                return None

        elif x1 == x2 - tail and y1 == y2:  # Move one hex to the front exception
            self.__swapCreatureWithEmptySlot((x1, y1), (x2, y2))  # Moving head
            self.__swapCreatureWithEmptySlot((x1 - tail, y1), (x2 - tail, y2))  # Moving tail

        elif x1 == x2 + 2 * tail and self.state[
            x1 - 3 * tail, y1] != 0 and y1 == y2:  # Move one hex to the back exception
            self.__swapCreatureWithEmptySlot((x1 - tail, y1), (x1 - 2 * tail, y2))  # Moving tail
            self.__swapCreatureWithEmptySlot((x1, y1), (x1 - tail, y2))  # Moving head

        elif self.state[x2 - tail, y2] != 0 and self.state[
            x2 + tail, y2] != 0:  # 1hex space in the interior of map exception
            # print("I cant move on this hex")
            self.illegalMove = 1
            return None

        elif self.state[x2 - tail][y2] == 0 and self.possibleMoves[x2 - tail, y2]:
            # After moving, tail still on the back side
            self.__swapCreatureWithEmptySlot((x1 - tail, y1), (x2 - tail, y2))  # Moving tail
            self.__swapCreatureWithEmptySlot((x1, y1), (x2, y2))  # Moving head

        else:
            # After moving, tail on the right side so we need to inverse head and tail
            self.__swapCreatureWithEmptySlot((x1 - tail, y1), (x2, y2))  # Moving tail
            self.__swapCreatureWithEmptySlot((x1, y1), (x2 + tail, y2))  # Moving head

        # Move queue
        self.queue.move()

    def __getEmptyNeighbours2Hex(self, hexField: tuple):
        """
        Finds empty neighbouring tiles of 2-hex unit

        :param hexField: (tuple) indices of the 2-hex unit
        :return: (list) of indices of empty neighbouring tiles
        """
        n = getNeighbours(hexField)
        neighbours = n.copy()

        # 0. Remembering first mob from the queue position and its tail
        mob = self.queue.queue[-1]
        mobx, moby = mob.field
        self.state[mobx, moby] = 0
        if mob.ally:
            tail = self.state[mobx - 1, moby]
            self.state[mobx - 1, moby] = 0
        else:
            tail = self.state[mobx + 1, moby]
            self.state[mobx + 1, moby] = 0

        for key, value in n.items():
            x, y = value
            # 1. The most important condition is empty neighbour
            if self.state[x, y] == 0 and self.possibleMoves[x, y]:
                # 2. Then we need to check 6 main cases with 2-3 sub-cases
                if key == "bottom_right":
                    if x == 0:  # Start of the map exception
                        # For this exception we need to check right place only
                        if self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            continue
                        else:
                            del neighbours['bottom_right']
                            continue

                    elif x == 14:  # End of the map exception
                        # For this exception we need to check left place only
                        if self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            neighbours['bottom'] = neighbours['bottom_right']
                            del neighbours['bottom_right']
                            continue
                        else:
                            del neighbours['bottom_right']
                            continue

                    else:
                        # For bottom right neighbour we need to check right place first
                        if self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            continue
                        # If right neighbour is not empty check left neighbour
                        elif self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            # If empty we need to change bottom right for bottom because of the specifics of 2hex units
                            neighbours['bottom'] = neighbours['bottom_right']
                            del neighbours['bottom_right']
                            continue
                        else:
                            del neighbours['bottom_right']
                            continue

                elif key == "bottom_left":
                    if x == 0:  # Start of the map exception
                        # For this exception we need to check right place only
                        if self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            neighbours['bottom'] = neighbours['bottom_left']
                            del neighbours['bottom_left']
                            continue
                        else:
                            del neighbours['bottom_left']
                            continue

                    elif x == 14:  # End of the map exception
                        # For this exception we need to check left place only
                        if self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            del neighbours['bottom_left']
                            continue
                        else:
                            neighbours['bottom_left'] = neighbours['bottom_left']
                            del neighbours['bottom_left']
                            continue

                    else:
                        # For bottom left neighbour we need to check left place first
                        if self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            continue
                        # If left neighbour is not empty check right neighbour
                        elif self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            # If empty we need to change bottom left for bottom because of the specifics of 2hex units
                            neighbours['bottom'] = neighbours['bottom_left']
                            del neighbours['bottom_left']
                            continue
                        else:
                            del neighbours['bottom_left']
                            continue

                elif key == "top_right":
                    if x == 0:  # Start of the map exception
                        # For this exception we need to check right place only
                        if self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            continue
                        else:
                            del neighbours['top_right']
                            continue

                    elif x == 14:  # End of the map exception
                        # For this exception we need to check left place only
                        if self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            neighbours['top'] = neighbours['top_right']
                            del neighbours['top_right']
                            continue
                        else:
                            del neighbours['top_right']
                            continue

                    else:
                        # SIMILAR TO BOTTOM RIGHT
                        if self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            continue
                        elif self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            neighbours['top'] = neighbours['top_right']
                            del neighbours['top_right']
                            continue
                        else:
                            del neighbours['top_right']
                            continue

                elif key == "top_left":
                    if x == 0:  # Start of the map exception
                        # For this exception we need to check right place only
                        if self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            neighbours['top'] = neighbours['top_left']
                            del neighbours['top_left']
                            continue
                        else:
                            del neighbours['top_left']
                            continue

                    elif x == 14:  # End of the map exception
                        # For this exception we need to check left place only
                        if self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            del neighbours['top_left']
                            continue
                        else:
                            neighbours['top_left'] = neighbours['top_left']
                            del neighbours['top_left']
                            continue

                    else:
                        # SIMILAR TO BOTTOM_LEFT
                        if self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            continue
                        elif self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            neighbours['top'] = neighbours['top_left']
                            del neighbours['top_left']
                            continue
                        else:
                            del neighbours['top_left']
                            continue

                elif key == "right":
                    # Need to check only neighbour in the right side
                    if x < 14:
                        if self.state[x + 1, y] == 0 and self.possibleMoves[x + 1, y]:
                            continue
                        else:
                            del neighbours['right']
                            continue
                    else:
                        del neighbours['right']
                        continue

                elif key == "left":
                    # Need to check only neighbour in the left side
                    if x > 0:
                        if self.state[x - 1, y] == 0 and self.possibleMoves[x - 1, y]:
                            continue
                        else:
                            del neighbours['left']
                            continue
                    else:
                        del neighbours['left']
                        continue
            else:
                del neighbours[key]

        self.state[mobx, moby] = mob
        if mob.ally:
            self.state[mobx - 1, moby] = tail
        else:
            self.state[mobx + 1, moby] = tail

        return neighbours

    def __getEmptyNeighbours(self, hexField: tuple):
        """
        Finds empty neighbouring tiles of 1-hex unit

        :param hexField: (tuple) indices of the 1-hex unit
        :return: (list) of indices of empty neighbouring tiles
        """
        n = getNeighbours(hexField)
        neighbours = n.copy()

        # 0. Remembering first mob from the queue position and filling it with zero, because in reachable neighbours
        # we want to include current position of the creature we move
        mob = self.queue.queue[-1]
        mobx, moby = mob.field
        self.state[mobx, moby] = 0

        # 1. Deleting not reachable neighbours
        for key, value in n.items():
            x, y = value
            if self.state[x][y] != 0 or not self.possibleMoves[x, y]:
                del neighbours[key]

        # 2. Back to previous state
        self.state[mobx, moby] = mob

        return neighbours

    def __event_CreatureAtTheEndOfPossibleMoves(self, possibleMoves, neighbour: tuple, mob: CreatureBox):
        """
        Checks if there is an enemy at the edge of possible moves. If so adds that tile to the possible moves

        :param possibleMoves: (np.array) 2D - non-zero elements are the tiles the unit can move on
        :param neighbour:   (tuple) checked tile at the edge of possible moves
        :param mob: (CreatureBox) currently moving unit
        """
        if isinstance(self.state[neighbour], CreatureBox):
            if self.state[neighbour].ally != mob.ally:
                possibleMoves[neighbour] = 1

    def __deleteObstaclesFromPossibleMoves(self, possibleMoves):
        """
        Sets tiles containing obstacles to 0 in possible moves array

        :param possibleMoves: (np.array) 2D - non-zero elements are the tiles the unit can move on
        """
        for x in range(15):
            for y in range(11):
                if isinstance(self.state[x, y], Obstacle):
                    possibleMoves[x, y] = 0

    def __deleteAlliedCreaturesFromPossibleMoves(self, possibleMoves, mob: CreatureBox):
        """
        Sets tiles containing ally creatures to 0 in possible moves array

        :param possibleMoves: (np.array) 2D - non-zero elements are the tiles the unit can move on
        :param mob: (CreatureBox) - currently moving unit
        """
        for x in range(15):
            for y in range(11):
                if isinstance(self.state[x, y], CreatureBox):
                    if self.state[x, y].ally == mob.ally and (x, y) != mob.field:
                        possibleMoves[x, y] = 0

    def __addAllOpponentsToPossibleMoves(self, possibleMoves, mob: CreatureBox):
        """
         Sets tiles containing opponent tiles to 1
         Useful for evaluating possible moves of ranged unit

         :param possibleMoves: (np.array) 2D - non-zero elements are the tiles the unit can move on
         :param mob: (CreatureBox) - currently moving unit
         """
        neighbours = getNeighbours(mob.field).values()
        neighbours = [i for i in neighbours if
                      (isinstance(self.state[i[0], i[1]], CreatureBox) and self.state[i[0], i[1]].ally != mob.ally)]
        if len(neighbours) == 0:
            for y in range(11):
                for x in range(15):
                    if isinstance(self.state[x, y], CreatureBox):
                        if self.state[x, y].ally != mob.ally:
                            possibleMoves[x, y] = 1

    def __possibleMovesFlying(self, mob):
        """
        Algorithm:
        0. Initialize possible moves table with zeros: np.zeros((15, 11))
        1. Start algorithm from field where creature we are moving is standing and add this field to "to visit" list
           This field is current node. Set value of this node as speed of the creature.
        2. Get neighbours of this field

        Do followings for each neighbour
        3. If current node has value greater than 1, so we have energy for continue moving, add neighbour
           to "to visit" list (it adding all the neighbours or no neighbour)
        4. If current node has value equal to 1 we need to check neighbours of this field one more time to check for
           creatures in neighbourhood of this field. This is necessary, because when we can reach neighbourhood of
           a creature, we can attack it too (so move should be possible). So check if this neighbour is a creature.
           If it is, set value of this neighbour to 1. (this triggers only when current node is equal to 1)
        5. If value of the node is not equal to 0 (value has not been set), set value of this node to currentNode value - 1

        6. Add currentNode to visited and delete it from "to visit" list
        7. Repeat algorithm to time when we do not have any node to visit ("to visit" list is empty)

        :return: (np.array) 2D - non-zero elements are the tiles the unit can move on
        """

        # Get first mob from queue
        # mob = self.queue.queue[-1]
        speed = mob.type.speed + 1
        visited = set()
        toVisit = [mob.field]

        # Initialization
        possibleMoves = np.zeros((15, 11))
        possibleMoves[mob.field] = speed
        while len(toVisit):
            # Get neighbours of the current node
            currentNode = toVisit[0]
            neighbours = getNeighbours(currentNode).values()

            for neighbour in neighbours:
                if neighbour not in visited:
                    # Add next nodes to visit
                    if possibleMoves[currentNode] > 1:
                        toVisit.append(neighbour)

                    # If this is the end check for creatures in neighbourhood
                    elif possibleMoves[currentNode] == 1:
                        self.__event_CreatureAtTheEndOfPossibleMoves(possibleMoves, neighbour, mob)

                    # If value of the neighbour has not been set, set value to value of current node minus 1
                    if not possibleMoves[neighbour]:
                        possibleMoves[neighbour] = possibleMoves[currentNode] - 1

            # Add current node to visited and delete it from "to visit" list
            visited.add(currentNode)
            del toVisit[0]

        return possibleMoves

    def __possibleMovesFlying1Hex(self, mob):
        """
        Evaluates possible moves of 1-hex flying unit
        sets all tiles as possible move except tiles containing allies and obstacles if unit's speed is
        greater or equal 18. Calls __possibleMovesFlying() otherwise

        :param mob: (CreatureBox) - currently moving unit
        :return: (np.array) 2D - non-zero elements are the tiles the unit can move on
        """
        if mob.type.speed >= 18:
            possibleMoves = np.ones((15, 11))
        else:
            possibleMoves = self.__possibleMovesFlying(mob)

        self.__deleteAlliedCreaturesFromPossibleMoves(possibleMoves, mob)
        self.__deleteObstaclesFromPossibleMoves(possibleMoves)
        if mob.type.ammo: self.__addAllOpponentsToPossibleMoves(possibleMoves, mob)

        return possibleMoves

    def __possibleMovesFlying2Hex(self, mob):
        """
        Evaluates possible moves of 1-hex flying unit
        sets all tiles as possible move except tiles containing allies and obstacles if unit's speed is
        greater or equal 17. Calls __possibleMovesFlying() otherwise. Proceeds with some postprocessing afterwards.

        :param mob: (CreatureBox) - currently moving unit
        :return: (np.array) 2D - non-zero elements are the tiles the unit can move on
        """
        # 1. Take possibleMoves for flying units and do some postprocessing
        # after defining possibleMoves we have to do some postprocessing to get realPossibleMoves true for 2hex units
        # possibleMoves here are only candidates for realPossibleMoves bc we need to have 2hex space for entering it
        if mob.type.speed >= 17:
            possibleMoves = np.ones((15, 11))
        else:
            possibleMoves = self.__possibleMovesFlying(mob)

        # 2. Initializing some variables for code reduction
        if mob.ally:
            tail = 1  # if mob is ally we need to check left side firstly
            start = 0  # for ally start of board is 0
            end = 14  # and end of board is 14, this is needed for boundary cases execution
        else:
            tail = -1
            start = 14
            end = 0

        # 3. Defining realPossibleMoves
        realPossibleMoves = np.zeros((15, 11))
        for y in range(11):
            for x in range(15):
                # Boundary case
                if x == start:
                    if self.state[x, y] == 0 and self.state[x + tail, y] == 0 \
                            and possibleMoves[x, y] and possibleMoves[x + tail, y]:
                        realPossibleMoves[x, y] = 1

                # Boundary case 2
                elif x == end:
                    if self.state[x, y] == 0 and (self.state[x - tail, y] == 0 or (x - tail, y) == mob.field) \
                            and possibleMoves[x, y] and possibleMoves[x - tail, y]:
                        realPossibleMoves[x, y] = 1

                # Firstly check default side for tail
                elif self.state[x, y] == 0 and (self.state[x - tail, y] == 0 or (x - tail, y) == mob.field) \
                        and possibleMoves[x, y] and possibleMoves[x - tail, y]:
                    realPossibleMoves[x, y] = 1

                # Then check default the other side
                elif self.state[x, y] == 0 and self.state[x + tail, y] == 0 \
                        and possibleMoves[x, y] and possibleMoves[x + tail, y]:
                    realPossibleMoves[x, y] = 1

        # 4. Adding to realPossibleMoves current position of unit we move
        realPossibleMoves[mob.field] = 1
        realPossibleMoves[mob.field[0] - tail, mob.field[1]] = 1

        # 5. Extending realPossibleMoves at the start side of the unit (if ally left, if not right)
        if mob.ally:
            for y in range(11):
                for x in range(13):
                    if realPossibleMoves[x + 1, y]:
                        if self.state[x, y] == 0:
                            realPossibleMoves[x, y] = 1
                            break  # go to the next row
        else:
            for y in range(11):
                for x in range(14, 0, -1):
                    if realPossibleMoves[x - 1, y]:
                        if self.state[x, y] == 0:
                            realPossibleMoves[x, y] = 1
                            break  # go to the next row

        # 6. Appending creatures in range to realPossibleMoves
        for y in range(11):
            for x in range(15):
                if isinstance(self.state[x, y], CreatureBox):
                    if self.state[x, y].ally != mob.ally:
                        n = self.__getEmptyNeighbours2Hex((x, y))
                        for neigh in n.values():
                            if isinstance(self.state[neigh], CreatureBox):
                                continue
                            if realPossibleMoves[neigh]:
                                realPossibleMoves[x, y] = 1

        if mob.type.ammo: self.__addAllOpponentsToPossibleMoves(possibleMoves, mob)

        return realPossibleMoves

    def __possibleMovesLand1Hex(self, mob):
        """
        Evaluates possible moves of non-flying 1-hex unit

        :param mob: (CreatureBox) - currently moving unit
        :return: (np.array) 2D - non-zero elements are the tiles the unit can move on
        """
        speed = mob.type.speed + 1
        visited = set()
        toVisit = [mob.field]

        # Initialization
        possibleMoves = np.zeros((15, 11))
        possibleMoves[mob.field] = speed
        while len(toVisit):
            # Get neighbours of the current node
            currentNode = toVisit[0]
            neighbours = getNeighbours(currentNode).values()

            for neighbour in neighbours:
                if neighbour not in visited:
                    # Add next nodes to visit
                    if possibleMoves[currentNode] > 1:
                        if not isinstance(self.state[neighbour], Obstacle): toVisit.append(neighbour)

                    # If this is the end check for creatures in neighbourhood
                    elif possibleMoves[currentNode] == 1 and not isinstance(self.state[currentNode], CreatureBox):
                        self.__event_CreatureAtTheEndOfPossibleMoves(possibleMoves, neighbour, mob)

                    # If value of the neighbour has not been set, set value to value of current node minus 1
                    if not possibleMoves[neighbour]:
                        if possibleMoves[currentNode] != 1 and isinstance(self.state[neighbour], CreatureBox):
                            possibleMoves[neighbour] = 1
                        elif not isinstance(self.state[neighbour], Obstacle):
                            possibleMoves[neighbour] = possibleMoves[currentNode] - 1

            # Add current node to visited and delete it from "to visit" list
            visited.add(currentNode)
            del toVisit[0]

        # Deleting ally creatures from possible moves except creature we moves
        self.__deleteAlliedCreaturesFromPossibleMoves(possibleMoves, mob)

        if mob.type.ammo: self.__addAllOpponentsToPossibleMoves(possibleMoves, mob)

        return possibleMoves

    def __possibleMovesLand2Hex(self, mob):
        """
        Evaluates possible moves of non-flying 2-hex unit

        :param mob: (CreatureBox) - currently moving unit
        :return: (np.array) 2D - non-zero elements are the tiles the unit can move on
        """
        speed = mob.type.speed + 1

        # 1. Initializing some variables for code reduction
        if mob.ally:
            tail = 1  # if mob is ally we need to check left side firstly
            start = 0  # for ally start of board is 0
            end = 14  # and end of board is 14, this is needed for boundary cases execution
        else:
            tail = -1
            start = 14
            end = 0

        # 2. Creating new thicker state (making obstacles and creatures one hex thicker)
        hex2State = np.zeros((15, 11))
        for y in range(11):
            for x in range(start, end, tail):
                if isinstance(self.state[x, y], Obstacle):
                    hex2State[x, y] = 1
                    hex2State[x + tail, y] = 1

                elif isinstance(self.state[x, y], CreatureBox):
                    if self.state[x, y].field != mob.field:
                        hex2State[x, y] = 2
                        hex2State[x + tail, y] = 2

                elif x == start:
                    hex2State[x, y] = 1

        # 3. Candidates for possible moves initialization
        possibleMoves = np.zeros((15, 11))
        possibleMoves[mob.field] = speed
        possibleMoves[mob.field[0] - tail, mob.field[1]] = speed - 1

        # 4. Classic 1hex possibleMoves algorithm but with two initial hexes in toVisit list
        toVisit = [mob.field, (mob.field[0] - tail, mob.field[1])]
        visited = set()
        while len(toVisit):
            # Get neighbours of the current node
            currentNode = toVisit[0]
            neighbours = getNeighbours(currentNode).values()

            for neighbour in neighbours:
                if neighbour not in visited:
                    # Add next nodes to visit
                    if possibleMoves[currentNode] > 1:
                        if not hex2State[neighbour] == 1: toVisit.append(neighbour)

                    # If this is the end check for creatures in neighbourhood
                    elif possibleMoves[currentNode] == 1 and not hex2State[currentNode] == 2:
                        self.__event_CreatureAtTheEndOfPossibleMoves(possibleMoves, neighbour, mob)

                    # If value of the neighbour has not been set, set value to value of current node minus 1
                    if not possibleMoves[neighbour]:
                        if possibleMoves[currentNode] != 1 and hex2State[neighbour] == 2:
                            possibleMoves[neighbour] = 1

                        elif not hex2State[neighbour] == 1:
                            possibleMoves[neighbour] = possibleMoves[currentNode] - 1

            # Add current node to visited and delete it from "to visit" list
            visited.add(currentNode)
            del toVisit[0]

        # 5. Defining realPossibleMoves
        realPossibleMoves = np.zeros((15, 11))
        for y in range(11):
            for x in range(15):
                # Boundary case
                if x == start:
                    if self.state[x, y] == 0 and self.state[x + tail, y] == 0 \
                            and possibleMoves[x, y] and possibleMoves[x + tail, y]:
                        realPossibleMoves[x, y] = 1

                # Boundary case 2
                elif x == end:
                    if self.state[x, y] == 0 and (self.state[x - tail, y] == 0 or (x - tail, y) == mob.field) \
                            and possibleMoves[x, y] and possibleMoves[x - tail, y]:
                        realPossibleMoves[x, y] = 1

                # Firstly check default side for tail
                elif self.state[x, y] == 0 and (self.state[x - tail, y] == 0 or (x - tail, y) == mob.field) \
                        and possibleMoves[x, y]:  # and possibleMoves[x - tail, y]:
                    realPossibleMoves[x, y] = 1

                # Then check default the other side
                elif self.state[x, y] == 0 and self.state[x + tail, y] == 0 \
                        and possibleMoves[x, y] and possibleMoves[x + tail, y]:
                    realPossibleMoves[x, y] = 1

        # 6. Adding to realPossibleMoves current position of unit we move
        realPossibleMoves[mob.field] = 1
        realPossibleMoves[mob.field[0] - tail, mob.field[1]] = 1

        # 7. Extending realPossibleMoves at the start side of the unit (if ally left, if not right)
        if mob.ally:
            for y in range(11):
                for x in range(13):
                    if realPossibleMoves[x + 1, y]:
                        if self.state[x, y] == 0:
                            realPossibleMoves[x, y] = 1
        else:
            for y in range(11):
                for x in range(14, 0, -1):
                    if realPossibleMoves[x - 1, y]:
                        if self.state[x, y] == 0:
                            realPossibleMoves[x, y] = 1

        # 8. Appending creatures in range to realPossibleMoves
        for y in range(11):
            for x in range(15):
                if isinstance(self.state[x, y], CreatureBox):
                    if self.state[x, y].ally != mob.ally:
                        n = self.__getEmptyNeighbours2Hex((x, y))
                        for neigh in n.values():
                            if isinstance(self.state[neigh], CreatureBox):
                                continue
                            if realPossibleMoves[neigh]:
                                realPossibleMoves[x, y] = 1

        if mob.type.ammo: self.__addAllOpponentsToPossibleMoves(possibleMoves, mob)

        return realPossibleMoves

    def filter_possible_moves(self, mob: CreatureBox, possibleMoves):
        """
        Makes additional limitations to possibleMoves based on our strategy :param mob: (CreatureBox) - currently
        moving

        :param possibleMoves: (np.array) 2D - non-zero elements are the tiles the unit can move on
        :return: (np.array) 2D - non-zero elements are the tiles the unit can move on, (np.array) 2D - non-zero elements
         are the tiles the unit can move on limited to only those we allow it to move on
        """
        # make range unit able to only shoot if not blocked
        alternatePossibleMoves = possibleMoves.copy()
        notMaskedPossibleMoves = possibleMoves.copy()

        if not self.training or (self.training and not mob.ally):
            notBlocked = False
            if mob.type.ammo > 0:
                for x in range(15):
                    for y in range(11):
                        if possibleMoves[x, y] != 0 and isinstance(self.state[x, y], CreatureBox) and \
                                self.state[x, y].ally != mob.ally:
                            alternatePossibleMoves[x, y] = 1
                            notBlocked = True
                        else:
                            alternatePossibleMoves[x, y] = 0
            if notBlocked:
                possibleMoves = alternatePossibleMoves
            # make melee unit able to only attack if it can
            else:
                for x in range(15):
                    for y in range(11):
                        if possibleMoves[x, y] != 0 and isinstance(self.state[x, y], CreatureBox) and \
                                self.state[x, y].ally != mob.ally:
                            # check if there is an empty hex to attack enemy from
                            if mob.type.size == 1:
                                neighbours = self.__getEmptyNeighbours((x, y))
                            else:
                                neighbours = self.__getEmptyNeighbours2Hex((x, y))

                            if len(neighbours) != 0:
                                alternatePossibleMoves[x, y] = 1
                                notBlocked = True
                            else:
                                alternatePossibleMoves[x, y] = 0
                        else:
                            alternatePossibleMoves[x, y] = 0
            if notBlocked:
                possibleMoves = alternatePossibleMoves

        return notMaskedPossibleMoves, possibleMoves

    def choosePossibleMoves(self, mob: CreatureBox, update=True):
        """
        Main function to execute appropriate possible moves evaluation

        :param mob: (CreatureBox) - currently moving unit
        :return: (np.array) 2D - non-zero elements are the tiles the unit can move on,
            (np.array) 2D - non-zero elements are the tiles the unit can move on limited to only those we allow it to move on
        """
        if mob.type.name == "Catapult":
            self.possibleMoves = np.zeros((15, 11))
            destructible = np.array([coordinate for coordinate in self.destructible_walls.keys() if self.destructible_walls[coordinate] != 0])
            self.possibleMoves[destructible[:, 0], destructible[:, 1]] = 1

            return self.possibleMoves, self.possibleMoves

        if mob.type.name == "FirstAid":
            self.possibleMoves = np.zeros((15, 11))
            ally_fields = np.array([unit.field for unit in self.queue.queue if unit.ally])
            self.possibleMoves[ally_fields[:, 0], ally_fields[:, 1]] = 1

            return self.possibleMoves, self.possibleMoves

        if mob.type.size == 2:
            if mob.type.fly:
                possibleMoves = self.__possibleMovesFlying2Hex(mob)
            else:
                possibleMoves = self.__possibleMovesLand2Hex(mob)

        else:
            if mob.type.fly:
                possibleMoves = self.__possibleMovesFlying1Hex(mob)
            else:
                possibleMoves = self.__possibleMovesLand1Hex(mob)

        if update:
            self.possibleMoves = possibleMoves

        notMaskedPossibleMoves, possibleMoves = self.filter_possible_moves(mob, possibleMoves)

        return notMaskedPossibleMoves, possibleMoves

    def moveCreature(self, hexField: tuple, update_possible_moves=True):
        """
        Simulates the move of a unit. Executes proper action depending on chosen tile

        :param hexField: (tuple) - indices of chosen tile to move on
        :return: (tuple) - indices of chosen tile to move on,
            (str) - side of the attack target we attack it from
        """
        self.illegalMove = 0  # Set illegal move to false by default
        mob = self.queue.queue[-1]  # Take first creature from queue
        x1, y1 = mob.field  # Move from (x1, y1) to (x2, y2)
        x2, y2 = hexField

        if mob.type.name == "Catapult" and not self.training:
            self.queue.move()
            return hexField, None

        if mob.type.name == "FirstAid":
            self.queue.move()
            return hexField, None

        # Choose right move type depending on the creature type:
        if update_possible_moves:
            self.possibleMoves, _ = self.choosePossibleMoves(mob)

        # Move only if possibleMove array (15x11) returns that targetField is possible to move on
        if self.possibleMoves[x2][y2] and not isinstance(self.state[x2][y2], Obstacle):
            # If targetField is creature, we are testing ally
            if isinstance(self.state[x2][y2], CreatureBox):
                # If targetField is enemy creature we need to decide from which side we want to attack
                if self.state[x1][y1].ally != self.state[x2][y2].ally:
                    mob.waited = False
                    neighbours = getNeighbours((x1, y1)).values()
                    neighbours = [i for i in neighbours if (isinstance(self.state[i[0], i[1]], CreatureBox) and
                                                            self.state[i[0], i[1]].ally != mob.ally)]
                    if self.state[x1][y1].type.ammo and len(neighbours) == 0:
                        self.queue.move()
                        self.__rangeAttack((x2, y2))
                        return hexField, None

                    else:
                        if mob.type.size == 1:
                            attackSide = self.__movingAndAttacking((x1, y1), (x2, y2))
                            return hexField, attackSide
                        else:
                            attackSide = self.__movingAndAttacking2Hex((x1, y1), (x2, y2))
                            return hexField, attackSide

                else:
                    self.queue.move()
                    print("Defend")  # Wait
                    return hexField, None

            else:
                if mob.type.size == 1:
                    self.__moving((x1, y1), (x2, y2))
                    return hexField, None
                else:
                    self.__moving2Hex((x1, y1), (x2, y2))
                    return hexField, None

        else:
            # print("I cant move on this hex")  # Cant move
            self.illegalMove = 1
            return None, None

    def prepareInputForNN(self, currUnit, update_possible_moves=True):
        """
        Input for neural network preparation
        Form (x, y, z)
        x, y: coordinates of the hex
        z: features of the hex (current hero/hero/obstacle/empty hex, num of creatures at the hex,
        attack, hp, speed, ammo)
        stats are negative for hostile creatures
        stats are zero for empty hex

        :return: (np.array) 3D - input for neural network
        """
        currPos = currUnit.field
        inputNN = np.zeros((15, 11, 7))
        # [    0#        1#       2#      3#      4#        5#, 6 ]
        # [ai_value, possible, ally, enemy, empty, , current]
        if update_possible_moves:
            _, possible_moves = self.choosePossibleMoves(currUnit, False)
        else:
            possible_moves = self.possibleMoves

        for x in range(self.state.shape[0]):
            for y in range(self.state.shape[1]):

                inputNN[x][y] = [0, 0, 0, 0, 0, 0, 0]
                if self.state[x][y] == 0:
                    inputNN[x][y][4] = 1

                if isinstance(self.state[x][y], Obstacle):
                    inputNN[x][y][5] = 1

                if isinstance(self.state[x][y], CreatureBox):
                    inputNN[x][y][0] = self.state[x][y].type.value/78845
                    inputNN[x][y][2] = 1 if self.state[x][y].ally else 0
                    inputNN[x][y][3] = 0 if self.state[x][y].ally else 1

                if possible_moves[x][y] == 0:
                    inputNN[x][y][1] = 0
                else:
                    inputNN[x][y][1] = 1

                if currPos == (x, y):
                    inputNN[x][y][6] = 1

        return inputNN

    def startTurn(self):
        """
        Takes unit from a queue and updates possibleMoves in environment according to it
        """
        mob = self.queue.queue[-1]
        self.possibleMoves, _ = self.choosePossibleMoves(mob)

    def printEnvironment(self):
        """
        Prints our environment state in console
        """
        if self.training:
            self.startTurn()
        for y in range(11):
            txt = ""
            for x in range(15):

                # Drawing creatures
                if isinstance(self.state[x][y], CreatureBox):
                    if self.state[x][y].ally:
                        if self.possibleMoves[x][y]:
                            txt += Colors.OKCYAN + "X " + Colors.ENDC
                        else:
                            txt += Colors.OKBLUE + "X " + Colors.ENDC
                    else:
                        if self.possibleMoves[x][y]:
                            txt += Colors.WARNING + "X " + Colors.ENDC
                        else:
                            txt += Colors.FAIL + "X " + Colors.ENDC

                # Drawing obstacles
                elif isinstance(self.state[x][y], Obstacle):
                    txt += Colors.BOLD + "X " + Colors.ENDC

                else:  # Drawing empty hexes
                    if self.possibleMoves[x][y]:
                        txt += Colors.OKGREEN + chr(1) + " " + Colors.ENDC
                    else:
                        txt += chr(1) + " "

            if even(y):
                print(" " + txt)
            else:
                print(txt)

        print("-----------------------------")

