"""Script containing classes associated with various objects on map. """
import time

import data.resources_dec_tree
import image_processing.screen_slicing
import numpy as np
from GUI_handling import AdventureGUI
from GUI_handling.AdventureGUI import choose_chest
from data.Artifacts import Effect
from data.building import Cost
from image_processing.detecting_window import skills_window



class ObjectOnMap:
    def __init__(self, value: int, name: str, captured: bool = False, visited: bool = False):
        """
        Parent class of most objects on map

        :param value: Value of the object
        :param name: Name of the object
        :param captured: Boolean whether its captured or not
        :param visited: Boolean whether it's visited or not
        """
        self.name = name
        self.value = value
        self.captured = captured
        self.visited = visited

    def __repr__(self):
        return self.name + f' value: ({str(self.value)})'

    def __str__(self):
        return self.name + f' value: ({str(self.value)})'

    # placeholders for end ow week/day function
    def end_day(self, player):
        """
        End day buffer function

        :param player: Player object
        """
        pass

    def end_week(self, player):
        """
        End week buffer function

        :param player: Player object
        """
        pass

    def action(self, player, hero, okay=0, *args, **kwargs):
        """
        Action function that handles window

        :param player: Player object
        :param hero: Hero object
        :param okay: Parameter associated with window handling
        :return:
        """
        AdventureGUI.accept_offer()


class Mine(ObjectOnMap):
    def __init__(self, value: int, name: str, captured: bool = False, visited: bool = False):
        """
        class representing mines on the map

        :param value: int value
        :param name: name of the mine
        :param captured: boolean variable
        :param visited: boolean variable
        """
        super().__init__(value, name, captured, visited)
        self.position = (None, None)

    def __eq__(self, other):
        if isinstance(other, Mine):
            if self.name == other.name and self.position == other.position:
                return True
            else:
                return False
        else:
            return False

    def add_income(self, player):
        """
        function adding player income after capturing mine

        :param player: class Player
        :return:
        """

    def add_income(self, player):
        """
        function adds income of player after capturing this object

        :param player: class Player
        :return:
        """
        if self.name == "Gold_Mine":
            player.daily_income[0] += 1000
        if self.name == "Sawmill":
            player.daily_income[1] += 2
        if self.name == "Ore_Pit":
            player.daily_income[2] += 2
        if self.name == "Alchemists_Lab":
            player.daily_income[3] += 1
        if self.name == "Sulfur_Dune":
            player.daily_income[4] += 1
        if self.name == "Crystal_Cavern":
            player.daily_income[5] += 1
        if self.name == "Gem_Pond":
            player.daily_income[6] += 1

    def end_day(self, player):
        """
        function used after finished day to add resources to player.resources

        :param player: class Player
        :return:
        """
        if self.captured:
            if self.name == "Gold_Mine":
                player.addResource(0, 1000)
            if self.name == "Sawmill":
                player.addResource(1, 2)
            if self.name == "Ore_Pit":
                player.addResource(2, 2)
            if self.name == "Alchemists_Lab":
                player.addResource(3, 1)
            if self.name == "Sulfur_Dune":
                player.addResource(4, 1)
            if self.name == "Crystal_Cavern":
                player.addResource(5, 1)
            if self.name == "Gem_Pond":
                player.addResource(6, 1)

    def end_week(self, player):
        """
        XD

        :param player: class Player
        :return:
        """
        pass

    def action(self, player, hero, okay=0, *args, **kwargs):
        """
        information about capturing mine, or possibility to add garrison

        :param player: class Player
        :param hero: class  Hero
        :param okay: check if there is ok button
        :return:
        """
        if self not in player.captured_mines:
            player.captured_mines.append(self)
        self.captured = True
        time.sleep(0.04)
        AdventureGUI.accept_offer()


class Increase_Skill(ObjectOnMap):
    def __init__(self, value: int, name, skills: Effect):
        """
        Class representing objects on map that increase 4 basic skills attack ,defense, knowledge, spellpower

        :param value: int value
        :param name: name of the object
        :param skills: class effect
        """
        self.herolist = []
        super().__init__(value, name)
        self.skills = skills

    def action(self, player, hero, okay=0, *args, **kwargs):
        """
        if hero is not on list add him and give him bonus, list is permanent so each hero can receive bonus only once

        :param player: class Player
        :param hero: class Hero
        :param okay: check if there is ok button
        :return:
        """
        if hero not in self.herolist:
            self.herolist.append(hero)
            if self.name == "Arena":  # zrobione
                if hero.attack > hero.defense:
                    choose_chest("gold")
                else:
                    choose_chest("exp")
            if self.name == "Colosseum_of_the_Magi":  # zrobione
                if hero.spellpower > hero.knowledge:
                    choose_chest("gold")
                else:
                    choose_chest("exp")
            if self.name == "Library_of_Enlightenment":  # zrobione
                pass
            if self.name == "Marletto_Tower" or self.name == "Mercenary_Camp" or self.name == "Star_Axis" or self.name == "Garden_of_Revelation":  # zrobione
                hero.attack += self.skills.attack
                hero.defense += self.skills.defense
                hero.spellpower += self.skills.spell_power
                hero.knowledge += self.skills.knowledge
            if self.name == "School_of_Magic":  # zrobione
                if hero.spellpower > hero.knowledge:
                    choose_chest("gold")
                else:
                    choose_chest("exp")
                player.gold -= 1000
            if self.name == "School_of_War":  # zrobione
                if hero.attack > hero.defense:
                    choose_chest("gold")
                else:
                    choose_chest("exp")
                player.gold -= 1000
            AdventureGUI.accept_offer()
        else:
            AdventureGUI.accept_offer()


class LuckMorale(ObjectOnMap):
    def __init__(self, value: int, name, luck: int, morale: int):
        """
        Class representing objects that gives us morale or luck

        :param value: int value
        :param name: Name of the object
        :param luck: boolean variable
        :param morale: boolean variable
        """
        super().__init__(value, name)
        self.luck = luck
        self.morale = morale


class Mp(ObjectOnMap):
    def __init__(self, value: int, name, mp: int, reset: int = 7):
        """
        class representing objects that gives us movement points

        :param value: int value
        :param name: Name of the object
        :param mp: number of points
        :param reset: when objects resets and can give us ms again after last visit
        """
        super().__init__(value, name)
        self.mp = mp
        self.herolist = []
        self.reset = reset

    def end_week(self, player):
        """
        function clears herolist because after the whole week we can visit it again

        :param player: class Player
        :return:
        """

        self.herolist = []

    def action(self, player, hero, okay=0, *args, **kwargs):
        """
        if hero has not visited this type of buildings in this week we are adding him bonus

        :param player: Class Player
        :param hero: Class Hero
        :param okay: whether there is ok button
        :return:
        """
        if hero not in self.herolist:
            self.herolist.append(hero)
            AdventureGUI.accept_offer()
        else:
            AdventureGUI.accept_offer()



class DissapearOnClick(ObjectOnMap):
    def __init__(self, value: int, name):
        """
        Class representing objects that dissapear after visiting

        :param value: int value
        :param name: name of the object
        """
        super().__init__(value, name)

    def action(self, player, hero, okayImg=0, *args):
        """
        function performs an action after clicking on this object

        :param player: Class Player
        :param hero: Class Hero
        :param okayImg: whether there is ok button
        :return:
        """
        if self.name == "Treasure_Chest":
            if okayImg == 1:
                AdventureGUI.accept_offer()
            else:
                choice = data.resources_dec_tree.gold_or_exp(hero, player)
                AdventureGUI.choose_chest(choice)
                time.sleep(1)
                skills_window(hero)
        else:
            AdventureGUI.accept_offer()
        ranges = (
            (player.wood - 5, player.wood + 10),
            (player.mercury - 5, player.mercury + 10), (player.ore - 5, player.ore + 10),
            (player.sulfur - 5, player.sulfur + 10),
            (player.crystal - 5, player.crystal + 10), (player.gems - 5, player.gems + 10),
            (player.gold - 100, player.gold + 10000))
        image_processing.screen_slicing.check_resources(player, ranges)


class RescourcesOnClick(ObjectOnMap):
    def __init__(self, value: int, name, resources: Cost, reset: int = 7):
        """
        class representing objects that gives us resources after visited

        :param value: int value
        :param name: name of the object
        :param resources: what resources we get after visited
        :param reset: when objects can be visited again
        """
        super().__init__(value, name)
        self.resources = resources
        self.reset = reset

    def end_day(self, player):
        pass

    def end_week(self, player):
        """
        function used at the end of the week to let us know that we can get resources again

        :param player: Class Player
        """
        # we can visit each building once per week
        self.visited = False

    def action(self, player, hero, okay=0, *args, **kwargs):
        """
        function performs an action on the object

        :param player: class Player
        :param hero: class Hero
        :param okay: information whether there is ok button
        :return:
        """
        # we are setting availability of building and accepting its infobox
        self.visited = True
        time.sleep(0.04)
        AdventureGUI.accept_offer()
        ranges = (
            (player.wood - 5, player.wood + 10),
            (player.mercury - 5, player.mercury + 10), (player.ore - 5, player.ore + 10),
            (player.sulfur - 5, player.sulfur + 10),
            (player.crystal - 5, player.crystal + 10), (player.gems - 5, player.gems + 10),
            (player.gold - 100, player.gold + 10000))
        image_processing.screen_slicing.check_resources(player, ranges, self.resources)


class LearningStone(ObjectOnMap):
    def __init__(self,value: int, name: str, captured: bool = False, visited: bool = False):
        super(LearningStone,self).__init__(value, name, captured, visited)
    def action(self, player, hero, okay=0, *args, **kwargs):
        super(LearningStone, self).action(self, player, hero, okay, *args, **kwargs)
        time.sleep(0.04)
        skills_window(hero)


class Portals(ObjectOnMap):
    def __init__(self, name, value, entrance_coords, exit_coords, two_way=True, can_enter=True, exit_underground=False):
        """
        Class representing portals on map

        :param name: name of the object
        :param value: int value
        :param entrance_coords: ?
        :param exit_coords: ?
        :param two_way: boolean whether it is two way portal
        :param can_enter: boolean whether we can enter
        :param exit_underground: ?
        """
        super(Portals, self).__init__(value, name)
        self.entrance_coords = entrance_coords
        self.exit_coords = exit_coords
        self.two_way = two_way
        self.can_enter = can_enter
        self.exit_underground = exit_underground


class ObservationTower(ObjectOnMap):
    def __init__(self, value: int, name: str):
        """
                Parent class of ObservationTower object

                :param value: Value of the object
                :param name: Name of the object
                """
        super().__init__(value, name)

        self.mask = np.asarray([
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0],
            [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             1.0, 1.0,
             1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

    def action(self, player, hero, okay=0, *args, **kwargs):
        """
                Discovering tiles from Observation Tower.

                :param player: class Player
                :param hero: class Hero
                :param okay: information whether there is ok button
                :return:
                """
        self.visited = True
        mapa = args[0]
        fog = mapa.fog
        position = args[1]

        x1 = position[1] - 20
        x2 = position[1] + 20
        y1 = position[0] - 20
        y2 = position[0] + 20
        left, right, up, down = 0, 41, 0, 41
        if x1 < 0:
            left = np.abs(x1)
            right = 41
        if x2 > 71:
            right = 41 - (x2 - 71)
            left = 0
        if y1 < 0:
            up = np.abs(y1)
            down = 41
        if y2 > 71:
            down = 41 - (y2 - 71)
            up = 0

        mask = self.mask[up:down, left:right]
        mask_shape = np.shape(mask)
        for y in range(mask_shape[0]):
            for x in range(mask_shape[1]):
                if mask[y, x] == 1:
                    fog[position[0] - 20 + up + y, position[1] - 20 + left + x] = 1
        return fog


class ObeliskObject(ObjectOnMap):
    def __init__(self, value: int, name):
        """
        Class representing objects that gives us morale or luck

        :param value: int value
        :param name: Name of the object
        """
        super().__init__(value, name)

    def action(self, player, hero, okay=0, *args, **kwargs):
        """
        Action function that handles window

        :param player: Player object
        :param hero: Hero object
        :param okay: Parameter associated with window handling
        :return:
        """
        AdventureGUI.accept_offer()
        time.sleep(0.8)
        AdventureGUI.accept_offer()


# Mines--------------------------------------------
Sawmill = Mine(1500, "Sawmill")

Ore_Pit = Mine(1500, "Ore_Pit")

Crystal_Cavern = Mine(3500, "Crystal_Cavern")

Gem_Pond = Mine(3500, "Gem_Pond")

Alchemists_Lab = Mine(3500, "Alchemists_Lab")

Sulfur_Dune = Mine(3500, "Sulfur_Dune")

Gold_Mine = Mine(3500, "Gold_Mine")

Abandoned_Mine = Mine(3500, "Abandoned_Mine")

# Increase_Skills
Arena = Increase_Skill(3000, "Arena", Effect(0, 0, 0, 0))
Colosseum_of_the_Magi = Increase_Skill(3000, "Colosseum_of_the_Magi", Effect(0, 0, 0, 0))
Garden_of_Revelation = Increase_Skill(1500, "Garden_of_Revelation", Effect(0, 0, 0, 1))
Library_of_Enlightenment = Increase_Skill(-5000000, "Library_of_Enlightenment", Effect(0, 0, 0, 0))
Marletto_Tower = Increase_Skill(1500, "Marletto_Tower", Effect(0, 1, 0, 0))
Mercenary_Camp = Increase_Skill(1500, "Mercenary_Camp", Effect(1, 0, 0, 0))
School_of_Magic = Increase_Skill(1000, "School_of_Magic", Effect(0, 0, 0, 0))
School_of_War = Increase_Skill(1000, "School_of_War", Effect(0, 0, 0, 0))
Star_Axis = Increase_Skill(1500, "Star_Axis", Effect(0, 0, 1, 0))

# gives_resources_when_clicked
Derrick = RescourcesOnClick(750, "Derrick", Cost(500, 0, 0, 0, 0, 0, 0))
Lean_To = RescourcesOnClick(500, "Lean_To", Cost(0, 0, 0, 0, 0, 0, 0), 10000)
Mystical_Garden = RescourcesOnClick(500, "Mystical_Garden", Cost(0, 0, 0, 0, 0, 0, 0))
Prospector = RescourcesOnClick(500, "Prospector", Cost(0, 0, 0, 0, 0, 0, 0))
Warehouse_of_Crystal = RescourcesOnClick(2500, "Warehouse_of_Crystal", Cost(0, 0, 0, 0, 0, 6, 0))
Warehouse_of_Gem = RescourcesOnClick(2500, "Warehouse_of_Gem", Cost(0, 0, 0, 0, 0, 0, 6))
Warehouse_of_Gold = RescourcesOnClick(6000, "Warehouse_of_Gold", Cost(2000, 0, 0, 0, 0, 0, 0))
Warehouse_of_Mercury = RescourcesOnClick(2500, "Warehouse_of_Mercury", Cost(0, 0, 0, 6, 0, 0, 0))
Warehouse_of_Ore = RescourcesOnClick(2250, "Warehouse_of_Ore", Cost(0, 0, 10, 0, 0, 0, 0))
Warehouse_of_Sulfur = RescourcesOnClick(2500, "Warehouse_of_Sulfur", Cost(0, 0, 0, 0, 6, 0, 0))
Warehouse_of_Wood = RescourcesOnClick(2250, "Warehouse_of_Wood", Cost(0, 10, 0, 0, 0, 0, 0))
Water_Wheel = RescourcesOnClick(750, "Water_Wheel", Cost(500, 0, 0, 0, 0, 0, 0))
Windmill = RescourcesOnClick(2500, "Windmill", Cost(0, 0, 0, 0, 0, 0, 0))

# gives_to_luck_or_morale?
Faerie_Ring = LuckMorale(100, "Faerie_Ring", 1, 0)
Fountain_of_Fortune = LuckMorale(100, "Fountain_of_Fortune", 0, 0)
Idol_of_Fortune = LuckMorale(100, "Idol_of_Fortune", 1, 1)
Mermaids = LuckMorale(100, "Mermaids", 1, 0)
Swan_Pond = LuckMorale(100, "Swan_Pond", 2, 0)
Temple = LuckMorale(100, "Temple", 0, 1)
# _gives_mp
Rally_Flag = Mp(100, "Rally_Flag", 400)
Watering_Hole = Mp(500, "Watering_Hole", 400)
Watering_Place = Mp(500, "Watering_Place", 1000)
Fountain_of_Youth = ObjectOnMap(100, "Fountain_of_Youth")
Oasis = ObjectOnMap(100, "Oasis")
Stables = Mp(200, "Stables", 400)
# Disapears_after_click
Campfire = DissapearOnClick(2000, "Campfire")
Flotsam = DissapearOnClick(500, "Flotsam")
Grave = DissapearOnClick(500, "Grave")  # zmienia_sie
Jetsam = DissapearOnClick(500, "Jetsam")
Ocean_Bottle = DissapearOnClick(0, "Ocean_Bottle")
Prison = DissapearOnClick(5000, "Prison")
Pandoras_Box = DissapearOnClick(0, "Pandoras_Box")
Scholar = DissapearOnClick(1500, "Scholar")
Sea_Barrel = DissapearOnClick(500, "Sea_Barrel")
Sea_Chest = DissapearOnClick(1500, "Sea_Chest")
Shipwreck_Survivor = DissapearOnClick(1500, "Shipwreck_Survivor")
Treasure_Chest = DissapearOnClick(0, "Treasure_Chest")
Vial_Of_Mana = DissapearOnClick(3000, "Vial_Of_Mana")
Wagon = DissapearOnClick(500, "Wagon")

# Observation towers
Observation_Tower = ObservationTower(750, "Observation_Tower")
Redwood_Observatory = ObservationTower(750, "Redwood_Observatory")

# Obelisk
Obelisk = ObeliskObject(350, "Obelisk")

# Other
Altar_of_Mana = ObjectOnMap(100, "Altar_of_Mana")
Altar_of_Sacrifice = ObjectOnMap(100, "Altar_of_Sacrifice")
Ancient_Lamp = ObjectOnMap(5000, "Ancient_Lamp")
Anti_Magic_Garrison = ObjectOnMap(0, "Anti_Magic_Garrison")
Black_Market = ObjectOnMap(8000, "Black_Market")
Boat = ObjectOnMap(0, "Boat")
Border_Gate = ObjectOnMap(0, "Border_Gate")
Border_Guard = ObjectOnMap(0, "Border_Guard")
Buoy = ObjectOnMap(100, "Buoy")
Cannon_Yard = ObjectOnMap(3000, "Cannon_Yard")
Cartographer = ObjectOnMap(7500, "Cartographer")
Corpse = ObjectOnMap(500, "Corpse")
Cover_of_Darkness = ObjectOnMap(500, "Cover_of_Darkness")
Den_of_Thieves = ObjectOnMap(100, "Den_of_Thieves")
Freelancers_Guild = ObjectOnMap(100, "Freelancers_Guild")
Gazebo = ObjectOnMap(1500, "Gazebo")
Hermits_Shack = ObjectOnMap(1500, "Hermits_Shack")
Hill_Fort = ObjectOnMap(7000, "Hill_Fort")
Hut_of_The_Magi = ObjectOnMap(-10000, "Hut_of_The_Magi")
Junkman = ObjectOnMap(200, "Junkman")
Keymasters_Tent = ObjectOnMap(5000, "Keymasters_Tent")
Learning_Stone = LearningStone(1500, "Learning_Stone")
Lighthouse = ObjectOnMap(0, "Lighthouse")
Magic_Spring = ObjectOnMap(500, "Magic_Spring")
Magic_Well = ObjectOnMap(250, "Magic_Well")
Mineral_Spring = ObjectOnMap(500, "Mineral_Spring")
Monolith_One_Way_Entrance = ObjectOnMap(-10000, "Monolith_One_Way_Entrance")
Monolith_One_Way_Exit = ObjectOnMap(-10000, "Monolith_One_Way_Exit")
Monolith_Two_Way = ObjectOnMap(-10000, "Monolith_Two_Way")
Observatory = ObjectOnMap(500, "Observatory")
Pillar_of_Fire = ObjectOnMap(750, "Pillar_of_Fire")
Portal_One_Way_Entrance = ObjectOnMap(-10000, "Portal_One_Way_Entrance")
Portal_One_Way_Exit = ObjectOnMap(-10000, "Portal_One_Way_Exit")
Portal_Two_Way = ObjectOnMap(-10000, "Portal_Two_Way")
Quest_Guard = ObjectOnMap(-10000, "Quest_Guard")
Refugee_Camp = ObjectOnMap(5000, "Refugee_Camp")
Sanctuary = ObjectOnMap(-1000000, "Sanctuary")
Seafaring_Academy = ObjectOnMap(8000, "Seafaring_Academy")
Seers_Hut = ObjectOnMap(0, "Seers_Hut")
Shipyard = ObjectOnMap(0, "Shipyard")
Shrine_Of_Magic_Incantation = ObjectOnMap(500, "Shrine_Of_Magic_Incantation")
Shrine_Of_Magic_Gesture = ObjectOnMap(2000, "Shrine_Of_Magic_Gesture")
Shrine_Of_Magic_Mystery = ObjectOnMap(7000, "Shrine_Of_Magic_Mystery")
Shrine_Of_Magic_Thought = ObjectOnMap(3000, "Shrine_Of_Magic_Thought")
Subterranean_Gate = ObjectOnMap(0, "Subterranean_Gate")
Temple_Of_Loyalty = ObjectOnMap(100, "Temple_Of_Loyalty")
Town_Gate = ObjectOnMap(10000, "Town_Gate")
Trailblazer = ObjectOnMap(200, "Trailblazer")
Trading_Post = ObjectOnMap(3000, "Trading_Post")
Tree_Of_Knowledge = LearningStone(2500, "Tree_Of_Knowledge")
Warlocks_Lab = ObjectOnMap(10000, "Warlocks_Lab")
Whirlpool = ObjectOnMap(0, "Whirlpool")
Witch_Hut = ObjectOnMap(1500, "Witch_Hut")
War_Machine_Factory = ObjectOnMap(-50000, "War_Machine_Factory")
# jednostki_w_srodku
Garrison = ObjectOnMap(0, "Garrison")
