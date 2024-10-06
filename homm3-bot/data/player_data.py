"""Script containing player class"""
from data.hero import Hero
from GUI_handling import AdventureGUI


class Player:
    def __init__(self, color: str,  gold: int = 0, wood: int = 0, ore: int = 0, mercury: int = 0, sulfur: int = 0,
                 crystal: int = 0, gems: int = 0, month: int = 1, week: int = 1, day: int = 1):
        """
        Class representing a player. Each player has a different color and different amounts of resources.

        :param color: Color of the player
        :param gold: Amount of owned gold
        :param wood: Amount of owned wood
        :param ore: Amount of owned ore
        :param mercury: Amount of owned mercury
        :param sulfur: Amount of owned sulfur
        :param crystal: Amount of owned crystal
        :param gems: Amount of owned gems
        :param month: Current month
        :param week: Current week
        :param day: Current day
        """
        self.color = color
        self.gold = gold
        self.wood = wood
        self.ore = ore
        self.mercury = mercury
        self.sulfur = sulfur
        self.crystal = crystal
        self.gems = gems
        self.heroes: list[Hero] = []  # set type of heroes (list of Hero)
        self.enemies: list[Hero] = []
        self.cities = []
        self.month = month
        self.week = week
        self.day = day
        self.daily_income = [500, 0, 0, 0, 0, 0, 0]
        self.camera = (0,0)
        self.captured_habitats = []
        self.captured_mines = []

    def logResources(self):
        print(f"[PLAYER RESOURCES]: Gold {self.gold}, Wood {self.wood}, Ore {self.ore}, Mercury "
              f"{self.mercury}, Sulfur {self.sulfur}, Crystals {self.crystal}, Gems {self.gems}")

    def addResource(self, idx, value):
        """
        Adds a specific resource to the player

        :param idx: parameter specifying a resource
        :param value: value of the added resource
        """
        # [self.gold, self.wood, self.ore, self.mercury, self.sulfur, self.crystal, self.gems]
        if idx == 0: self.gold += value
        elif idx == 1: self.wood += value
        elif idx == 2: self.ore += value
        elif idx == 3: self.mercury += value
        elif idx == 4: self.sulfur += value
        elif idx == 5: self.crystal += value
        elif idx == 6: self.gems += value

    def setResource(self, idx, value):
        """
        Sets a specific resource to the player

        :param idx: parameter specifying a resource
        :param value: value of the set resource
        """
        if idx == 0: self.gold = value
        elif idx == 1: self.wood = value
        elif idx == 2: self.ore = value
        elif idx == 3: self.mercury = value
        elif idx == 4: self.sulfur = value
        elif idx == 5: self.crystal = value
        elif idx == 6: self.gems = value


    # wrapers for gui functions with added camera position change
    def move_camera_up(self):
        """
        Moves the position of the camera up
        """
        AdventureGUI.move_camera_up()
        x = self.camera[0]
        y = self.camera[1] +1
        self.camera = (x,y)

    def move_camera_down(self):
        """
        Moves the position of the camera down
        """
        AdventureGUI.move_camera_down()
        x = self.camera[0]
        y = self.camera[1] - 1
        self.camera = (x, y)

    def move_camera_left(self):
        """
        Moves the position of the camera left
        """
        AdventureGUI.move_camera_left()
        x = self.camera[0] - 1
        y = self.camera[1]
        self.camera = (x, y)

    def move_camera_right(self):
        """
        Moves the position of the camera right
        """
        AdventureGUI.move_camera_right()
        x = self.camera[0] + 1
        y = self.camera[1]
        self.camera = (x, y)

    def move_to_hero(self,n):
        """
        Moves the position of the camera to hero
        """
        AdventureGUI.press_hero(n)
        self.camera = self.heroes[n].position

    def move_to_town(self,n):
        """
        Moves the position of the camera to town
        """
        AdventureGUI.press_town(n)
        self.camera = self.cities[n].position