"""Script containing classes and functions handling our reward system"""
import numpy as np

import battleAI.reinforcmentLearningTest as rLT


class Tile:
    def __init__(self, point1, point2):
        """
        class representing a tile on a battlefield used in calculating distance

        :param point1: point 1 stating the location of the tile
        :param point2: point 2 stating the location of the destination tile
        """
        self.field = point1
        self.dest = point2
        self.G = 0
        self.H = hexDist(point1, point2)
        self.adjTiles = None

    def createAdjacentTiles(self, neighbours):
        """
        Creates adjacent tiles.

        :param neighbours: neighbour tiles of the tile
        """
        tiles = []
        for value in neighbours.values():
            if type(value) == tuple:
                adjTile = Tile(value, self.dest)
                tiles.append(adjTile)
        self.adjTiles = tiles

    def __lt__(self, other):
        """
        Compares whether one's tile G+H value is lower than other's

        :param other: different tile
        :return: bool
        """
        return self.G + self.H < other.G + other.H


def cubeDistance(point1, point2):
    """
    Calculate distance between points in 3D space.

    :param point1: list - coordinates [x,y,z]
    :param point2: list - coordinates [x,y,z]
    :return: int - distance between 2 points
    """
    a = abs(point1[0] - point2[0])
    b = abs(point1[1] - point2[1])
    c = abs(point1[2] - point2[2])
    return max(a, b, c)


def offsetToCube(point):
    """
    Change offset coordinates to cubic coordinates

    :param point: tuple - 2D offset coordinates (x, y)
    :return: list - coordinates [x,y,z]
    """
    col, row = point
    x = col - (row + (row & 1)) / 2
    y = row
    z = -x - y
    return [x, y, z]


def hexDist(point1, point2):
    """
    Calculates distance between 2 hexes

    :param point1: 2D offset coordinates (x, y)
    :param point2: 2D offset coordinates (x, y)
    :return: Cube distance between two hexes
    """
    # change hex indices into 3D coordinates
    # to simplify distance calculation
    point1 = offsetToCube(point1)
    point2 = offsetToCube(point2)
    # return distance between hexes measured in speed required to
    # get to the destination
    return cubeDistance(point1, point2)


def contains(container, item):
    """
    Helper function to check if container contains an item

    :param container: Container
    :param item: An item
    :return: True or False
    """
    if type(container) == list:
        for tile in container:
            if tile.field == item:
                return True
    elif type(container) == dict:
        for tile in container.values():
            if tile == item:
                return True
    return False


class Reward:
    def __init__(self, BattleEnv):
        """
        class representing a reward system.

        :param BattleEnv: Battle environment class
        """
        self.BattleEnv = BattleEnv
        self.queue = BattleEnv.queue.queue
        self.prevBlocked = 0
        self.prevHealth = 0
        self.done = False
        self.prevTeamHP = 0
        self.battle_result = 0

    def updateEnv(self, BattleEnv):
        """
        Updates battle environment and the queue.

        :param BattleEnv: Battle environment class
        """
        self.BattleEnv = BattleEnv
        self.queue = BattleEnv.queue.queue

    def calcPath(self, startPoint, endPoint):
        """
        Incomplete A* algorithm to compute real cost of a move/ speed required to move

        :param startPoint: Starting point
        :param endPoint: End point
        :return: Length of the path
        """
        openTiles = []
        closedTiles = []

        currentTile = Tile(startPoint, endPoint)
        openTiles.append(currentTile)

        G = 0

        while openTiles.__len__() != 0:
            openTiles = sorted(openTiles)
            currentTile = openTiles[0]
            openTiles.pop(0)
            closedTiles.append(currentTile)

            G = currentTile.G + 1
            if contains(closedTiles, endPoint):
                break
            neighbours = self.BattleEnv._Environment__getEmptyNeighbours(currentTile.field)
            neighboursAll = rLT.getNeighbours(currentTile.field)
            if contains(neighboursAll, endPoint):
                break
            currentTile.createAdjacentTiles(neighbours)
            for tile in currentTile.adjTiles:
                if contains(closedTiles, tile.field):
                    continue
                if not contains(openTiles, tile.field):
                    tile.G = G
                    openTiles.append(tile)
                elif tile.G + tile.H > G + tile.H:
                    tile.G = G
        return G - 1

    # inputs: current queue, whole queue
    def unitsInQueue(self, currQueue):
        """
        Counting % of allies and enemies still in queue

        :param currQueue: Queue
        :return: % of allies in queue, % of enemies in queue
        """
        allies, enemies = rLT.divideIntoAllyAndEnemy(self.queue)
        currAllies, currEnemies = rLT.divideIntoAllyAndEnemy(currQueue)
        alliesPercent = len(currAllies) / (len(allies) + len(enemies))
        enemiesPercent = len(currEnemies) / (len(allies) + len(enemies))

        return alliesPercent, enemiesPercent

    # calculate distance to opponents
    # temporally using queue since its currently a list of creatures on the battle field
    def opponentDistances(self, currUnitPos, side: str):
        """
        Calculate distance to opponents
        Temporally using queue since its currently a list of creatures on the battle field

        :param currUnitPos: Position of units
        :param side: "ally" or "enemy"
        :return: % of our units in range to an opponent
        """
        distances = []
        allies, enemies = rLT.divideIntoAllyAndEnemy(self.queue)
        if side == "ally":
            group = allies
        elif side == "enemy":
            group = enemies
        for unit in group:
            distances.append(self.calcPath(currUnitPos, unit.field))
        distances = np.array(distances)
        return distances

    # calculate % of units in range
    def unitsInRange(self, currUnitPos, speed, unitIsAlly, checkedSide: str):
        """
        Calculate % of units our unit is reaching

        :param currUnitPos: tuple - current position of our unit
        :param speed: int - speed of our unit
        :param unitIsAlly: bool - information whether our unit is an ally or enemy
        :param checkedSide: str - information which side of units are we checking
        :return: float - % of units our unit is reaching
        """
        allies, enemies = rLT.divideIntoAllyAndEnemy(self.queue)
        if (unitIsAlly and checkedSide == "ally") or (not unitIsAlly and checkedSide == "enemy"):
            side = "ally"
        elif (not unitIsAlly and checkedSide == "ally") or (unitIsAlly and checkedSide == "enemy"):
            side = "enemy"
        else:
            return
        distances = self.opponentDistances(currUnitPos, side)
        indexes = np.argwhere(speed > distances)
        if side == "ally":
            if len(allies) > 1:
                inRangePercent = (len(indexes) - 1) / (len(allies) - 1)
            elif len(allies) == 1:
                inRangePercent = 0
            else:
                inRangePercent = 0
                self.done = True
                self.battle_result = -1
        elif side == "enemy":
            if len(enemies) > 0:
                inRangePercent = len(indexes) / len(enemies)
            else:
                self.done = True
                self.battle_result = 1
                inRangePercent = 0
        else:
            return

        return inRangePercent

    def unitsReaching(self, currUnitPos, unitIsAlly, checkedSide: str):
        """
        Calculate % of units reaching our unit

        :param currUnitPos: Position of units on the battlfield
        :param unitIsAlly: Is a unit an ally
        :param checkedSide: :"ally" or "enemy"
        :return: % of units reaching our unit
        """
        allies, enemies = rLT.divideIntoAllyAndEnemy(self.queue)
        if (unitIsAlly and checkedSide == "ally") or (not unitIsAlly and checkedSide == "enemy"):
            group = allies
        elif (not unitIsAlly and checkedSide == "ally") or (unitIsAlly and checkedSide == "enemy"):
            group = enemies
        else:
            return
        reaching = 0
        for unit in group:
            distance = self.calcPath(unit.field, currUnitPos)
            if distance <= unit.type.speed:
                reaching = reaching + 1
        if checkedSide == "enemy":
            if len(group) > 0:
                reachingPercent = reaching / len(group)
            else:
                self.done = True
                reachingPercent = 0
                self.battle_result = 1
        elif checkedSide == "ally":
            if len(group) > 1:
                reachingPercent = (reaching - 1) / (len(group) - 1)
            elif len(group) == 1:
                reachingPercent = 0
            else:
                reachingPercent = 0
                self.done = True
                self.battle_result = -1
        else:
            return
        return reachingPercent

    def getTeamHP(self, currUnit, isTeamAlly):
        """
        Summing up all of the hp of the given team.

        :param currUnit: Current handled unit
        :param isTeamAlly: Checking whether team is allied or not
        :return: Summed hp of the team.
        """
        allies, enemies = rLT.divideIntoAllyAndEnemy(self.queue)
        if (currUnit.ally and isTeamAlly) or (not currUnit.ally and not isTeamAlly):
            group = allies
        else:
            group = enemies
        teamHP = 0
        for unit in group:
            teamHP += unit.stackHP

        self.prevTeamHP = teamHP
        return teamHP

    def damageDealt(self, currUnit, isTeamAlly=False):
        """
        Calculates damage dealt

        :param currUnit: currentUnit
        :param isTeamAlly: (Boolean) True-> allied, False -> not allied
        :return: stored HP - current HP
        """
        storedHP = self.prevTeamHP
        self.getTeamHP(currUnit, isTeamAlly)
        currentHP = self.prevTeamHP

        return storedHP - currentHP

    # calculate % of protected ranged allies
    def checkRanged(self, unitIsAlly):
        """
        Calculate % of protected ranged allies

        :param unitIsAlly: Boolean whether unit is allied or not
        :return: % of protected archers, % of blocked archers, % of released archers
        """
        allies, enemies = rLT.divideIntoAllyAndEnemy(self.queue)
        if unitIsAlly:
            group = allies
            opponentGroup = enemies
        else:
            group = enemies
            opponentGroup = allies
        protected = 0
        blocked = 0
        for unit in group:
            if unit.type.ammo == 0:
                continue
            emptyNeighbours = self.BattleEnv._Environment__getEmptyNeighbours(unit.field)
            neighbours = rLT.getNeighbours(unit.field)
            # if ally is surrounded by blocked tiles
            if len(emptyNeighbours) == 0:
                neighboursPositions = neighbours.values()
                # check if any of the blocked tiles is occupied by enemy
                enemyNeighbour = False
                for enemy in opponentGroup:
                    if contains(neighboursPositions, enemy):
                        enemyNeighbour = True
                # if not ranged is surrounded by obstacles and/or allies
                if not enemyNeighbour:
                    protected = protected + 1
                # if enemy is on a neighbouring tile the ally is blocked
                else:
                    blocked = blocked + 1
        if group.__len__() > 0:
            protectedPercent = protected / group.__len__()
            blockedPercent = blocked / group.__len__()
        else:
            protectedPercent = 0
            blockedPercent = 0
            self.done = True
            self.battle_result = -1
        # if number of currently blocked allies is lower than before they got released
        if blocked < self.prevBlocked:
            releasedPercent = (self.prevBlocked - blocked) / group.__len__()
            self.prevBlocked = blocked
        else:
            releasedPercent = 0
        return protectedPercent, blockedPercent, releasedPercent

    # save current's unit health before moving
    def saveUnitHealth(self, currUnit):
        """
        Updating unit's health before moving

        :param currUnit: Current handled unit
        """
        self.prevHealth = currUnit.stackHP

    # see if unit suffered from enemy's retaliation
    def retaliationTaken(self, health):
        """
        See if unit suffered from enemy's retaliation

        :param health: health of the unit
        :return: 1 - Taken, 0 - not taken
        """
        # if unit lost health during his own move
        if health < self.prevHealth:
            return 1
        else:
            return 0

    # calculate the reward
    # To be called after unit's move
    def calcReward(self, currUnit, BattleEnv):
        """
        Function that calculates the reward

        :param currUnit: Current unit
        :param BattleEnv: Battle enviroment class
        :return: reward, result of the battle
        """
        self.updateEnv(BattleEnv)
        alliesReaching = self.unitsReaching(currUnit.field, currUnit.ally, "ally")
        enemiesReaching = self.unitsReaching(currUnit.field, currUnit.ally, "enemy")
        alliesInRange = self.unitsInRange(currUnit.field, currUnit.type.speed, currUnit.ally, "ally")
        enemiesInRange = self.unitsInRange(currUnit.field, currUnit.type.speed, currUnit.ally, "enemy")
        retaliation = self.retaliationTaken(currUnit.stackHP)
        damageDealt = self.damageDealt(currUnit, isTeamAlly=False)
        # alliesInQueue, enemiesInQueue = unitsInQueue(currQueue)
        protectedRangedAllies, blockedRangedAllies, releasedRangedAllies = self.checkRanged(currUnit.ally)

        currUnit.damage_dealt = damageDealt

        reward = (3 * enemiesInRange if enemiesInRange > 0 else 0) + (1 - enemiesReaching) + \
                 (1 - blockedRangedAllies) + \
                 (0 if damageDealt == 0 else 30)

        if self.battle_result == 1:
            reward += 100
        if self.battle_result == -1:
            reward += -100

        return reward / 10, self.battle_result  # if currUnit.ally else -self.battle_result
