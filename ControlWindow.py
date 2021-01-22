"""
Modul ini berisi class untuk control window
"""
import tkinter
import tkinter.messagebox

class ControlWindow():
    def __init__(self, simulatorClass):  # control window needs the data about the
        self.simulatorClass = simulatorClass    # simulator class it wants to control

        # create the control window
        self.controlWindow = tkinter.Toplevel(self.simulatorClass.simulationWindow)
        self.controlWindow.title('Control Window')

        # create the left and right frame
        self.leftFrame = tkinter.Frame(self.controlWindow)
        self.rightFrame = tkinter.Frame(self.controlWindow)

        # create buttons for the left frame
        self.playButton = tkinter.Button(self.leftFrame, text='Play', width=20, height=2, bg='green',
                                         command=self.simulatorClass.startSimulation)
        self.quitButton = tkinter.Button(self.leftFrame, text='Quit', width=20, height=2, bg='red',
                                         command=self.simulatorClass.simulationWindow.destroy)

        # create buttons for the right frame
        self.pauseButton = tkinter.Button(self.rightFrame, text='Pause', width=20, height=2, bg='yellow',
                                          command=self.simulatorClass.stopSimulation)
        self.helpButton = tkinter.Button(self.rightFrame, text='Help', width=20, height=2, bg='white',
                                         command=self.showHelp)

        # pack all the widgets for the left frame
        self.playButton.pack()
        self.quitButton.pack()

        # pack all the widgets for the right frame
        self.pauseButton.pack()
        self.helpButton.pack()

        # pack all the frames
        self.leftFrame.pack(side='left')
        self.rightFrame.pack(side='right')

    def showHelp(self):
        tkinter.messagebox.showinfo('Help',
                                    '- "Play" button : starts the simulation\n'
                                    '- "Pause" button : pause the simulation\n'
                                    '- "Quit" button : close the simulation\n'
                                    '- "Help" button : show the help\n\n'
                                    'Object colors and shape meaning:\n'
                                    '- Blue Circle : Healthy human\n'
                                    '- Yellow Circle : Infected Human, but no symptom\n'
                                    '- Red Circle : Infected Human, but showing symptom\n'
                                    '- Black Circle : Dead Human\n'
                                    '- Green Rectangle : Sterile Surface\n'
                                    '- Orange Rectangle : Infected Surface\n\n'
                                    'Rules:\n'
                                    '- Human will not interact with a human that is showing symptom\n'
                                    "- Human that has been infected for 7 days will be dying and couldn't move anymore")
        self.controlWindow.deiconify()