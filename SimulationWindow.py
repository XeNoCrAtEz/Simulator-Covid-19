"""
Modul ini berisi class untuk window simulator
"""
import tkinter
import NewsReport
import Human
import tkinter.messagebox

class SimulationWindow():
    def __init__(self, initClass):  # simulation window needs the data about the simulator initializer class
        # set all the attribute of the simulation window based on the data inside InitWindow Class
        self.initClass = initClass
        self.worldWidth = initClass.initWorldWidth
        self.worldHeight = initClass.initWorldHeight
        self.humans = initClass.humans
        self.surfaces = initClass.surfaces

        # create the simulation window (a top level widget)
        self.simulationWindow = tkinter.Toplevel(self.initClass.initWindow)
        self.simulationWindow.title('Simulation Window')

        # create the world using Canvas
        self.theWorld = tkinter.Canvas(self.simulationWindow, width=self.worldWidth,
                                       height=self.worldHeight, bg='white',
                                       highlightthickness=0)

        # create all the initial objects inside canvas
        # but first, we need a dictionary to store the drawID and its paired object
        self.drawIDDictionary = {}  # an empty dictionary that stores pairs of drawID an its object
        self.drawObjects()

        # pack the world
        self.theWorld.pack()

        # create the graph/curve of infected people based on
        # the simulation window's data
        self.day = 0
        self.newsWindow = NewsReport.NewsWindow(self)

        # other attributes
        self.after_id = None    # after_id to store the ID created by after() method
        self.steps = 0      # attribute to keep the number of steps the human has taken
        self.hour = 0       # attribute to keep track of time
        self.refreshRate = int(1000/60)  # attribute to store specify the refresh rate of the simulation
                                         # default value is 60FPS

    # method for drawing the objects (humans and surfaces) on the simulation window
    def drawObjects(self):
        # draw an oval for every human
        for i in range(len(self.humans)):
            x1 = self.humans[i].location[0]     # create a local variable to store the x location of the human
            y1 = self.humans[i].location[1]     # create a local variable to store the y location of the human
            x2 = x1 + self.humans[i].size
            y2 = y1 + self.humans[i].size
            # create an oval with a size of 10 at the location of the human
            self.humans[i].drawID = self.theWorld.create_oval(x1, y1, x2, y2)
            # add drawID and its object to the drawIDDictionary
            self.drawIDDictionary[self.humans[i].drawID] = self.humans[i]
            # set the color of the human based on its condition
            self.theWorld.itemconfigure(self.humans[i].drawID, fill=self.humans[i].color)

        # draw a rectangle for every surface
        for i in range(len(self.surfaces)):
            x1 = self.surfaces[i].location[0]
            y1 = self.surfaces[i].location[1]
            x2 = x1 + self.surfaces[i].size
            y2 = y1 + self.surfaces[i].size
            # create a rectangle with a size of 10 at the location of the surface
            self.surfaces[i].drawID = self.theWorld.create_rectangle(x1, y1, x2, y2)
            # add drawID and its object to the drawIDDictionary
            self.drawIDDictionary[self.surfaces[i].drawID] = self.surfaces[i]
            # set the color of the surface based on its condition
            self.theWorld.itemconfigure(self.surfaces[i].drawID, fill=self.surfaces[i].color)

    # method for starting the simulation routine
    def startSimulation(self):
        collidedObjects = self.detectCollision()  # check and store collided objects
        if collidedObjects:  # interact the collided objects if there are some
            self.interactObjects(collidedObjects)
        for human in self.humans:   # set the next location for every human
            human.moveHuman(self.worldWidth, self.worldHeight)
            self.updateCollidedObject(collidedObjects)
        self.steps += 1     # indicate that all human have taken one step
        # if one hour has passed (1 hour = 10 steps)
        if self.steps % 10 == 0:
            self.decVirusLifetime()     # decrease the virus lifetime of every infected surface
            self.hour += 1      # indicate that one hour has passed
            print('hour : '+str(self.hour))
        # if one day has passed (1 day = 24 hours = 240 steps)
        if self.steps % 240 == 0:
            self.day += 1
            self.decHumanHP()       # decrease the HP of an infected human
            self.newsWindow.updateData()      # draw the graph
        self.refresh()      # redraw the world with the new position and color of each human
        gameOverFlag = self.gameOverCheck()     # check whether the game has over yet
        if gameOverFlag == 0:   # if all humans have died
            self.newsWindow.updateData()
            self.Lose()
        if gameOverFlag == 1:   # if all humans have won against coronavirus
            self.newsWindow.updateData()
            self.Win()
        if gameOverFlag == 2:   # if we are still fighting against coronavirus
            self.after_id = self.simulationWindow.after(self.refreshRate, self.startSimulation)

    # method for stopping the simulation routine
    def stopSimulation(self):
        if self.after_id:
            self.simulationWindow.after_cancel(self.after_id)
            self.after_id = None

    # method for checking collisions and return a dictionary that pairs the collided objects
    def detectCollision(self):
        collided = {}   # an empty dictionary for storing the collided objects
        for human in self.humans:   # get every human
            x1 = human.location[0]      # store its x location in x1
            y1 = human.location[1]      # store its y location in y1
            x2 = x1 + human.size
            y2 = y1 + human.size
            # check objects that are present in the area x1 and y1, and store it in result
            result = self.theWorld.find_overlapping(x1, y1, x2, y2)
            # if there is more than two objects that are present in that area (meaning: there is a collision)
            if len(result) > 1:
                tmpDict = {}      # create a temporary dictionary
                for i in range(len(result)-1):
                    tmpDict[result[0]] = result[1]  # pair object1 with object 2; object1 with object2; and so on
                collided.update(tmpDict)    # merge the temporary dictionary with the result dictionary
        return collided

    # method to interact all objects that are colliding.
    # it accepts dictionary provided by detectCollision method
    def interactObjects(self, collidedObjects):
        for object1ID, object2ID in collidedObjects.items():    # get the ID of the objects that collided
            object1 = self.drawIDDictionary[object1ID]  # get the objects from drawIDDictionary using the ID
            object2 = self.drawIDDictionary[object2ID]
            if isinstance(object1, Human.Human):        # if I am a human
                if isinstance(object2, Human.Human):    # and I am interacting with another human
                    object1.interactHuman(object2)
                    object2.interactHuman(object1)
                else:       # else, if I am interacting with a surface
                    object1.interactSurface(object2)
                    object2.interactHuman(object1)
            else:       # else, I am a surface and I interact with a human
                if object2 is type(Human.Human):
                    object1.interactHuman(object2)
                    object2.interactSurface(object1)

    # method for updating colliding objects
    # it only update objects from the list of IDs given to it
    def updateCollidedObject(self, collidedObjects):
        for object1drawID, object2drawID in collidedObjects.items():    # get the ID of the collided objects
            object1 = self.drawIDDictionary[object1drawID]      # get the object using the object's ID
            object2 = self.drawIDDictionary[object2drawID]
            # update each object
            object1.update()
            object2.update()

    # method for decreasing the lifetime of the virus on a surface
    def decVirusLifetime(self):
        for surface in self.surfaces:
            surface.decVirusLifetime()
            surface.update()        # also update the surface after decreasing the lifetime

    # method for decreasing the lifetime of infected human
    def decHumanHP(self):
        for human in self.humans:
            human.decHP()
            human.update()      # also update the human after decreasing the HP

    # method for updating the location and color of each object inside the simulation window
    def refresh(self):
        for drawID, theObject in self.drawIDDictionary.items():   # get the drawID and the object itself from drawIDDictionary
            x1 = theObject.location[0]      # create temporary variables to store its x and y location
            y1 = theObject.location[1]
            x2 = x1 + theObject.size
            y2 = y1 + theObject.size
            self.theWorld.coords(drawID, x1, y1, x2, y2)      # move the object to the specified location
            self.theWorld.itemconfigure(drawID, fill=theObject.color)   # also change the color of the object

    # method for checking whether the game has over or not
    def gameOverCheck(self):
        data = self.getData()
        deadCounter = data[2]
        infectedCounter = data[1] + data[3]
        # game over flag is raised when all humans have died :'(
        # or there are no more viruses left (yayy)
        if deadCounter == len(self.humans):
            return 0    # return 0 if the human is all dead (raise the lost flag)
        elif infectedCounter == 0:
            return 1    # return 1 if there is no more virus (raise the win flag)
        else:
            return 2    # return 2 if there is still some virus left (continue the simulation)

    # method that indicates we won against coronavirus
    def Win(self):
        self.stopSimulation()
        tkinter.messagebox.showinfo('Game Over',
                                    "The Humans Have Won Against CoronaVirus!!!")

    # method that indicates we lose against coronavirus and everybody died :'(
    def Lose(self):
        self.stopSimulation()
        tkinter.messagebox.showinfo('Game Over',
                                    "THE HUMANS IS DEAAADD!!!")

    # method for getting data of infected human, surface, death count, etc:
    def getData(self):
        infectedHuman = 0
        infectedSurface = 0
        deathCount = 0
        healthyCount = 0
        # getting the data of infected, dead, and healthy humans
        for human in self.humans:
            if human.HP == 0:
                deathCount += 1
            elif human.isInfected:
                infectedHuman += 1
            else:
                healthyCount += 1
        # getting the data of infected surface
        for surface in self.surfaces:
            if surface.isInfected:
                infectedSurface += 1
        day = self.day
        return [healthyCount, infectedHuman, deathCount, infectedSurface, day]