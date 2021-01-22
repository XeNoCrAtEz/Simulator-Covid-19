"""
Modul ini berisi class untuk menampilkan data manusia yang terinfeksi
"""
import tkinter

class NewsWindow():
    def __init__(self, simulatorClass):  # infected curve window needs data from the simulator class
        self.simulatorClass = simulatorClass

        # set the initial size of the graph window
        self.x_axis = 300
        self.y_axis = 160

        # create the graph/curve window
        self.newsWindow = tkinter.Toplevel(self.simulatorClass.simulationWindow)
        self.newsWindow.title('News Report')

        # the curve is drawn using canvas
        self.news = tkinter.Canvas(self.newsWindow, width=self.x_axis,
                                   height=self.y_axis, bg='white')

        # pack the canvas
        self.news.pack()

        # other attributes
        data = self.simulatorClass.getData()
        self.healthyCount = data[0]
        self.infectedHuman = data[1]
        self.deathCount = data[2]
        self.infectedSurface = data[3]

        # display initial data
        self.text = 'Day - 0 :' \
                    '\nHealthy Humans = '+str(self.healthyCount)+\
                    '\nInfected Humans = '+str(self.infectedHuman)+\
                    '\nDeath Count = '+str(self.deathCount)+\
                    '\nInfected Surface = '+str(self.infectedSurface)

        # create the text
        self.dataReport = self.news.create_text(150, 80, text=self.text,
                                                font='Times 20')

    # method to draw graph of infected people over time every 1 day
    def updateData(self):
        data = self.simulatorClass.getData()
        self.healthyCount = data[0]
        self.infectedHuman = data[1]
        self.deathCount = data[2]
        self.infectedSurface = data[3]
        self.day = data[4]
        self.text = 'Day - '+str(self.day) + ' :' + \
                    '\nHealthy Humans = ' + str(self.healthyCount) + \
                    '\nInfected Humans = ' + str(self.infectedHuman) + \
                    '\nDeath Count = ' + str(self.deathCount) + \
                    '\nInfected Surface = ' + str(self.infectedSurface)
        self.news.itemconfigure(self.dataReport,
                                text=self.text)
