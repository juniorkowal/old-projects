"""Script containing functions used determining the most optimal path using greedy alghoritms"""
# Greedy Algorithm for a Optimisation Path Problem

# Implementation of greedy algorithm
# to choose one of the optimum choice
# gready algorithm we send to the function:
# 1) list of objects, consisting of classes having coordinates, value and costs
# 2) max of points movments
# 3) Values of classes to sort it from the most valuable
# function return
# 1) result - objects where we are going
# 2) totValue - collected value

def greedy(items, maxcal, keyfunction):
    """
    Function which find the best path from current point to objects in max of movments points.
    It sorting objects by their value and find path with the biggest sum of their values.
    :param items: list of objects
    :param maxcal: max of points movments
    :param keyfunction: Values of classes to sort it from the most valuable
    :return: list of objects, sum of value objects in a list of objects
    """
    itemsCopy = sorted(items, key=keyfunction, reverse=True)

    result = []
    totalVal = 0
    totalCal = 0

    for i in range(1, len(items)):
        if totalCal + itemsCopy[i].cost[itemsCopy[i-1].co_ordinates] <= maxcal:
            result.append(itemsCopy[i])
            totalVal = totalVal + itemsCopy[i].val
            totalCal = totalCal + itemsCopy[i].cost[itemsCopy[i-1].co_ordinates]

    return result, totalVal
