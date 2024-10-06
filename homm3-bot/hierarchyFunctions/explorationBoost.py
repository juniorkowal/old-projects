"""Module containing an algorithm that evaluates value of hero's exploration"""


# Counting how many tiles will be discovered after achieving specific goal
def evaluateExplorationBoost(goal: tuple, adventureMap):
    """
    Gives values to spaces next to fog of war

    :param goal:
    :param adventureMap:
    :return value:
    """
    radius = 6  # searching radius (square area)
    checkRadiusVec = [2, 3, 4, 5, 6, 6, 6, 6, 6, 5, 4, 3, 2]  # Defines shape of searching (diamond shape)
    valueIntensity = 1
    if not isinstance(adventureMap.obj[goal], int):
        if adventureMap.obj[goal].name == 'Redwood_Observatory':
            radius = 20
            checkRadiusVec = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20,
                              20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19, 18, 17, 16, 15, 14, 13, 12, 10,
                              9, 8, 7, 6, 5, 4, 3, 2]

    fogsInSquare = 0  # Loop which is searching for fog objects in square area
    for x in range(goal[0] - radius, goal[0] + radius):
        for y in range(goal[1] - radius, goal[1] + radius):
            if 0 <= x < adventureMap.obj.shape[0] and 0 <= y < adventureMap.obj.shape[1]:
                if not adventureMap.maskMap[x, y]:
                    fogsInSquare += 1

    discoveredFogs = 0  # HoH3 discovering area for hero has not square shape. It has diamond shape
    for y in range(goal[0] - radius, goal[0] + radius):
        for x in range(goal[1] - checkRadiusVec[y + radius - goal[0]],
                       goal[1] + checkRadiusVec[y + radius - goal[0]]):
            if 0 <= x < adventureMap.obj.shape[0] and 0 <= y < adventureMap.obj.shape[1]:
                if not adventureMap.maskMap[x, y]:
                    discoveredFogs += 1

    value = (fogsInSquare + discoveredFogs) * valueIntensity
    return value
