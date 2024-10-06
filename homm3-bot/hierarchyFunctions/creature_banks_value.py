"""Module containing an algorithm that states the value of a creature bank"""
from data.creature_banks import *
from hierarchyFunctions.power_evaluation import *


def creature_bank_value(field: Creature_Bank, ourHero: Hero):
    """
    Function for calculating value for creature banks

    :param field: (Creature_Bank object) target creature bank
    :param ourHero: (Hero object) hero with specific army
    :return: (int) value of the given creature bank
    """
    # 1. If field is not Creature_Bank return 0
    if not type(field) == Creature_Bank:
        return 0

    # 2. Calculate power of the units in Creature Bank
    power = power_evaluation(ourHero, field.guard_reward[3].guard)

    # 4. Checking whether we have space for the new unit
    slot = -1
    valueForUnits = -1

    # 4.1 Testing if we have specific unit in our army
    for i, x in enumerate(ourHero.slots.slots):
        if x.unit.name == field.guard_reward[3].reward.units.slots[0].unit.name:
            slot = i

    # 4.2 If we do not have this unit in our army we are checking whether we have empty space for new unit
    if slot == -1:
        for i, x in enumerate(ourHero.slots.slots):
            if x.unit.name == "":
                slot = i
                break

    # 5. Calculate value for rewards (unit part)
    if slot != -1:
        valueForUnits = power * field.guard_reward[3].reward.units.slots[0].unit.value * \
                        field.guard_reward[3].reward.units.slots[0].amount  # XDDDDDDD

    # 6. Calculating value for rewards (resource part)
    # Resource factors for [gold, wood, ore, sulfur, mercury, gems, crystals]
    valuationOfResources = [1, 5, 5, 10, 10, 10, 10]
    valueForResources = 0
    for i, resource in enumerate(field.guard_reward[3].reward.resources):
        valueForResources += power * resource * valuationOfResources[i]

    return valueForUnits + valueForResources
