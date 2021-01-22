"""
Modul ini berisi class permukaan
"""
materials = ['plastic', 'metal', 'paper', 'wood']   # list of valid materials

class Surface():
    # initialize all attributes of the surface
    def __init__(self, material, location=(0, 0),
                 color='green', drawID=0):
        self.material = material
        self.location = location
        self.color = color
        self.drawID = drawID
        self.isInfected = False     # all surface is sterile when initialized
        self.virusLifetime = 0
        self.size = 12      # attribute to control the size of the surface

    # method for interacting with human
    def interactHuman(self, theHuman):
        # The surface will be infected if it interacts with an infected human
        if theHuman.isInfected == True:
            self.isInfected = True
            self.reInfect()     # re-infect myself everytime I interact with infected human
        else:
            pass

    # method for updating the surface's condition
    def update(self):
        if self.isInfected and self.virusLifetime == 0:     # if I still have 'infected' flag, but the virus is dead
            self.isInfected = False     # then I am no longer infected
            self.color = 'green'        # my color will go back to green
        elif self.isInfected:           # but if I'm still infected
            self.color = 'orange'       # my color will stay purple

    # method for re-infecting the surface
    def reInfect(self):
        # the virus' lifetime depends on the material of the surface
        if self.material == 'plastic':   # that has a lifetime of :
            self.virusLifetime = 7 * 24  # hour
        elif self.material == 'metal':
            self.virusLifetime = 7 * 24  # hour
        elif self.material == 'paper':
            self.virusLifetime = 3  # hour
        elif self.material == 'wood':
            self.virusLifetime = 4 * 24  # hour

    # method for decreasing the virus lifetime
    def decVirusLifetime(self):
        if self.isInfected:     # virus lifetime is decreased only if the surface is infected
            self.virusLifetime -= 1