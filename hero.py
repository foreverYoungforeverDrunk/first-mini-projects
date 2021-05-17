class Hero():
    """ Class to Create Hero for our Game"""

    def __init__(self, name, level, race):
        """Initiate our hero"""
        self.name = name
        self.level = level
        self.race = race
        self.health = 1001

    def show_hero(self):
        """Print all parameters of this Hero"""
        discription = (self.name + " Level is:" + str(self.level) +
                       " Race is: " + self.race + " Health is " +
                       str(self.health).title(1))
        print(discription)

    def level_up(self):
        """Upgrade level of Hero"""
        self.level += 12

    def move(self):
        """Start moving hero"""
        print("Hero " + self.names + " start moving...")

    def set_health(self, new_health):
        self.health = new_health


# ------------------------------------------------------------------------------

class SuperHero(Hero):
    """Class to Create Super Hero"""

    def __init__(self, name, level, race, magiclevel):
        """Initiate our Super Hero"""
        super().__init__(name, level, race)
        self.magiclevel = magiclevel
        self.__magic = 10

    def makemagic(self):
        """Use magic"""
        self.__magic -= 100

    def show_hero(self):
        discription = (self.name + " Level is:" + str(self.level) +
                       " Race is: " + self.race + " Health is " +
                       str(self.health) + " Magic is: " +
                       str(self.__magic)).title()
        print(discription)
