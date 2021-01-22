"""
Modul ini berisi class manusia
"""
import random

class Human():
    # initialize all attributes of the Human
    def __init__(self, HP=140, isActive=True, isShowingSymptom=False, isInfected=False, location=(0, 0), speed=(0, 0),
                 color='blue', drawID=0):  # color and drawID is used for drawing the human in canvas
        self.HP = HP    #UPDATE : the HP of every human is 140 now, so human will die on the 14th day
        self.isActive = isActive
        self.isShowingSymptom = isShowingSymptom
        self.isInfected = isInfected
        self.location = location
        self.speed = speed
        self.color = color
        self.drawID = drawID
        self.size = 10      # attribute to control the size of the human

    # method for interacting with a human
    def interactHuman(self, theHuman):
        # I will be infected if I am interacting with an infected human but he didn't show any symptoms
        if self.HP != 0:
            if theHuman.isInfected == True and theHuman.isShowingSymptom == False:
                self.isInfected = True
            self.bounce(theHuman)  # change my direction

    # method for interacting with a surface
    def interactSurface(self, theSurface):
        # I will be infected if I am interacting with an infected surface
        if theSurface.isInfected == True and self.HP != 0:
            self.isInfected = True
        self.bounce(theSurface)  # change my direction

    # method to set the human inactive
    def deactivate(self):
        self.isActive = False
        self.speed = [0, 0]

    # method for moving Human within the borders of the world
    def moveHuman(self, worldWidth, worldHeight):
        # human can only move if it is active
        if self.isActive:
            # add it's current location with its speed to get it's next location
            self.location[0] += self.speed[0]
            self.location[1] += self.speed[1]
            # check whether it has hit the borders of the world or not
            if self.location[0] >= worldWidth-self.size:
                self.speed[0] = -1     # if it hits the right borders, negate its x speed
            if self.location[0] <= 0:
                self.speed[0] = 1       # if it hits the left borders
            if self.location[1] >= worldHeight-self.size:
                self.speed[1] = -1     # if it hits the bottom borders, negate its y speed
            if self.location[1] <= 0:
                self.speed[1] = 1       # if it hits the top border
            # we use worldWidth-10 and worldHeight-10 because the size of the object is 10x10

    """# method for negating speed. It is used when two humans collide
    def negateSpeed(self):
        self.bounce()
        self.speed[0] = 0-self.speed[0]
        self.speed[1] = 0-self.speed[1]"""

    # method for bouncing off objects and borders
    def bounce(self, theHuman=None):
        self.speed = [0-self.speed[0],  # else, we set a random speed for each human
                      random.randint(-1, 1)]
        if isinstance(theHuman, Human):
            theHuman.speed = [0-theHuman.speed[0],  # else, we set a random speed for each human
                              random.randint(-1, 1)]
        if self.speed == [0, 0]:  # this ensures that no human will have 0 speed
            self.speed = [0, 1]
        if isinstance(theHuman, Human) and theHuman.speed == [0, 0]:
            theHuman.speed = [-1, 0]

    # method for updating the human's condition
    def update(self):
        if self.isInfected and self.HP > 110:    # if I am infected but my health is above 110
            self.color = 'yellow'               # then my color is yellow in canvas
            self.isShowingSymptom = False       # and I won't show any symptom
        elif self.isInfected and self.HP <= 110 and self.HP > 40:    # if my health is 40 < HP <= 110
            self.color = 'red'                  # then my color is red
            self.isShowingSymptom = True        # and I will also show symptom
        elif self.isInfected and self.HP <= 40 and self.HP > 0:     # if my health is 0 < HP <= 30
            self.deactivate()       # I'm dying and I can't move anymore
        elif self.HP == 0:          # else, I'm dead
            self.color = 'black'        # my color will be black
            self.isInfected = False     # and I won't infect other people again

    # method for decreasing the human's HP if he is infected
    # this method is called once per day. so infected human will die in 10 days
    def decHP(self):
        if self.isInfected:
            self.HP -= 10   # decrease the human HP by 10 if he is infected
