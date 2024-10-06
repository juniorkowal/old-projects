"""Script containing power evaluation algorithm"""
from colorama import Fore

from data.hero import Hero, Slot, Slots


def power_evaluation(x1: Hero, x2):
    """
    Function that evaluates power based on input parameters. Depending on parameter x2-Hero/Slot/Slots, different
    function will be used in power evaluation hero_power/creature_power/creatures_power

    :param x1: Hero object
    :param x2: Hero/Slot/Slots object
    :return: Compared power in form of ratio.
    """
    print(Fore.GREEN, end="")
    print("{0:^55}".format("-------------------power_evaluation--------------------"))
    print(Fore.BLUE, end="")
    p1 = hero_power(x1)
    p1 = p1 * 0.9
    print("")
    print("power of our hero = ", p1)
    print(Fore.CYAN,end="")
    p2 = 0

    if type(x2).__name__ == "Hero":
        p2 = hero_power(x2)
    elif type(x2).__name__ == "Slot":
        p2 = creature_power(x2)
    elif type(x2).__name__ == "Slots":
        p2 = creatures_power(x2)
    else:
        print(type(x2).__name__)
        print("podales zly typ!")

    print("")
    print("power of enemy = ", p2)
    print(Fore.GREEN, end="")
    p2 = p2 * 1.1 # artifical increased power of enemy units because bot is stupid :)
    cos = compare_power(p1, p2)
    print("------------------------------------------------------")
    print(Fore.RESET)
    return cos


def hero_power(hero: Hero):
    """
    function evaluates power(int) of hero

    :param hero: Class Hero
    :return: int
    """
    power = (1+hero.lvl/10) * creatures_power(hero.slots)
    return power


def creatures_power(slots: Slots):
    """
    function evaluates int: strength of Class Slots

    :param slots: Slots object
    :return: int - power
    """
    power = 0
    for s in slots.slots:
        power = power + creature_power(s)

    return power


def creature_power(slot: Slot):
    """
    Function stating creature's power

    :param slot: Slot object
    :return: int - power
    """
    power = slot.amount * slot.unit.value
    if slot.unit.ammo != 0:
        power = power * 1.5
    if slot.amount != 0:
        print("|", "{0:^19}".format(slot.unit.name), "|", "{0:^4}".format(slot.amount), "|", 'this units power: ', "{0:^7}".format(power))
    return power


def compare_power(x1, x2):
    """
    Compares power between x1 (int) and x2(int)

    :param x1: Strength parameter for first instance
    :param x2: Strength parameter for second instance
    :return: (float) ratio of strength. returns 1 -> win 100%. Returns -10 -> win 1%
    """
    ratio = x2/x1
    print(Fore.LIGHTRED_EX, end="")
    print("Ratio = ", ratio)
    print(Fore.GREEN, end="")
    if ratio < 0.5 or x2 == 0:
        print("win 100%")
        return 1
    elif ratio < 0.6:
        print("win 95%")
        return 0.9
    elif ratio < 0.7:
        print("win 90%")
        return 0.75
    elif ratio < 0.8:
        print("win 80%")
        return 0.2
    elif ratio < 0.9:
        print("win 65%")
        return -0.1
    elif ratio < 1:
        print("win 50% - our bot intelligence")
        return -0.3
    elif ratio < 1.1:
        print("win 10%")
        return -0.5
    elif ratio < 1.2:
        print("win 10%")
        return -1
    else:
        print("win 1%")
        return -10
