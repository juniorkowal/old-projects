
from data.hero import *
"""Script that contains functions used to determine how many movement points does a hero have at the start of the day"""

# this function return value of movments points on land and on water at start a day
def calculate_movments_points_at_start_day(hero):
    """
    Function which calculate points of movments at start a day. It check how is the lowest speed unit in army,
    what artifacts and skills we have. On this basis it calculate bonus next add it to variable base_movment.
    :param hero: Hero class
    :return: points of movment at start a day
    """
    base_movment = 1900

    # variable for help to write instructions, in the future it will be read from game status --------------------------
    logistic = None
    navigation = None
    wearing_boots_of_speed = False
    wearing_equestrian_gloves = False
    wearing_necklace_of_ocean_guidance = False
    wearing_sea_captain_hat = False
    stables_visited = False
    lighthouse_visited = False

    # logistic ---------------------------------------------------------------------------------------------------------

    for i in range(8):
        if hero.skills.secondary_skills[i].name == "Logistics":
            logistic = hero.skills.secondary_skills[i].lvl

    # speed calc -------------------------------------------------------------------------------------------------------
    speed_list = []
    for i in range(7):
        speed_list.append(hero.slots.slots[i].unit.speed)
    speed_list_min = 10
    for speed in speed_list:
        if speed != 0 and speed < speed_list_min:
            speed_list_min = speed
    speed_of_the_slowest_unit_in_arm = speed_list_min

    # ------------------------------------------------------------------------------------------------------------------

    # artifacts check --------------------------------------------------------------------------------------------------
    if "Boots_of_Speed" in hero.artifacts['Feet']:
        wearing_boots_of_speed = True

    if "Equestrians_Gloves" in hero.artifacts['Ring']:
        wearing_equestrian_gloves = True
    # ------------------------------------------------------------------------------------------------------------------



    # check the speed of the slowest unit in army and calc movment points for hero
    if speed_of_the_slowest_unit_in_arm > 10:
        base_movment = 2000
    elif speed_of_the_slowest_unit_in_arm == 10:
        base_movment = 1960
    elif speed_of_the_slowest_unit_in_arm == 9:
        base_movment = 1900
    elif speed_of_the_slowest_unit_in_arm == 8:
        base_movment = 1830
    elif speed_of_the_slowest_unit_in_arm == 7:
        base_movment = 1760
    elif speed_of_the_slowest_unit_in_arm == 6:
        base_movment = 1700
    elif speed_of_the_slowest_unit_in_arm == 5:
        base_movment = 1630
    elif speed_of_the_slowest_unit_in_arm == 4:
        base_movment = 1560
    elif speed_of_the_slowest_unit_in_arm == 3:
        base_movment = 1500

    # check logistic bonus at land
    if logistic == 0: #'basic':
        logistic_or_navigation_bonus = base_movment * 0.05
    elif logistic == 1: #'advanced ':
        logistic_or_navigation_bonus = base_movment * 0.1
    elif logistic == 2: #'expert':
        logistic_or_navigation_bonus = base_movment * 0.2
    else:
        logistic_or_navigation_bonus = 0

    # check navigation bonus for moving on the boat
    if navigation == 'basic':
        navigation_or_navigation_bonus = base_movment * 0.15
    elif navigation == 'advanced ':
        navigation_or_navigation_bonus = base_movment * 0.2
    elif navigation == 'expert':
        navigation_or_navigation_bonus = base_movment * 0.25
    else:
        navigation_or_navigation_bonus = 0

    # check artifact bonus on land and water
    artifact_bonus_land = 0
    artifact_bonus_water = 0
    if wearing_boots_of_speed:
        artifact_bonus_land += 600
    if wearing_equestrian_gloves:
        artifact_bonus_land += 300
    if wearing_necklace_of_ocean_guidance:
        artifact_bonus_water += 1000
    if wearing_sea_captain_hat:
        artifact_bonus_water += 500

    # check stable/sighthouse bonus
    stable_bonus = 0
    lighthouse_bonus = 0
    if stables_visited:
        stable_bonus += 400
    if lighthouse_visited:
        lighthouse_bonus += 500

    movment_land = base_movment + logistic_or_navigation_bonus + artifact_bonus_land + stable_bonus
    # movment_water = base_movment + navigation_or_navigation_bonus + artifact_bonus_water + lighthouse_bonus

    print("Movment points: ", movment_land)

    return movment_land
