"""
Modul ini berisi class untuk window inisialisasi keadaan awal simulator
Modul ini adalah modul program utama
"""
import tkinter
import tkinter.messagebox
import random
import SimulationWindow, ControlWindow
import Human, Surfaces

class InitWindow():
    def __init__(self):
        # create the root widget of the program
        self.initWindow = tkinter.Tk()
        self.initWindow.title('Initialize Simulation')  # for changing the program title
        self.initWindow.configure(bg='white')

        # create all the frames
        self.topFrame = tkinter.Frame(self.initWindow, width=370, height=30, bg='white')
        self.centerLeftFrame = tkinter.Frame(self.initWindow, width=115, height=60, bg='white')
        self.bottomFrame = tkinter.Frame(self.initWindow, width=370, height=50, bg='white')
        self.centerRightFrame = tkinter.Frame(self.initWindow, width=255, height=57, bg='white')

        # widgets for the top frame
        self.helpButton = tkinter.Button(self.topFrame, text='Help',
                                         width=20, command=self.showHelp)
        self.quitButton = tkinter.Button(self.topFrame, text='Quit',
                                         width=20, command=self.initWindow.destroy)

        # widgets for the center left frame
        self.initHumanPrompt = tkinter.Label(self.centerLeftFrame,
                                             text='Jumlah manusia',
                                             bg='white')
        self.initSurfacePrompt = tkinter.Label(self.centerLeftFrame,
                                               text='Jumlah permukaan',
                                               bg='white')
        self.initWorldSizePrompt = tkinter.Label(self.centerLeftFrame,
                                                 text='Ukuran dunia (meter)',
                                                 bg='white')

        # widgets for the center right frame
        self.initHumanEntry = tkinter.Entry(self.centerRightFrame,
                                            width=45)
        self.initSurfaceEntry = tkinter.Entry(self.centerRightFrame,
                                              width=45)
        self.initWorldWidthEntry = tkinter.Entry(self.centerRightFrame,
                                                 width=20)
        self.initWorldHeightEntry = tkinter.Entry(self.centerRightFrame,
                                                  width=20)
        self.times = tkinter.Label(self.centerRightFrame,  # label for the 'X'
                                   text='X',
                                   bg='white')

        # widgets for the bottom frame
        self.mode = tkinter.IntVar()  # variable named 'mode' to store the game's mode
        self.mode.set(1)  # set the default mode to 1
        self.mode1RB = tkinter.Radiobutton(self.bottomFrame,  # No Social Distancing option
                                           text='No Social Distancing Mode',
                                           variable=self.mode,
                                           value=1, bg='white')
        self.mode2RB = tkinter.Radiobutton(self.bottomFrame,  # Extreme Social Distancing option
                                           text='Extreme Social Distancing Mode',
                                           variable=self.mode,
                                           value=2, bg='white')
        self.startButton = tkinter.Button(self.bottomFrame,  # Start Simulation Button
                                          text='GASSS!!!',
                                          width=23,
                                          height=3,
                                          command=self.startSimulation)

        # pack all the top frame widgets
        self.helpButton.pack(side='left')
        self.quitButton.pack(side='right')

        # pack all the center left frame widgets
        self.initHumanPrompt.pack(side='top')
        self.initSurfacePrompt.pack(side='top')
        self.initWorldSizePrompt.pack(side='top')

        # pack all the center right frame widgets
        self.initHumanEntry.pack()
        self.initSurfaceEntry.pack()
        self.initWorldHeightEntry.pack(side='right')
        self.times.pack(side='right')
        self.initWorldWidthEntry.pack(side='right')

        # pack all the bottom frame widgets
        self.startButton.pack(side='right')
        self.mode2RB.pack(side='bottom')
        self.mode1RB.pack(side='left')

        # pack all the frames
        self.topFrame.pack()
        self.topFrame.pack_propagate(0)  # pack_propagate is set to 0
        self.bottomFrame.pack(side='bottom')  # so we can change the width and height
        self.bottomFrame.pack_propagate(0)  # of the frames manually
        self.centerLeftFrame.pack(side='left')
        self.centerLeftFrame.pack_propagate(0)
        self.centerRightFrame.pack(side='right')
        self.centerRightFrame.pack_propagate(0)

        # create empty list to store initialized human and surfaces data
        self.humans = []
        self.surfaces = []

    # method for displaying help
    def showHelp(self):
        tkinter.messagebox.showinfo('Help',
                                    '- Quit button : Close the application\n'
                                    '- "GAASS!!" button : Start the simulation\n\n'
                                    '- Input all the initial condition of the simulation and then press "GAASSS!! :\n'
                                    '  Jumlah manusia          : Initial human population\n'
                                    '  Jumlah permukaan     : Initial surface population\n'
                                    '  Ukuran dunia (meter) : Size of the world in meter\n'
                                    '\t- The first value is its width\n'
                                    '\t- The second value is its height\n'
                                    '- No Social Distancing Mode : All human is moving and interact with other human ot surface\n'
                                    '- Extreme Social Distancing Mode : 80% of the human is inactive\n\n'
                                    "Note : If you didn't specify the initial value, then it will use the default value :\n"
                                    "\t- Jumlah manusia      : 10\n"
                                    "\t- Jumlah permukaan : 5\n"
                                    "\t- Ukuran dunia          : 500 X 500\n"
                                    "\t- No Social Distancing Mode\n\n"
                                    "ENJOY!!! :)")

    # method for starting the simulation
    def startSimulation(self):
        # before starting the simulation, we check all the entries first
        # if one of the entries haven't been inputted, then use the default value
        try:
            self.initHuman = int(self.initHumanEntry.get())
        except ValueError:
            self.initHuman = 10  # default human count is 10

        try:
            self.initSurface = int(self.initSurfaceEntry.get())
        except ValueError:
            self.initSurface = 5  # default surface count is 5

        try:
            self.initWorldWidth = int(self.initWorldWidthEntry.get())
        except ValueError:
            self.initWorldWidth = 500  # default world width is 500

        try:
            self.initWorldHeight = int(self.initWorldHeightEntry.get())
        except ValueError:
            self.initWorldHeight = 500  # default world height is 500

        # create the list of humans and surfaces
        self.createHumans()
        self.createSurfaces()

        # create the simulation window and the control window
        # pass the created humans and surfaces to the simulation window
        # let the simulation window draw the objects
        simuWin = SimulationWindow.SimulationWindow(self)
        ctrlWin = ControlWindow.ControlWindow(simuWin)

        # let's wait until the user press 'play' button from control window

    # method to create a list of humans
    def createHumans(self):
        self.humans = []    # set the humans list to empty to ensure it is empty
        for i in range(self.initHuman):
            # append new human to humans list that has random initial location
            self.humans.append(Human.Human(location=[random.randint(0, self.initWorldWidth-10),
                                                     random.randint(0, self.initWorldHeight-10)]))
            # it has minus 10 because the size of the object is 10x10

            # next set the initial speed of the human
            if self.mode.get() == 2 and i < self.initHuman*80/100:  # if we use mode 2 (extreme social distancing)
                self.humans[i].deactivate()                         # then 80% of the humans must be deactivated
            else:
                self.humans[i].speed = [random.randint(-1, 1),      # else, we set a random speed for each human
                                        random.randint(-1, 1)]
                if self.humans[i].speed == [0, 0]:      # this ensures that no human will have 0 speed
                    self.humans[i].speed = [0, 1]
        self.humans[self.initHuman-1].isInfected = True    # the last human we create is the patient zero
        self.humans[self.initHuman-1].color = 'yellow'     # set the patient zero's color accordingly

    # method to create a list of surfaces
    def createSurfaces(self):
        self.surfaces = []      # set the surfaces list to empty to ensure it is empty
        for i in range(self.initSurface):
            # append new surface to surfaces list that has random initial location and material
            self.surfaces.append(Surfaces.Surface(material=random.choice(Surfaces.materials),
                                                  location=[random.randint(0, self.initWorldWidth-10),
                                                            random.randint(0, self.initWorldHeight-10)]))
            # it has minus 10 because the size of the object is 10x10

def main():
    covidSimulator = InitWindow()
    covidSimulator.initWindow.mainloop()

if __name__ == '__main__':
    main()