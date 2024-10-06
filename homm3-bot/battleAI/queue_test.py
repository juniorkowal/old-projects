class BattleQueue:
    def __init__(self, allyCreatures: list, enemyCreatures: list):
        """
        Class representing battle queue. Battle queue is a list of creatures that go into battle, 
        each creature has its own speed that determines its position in the queue.
        The creature with the highest speed value moves first. If two or more creatures on different 
        sides of engaging armies have the same speed value, the creature on the army which did not have
        the latest chance to act will act first. And if it is the beginning of the battle, the attacker 
        will have the initiative.

        :param allyCreatures: List of allied creatures
        :param enemyCreatures: List of enemy creatures
        """
        self.allies = allyCreatures.copy()
        self.enemies = enemyCreatures.copy()
        self.attacker = True
        self.acted = 1
        self.queue = []
        self.battleStart()

    def initial(self):
        """
        Function that sorts creatures based on their faction and speed.
        """
        while len(self.allies) > 0 and len(self.enemies) > 0:
            if self.allies[-1].type.speed == self.enemies[-1].type.speed and self.acted == 1:
                self.queue.append(self.enemies[-1])
                self.enemies.pop()
                self.acted = 0
            elif self.allies[-1].type.speed == self.enemies[-1].type.speed and self.acted == 0:
                self.queue.append(self.allies[-1])
                self.allies.pop()
                self.acted = 1
            elif self.allies[-1].type.speed < self.enemies[-1].type.speed:
                while len(self.enemies) > 0 and self.allies[-1].type.speed < self.enemies[-1].type.speed:
                    self.queue.append(self.enemies[-1])
                    self.enemies.pop()
                    self.acted = 0
            else:
                while len(self.allies) > 0 and self.allies[-1].type.speed > self.enemies[-1].type.speed:
                    self.queue.append(self.allies[-1])
                    self.allies.pop()
                    self.acted = 1
        while len(self.allies) > 0:
            self.queue.append(self.allies[-1])
            self.allies.pop()
        while len(self.enemies) > 0:
            self.queue.append(self.enemies[-1])
            self.enemies.pop()

    def battleStart(self):
        """
        This function sorts creatures based on their speed, faction and whether they already made an action.
        """
        self.allies.sort(key=lambda x: (x.type.speed, -(x.field[0] ** 2 + x.field[1] ** 2)))
        self.enemies.sort(key=lambda x: (x.type.speed, -(x.field[0] ** 2 + x.field[1] ** 2)))
        if self.attacker:
            while len(self.allies) > 0 and self.allies[-1].type.speed > self.enemies[-1].type.speed:
                self.queue.append(self.allies[-1])
                self.allies.pop()
                self.acted = 1
            self.initial()
        else:
            while len(self.enemies) > 0 and self.allies[-1].type.speed < self.enemies[-1].type.speed:
                self.queue.append(self.enemies[-1])
                self.enemies.pop()
                self.acted = 0
            self.initial()
        self.queue.reverse()

    def delete(self, hexPos):
        """
        Simple function which deletes a creature from the Battle queue based on its position.
        """
        for idx in range(len(self.queue) - 1):
            if self.queue[idx].field == hexPos:
                del self.queue[idx]

    def move(self):
        """
        This function simulates creature's move: attacking and moving.
        """
        self.queue.insert(0, self.queue[-1])
        self.queue = self.queue[:-1]

    def undoMove(self):
        """
        Function reverts creature's last move.
        """
        self.queue.append(self.queue[0])
        self.queue = self.queue[1:]

    def printQueue(self):
        """
        Show us our beautiful Battle queue.
        """
        for mob in self.queue:
            print('{:<17s}{:>4d}{:>6d}{:>6d}{:<1s}{:>2d}'.format(mob.type.name, mob.type.speed, mob.ally,
                                                                 mob.field[0], ', ', mob.field[1]))

    def getQueue(self):
        """
        Get the Battle queue's current status and parameters.

        :return: queue's parameters.
        """
        return self.queue
