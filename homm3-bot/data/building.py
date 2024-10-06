"""Script containing Cost and building class along with classes inheriting after building class"""

from data.creature import Creature
from data.magic import Spells


class Cost:
    def __init__(self, gold: int, wood: int, ore: int, mercury: int, sulfur: int, crystal: int, gems: int):
        """
        Class representing cost (in resources).

        :param gold: Amount of gold
        :param wood: Amount of wood
        :param ore: Amount of ore
        :param mercury: Amount of mercury
        :param sulfur: Amount of sulfur
        :param crystal: Amount of crystal
        :param gems: Amount of gems
        """
        self.gold = gold
        self.wood = wood
        self.ore = ore
        self.mercury = mercury
        self.sulfur = sulfur
        self.crystal = crystal
        self.gems = gems
        self.resources = [self.gold, self.wood, self.ore, self.mercury, self.sulfur, self.crystal, self.gems]


class Building:
    def __init__(self, name: str, built: bool = False, *cost: Cost):
        """
        Class representing Building (f.e MageGuild..)

        :param name: Name of the object
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        """
        self.name = name
        self.built = built
        self.cost = cost


class MageGuild(Building):
    def __init__(self, lvl: int, name: str, spells: Spells, *cost: Cost, built: bool = False):
        """
        Class Inheriting after building class. Representing Mage Guild building.

        :param lvl: Mage guild level
        :param name: Name of the building
        :param spells: Spells present in mage guild
        :param cost: Construction cost of the building
        :param built: boolean. built -> True, not built -> False
        """
        super().__init__(name, built, *cost)
        self.lvl = lvl
        self.spells = spells


class Fort(Building):
    def __init__(self, lvl: int = 0, name: str = "Fort", built=False,
                 *cost: Cost):
        """
        Class Inheriting after building class. Representing Fort building.

        :param lvl: Fort level
        :param name: Name of the building
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        """
        super().__init__(name, built, *cost)
        self.lvl = lvl


class CityHall(Building):
    def __init__(self, lvl: int = 0, name: str = '', built: bool = False, *cost: Cost, income: int = 500):
        """
        Class inheriting after building class. Representing City Hall building.

        :param lvl: Mage guild level
        :param name: Name of the building
        :param cost: Construction cost of the building
        :param built: boolean. built -> True, not built -> False
        :param income: Amount of gold received from the City Hall object
        """
        super().__init__(name, built, *cost)
        self.lvl = lvl
        self.income = income


class Tavern(Building):
    def __init__(self, name: str = '', built: bool = False, *cost: Cost):
        """
        Class inheriting after building class. Representing Tavern building.

        :param name: Name of the building
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        """
        super().__init__(name, built, *cost)


class Marketplace(Building):
    def __init__(self, name: str = '', built: bool = False, *cost: Cost):
        """
        Class inheriting after building class. Representing Marketplace building.

        :param name: Name of the building
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        """
        super().__init__(name, built, *cost)


class ResourceSilo(Building):
    def __init__(self, name: str = '', built: bool = False,
                 *cost: Cost, income: Cost):
        """
        Class inheriting after building class. Representing Resource Silo building.

        :param name: Name of the building
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        :param income: Amount of gold received from the Resource Silo object
        """
        super().__init__(name, built, *cost)
        self.income = income


class Habitat(Building):
    def __init__(self, cost: (Cost, Cost), unit: Creature, unit_up: Creature, growth: int,
                 unit_cost: Cost, unit_cost_up: Cost, to_buy: int = 0, lvl: int = 0,
                 name: str = '', built: bool = False):
        """
        Class inheriting after building class. Representing Habitat building.

        :param cost: Construction cost of the building
        :param unit: Which unit does the habitat produce
        :param unit_up: Which upgraded unit does the habitat produce
        :param growth: Unit growth per week
        :param unit_cost: Cost of the unit
        :param unit_cost_up: Cost of the upgraded unit
        :param to_buy: How many units is available to buy
        :param lvl: Habitat level
        :param name: Name of the building
        :param cost: Construction cost of the building
        :param built: boolean. built -> True, not built -> False
        """
        super().__init__(name, built, cost)
        self.lvl = lvl
        self.unit_type = unit
        self.unit_type_up = unit_up
        self.growth = growth
        self.unit_cost = unit_cost
        self.unit_cost_up = unit_cost_up
        self.unit_ready = growth
