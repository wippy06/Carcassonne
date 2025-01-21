import tkinter as tk
from frames.start import start
from frames.pause import pause
from frames.selectGame import selectGame
from frames.selectPlayers import selectPlayers
from frames.gameWindow import gameWindow
from constants import START_FULLSCREEN

class mainWindow:
    def __init__(self):
        #set tk vars
        self.__window = tk.Tk()
        self.__window.attributes("-fullscreen", START_FULLSCREEN)

        self.__window.title("Carcassonne")

        self.__topBarFrame = tk.Frame(self.__window)
        self.__topBarFrame.pack(side="top", fill ="x")

        self.__topBarFrameL = tk.Frame(self.__topBarFrame)
        self.__topBarFrameL.pack(side="left")

        self.__topBarFrameR = tk.Frame(self.__topBarFrame)
        self.__topBarFrameR.pack(side="right")

        self.__bottomFrame = tk.Frame(self.__window)
        self.__bottomFrame.pack(side="top")

        tk.Label(self.__topBarFrameL,text ="Carcassonne").pack()
        tk.Button(self.__topBarFrameR, text = "Pause", command = self.__pause).pack()
        tk.Button(self.__topBarFrameR, text="Exit", command=self.__window.destroy).pack()

        self.__window.bind("<Escape>", self.__endFullscreen)
        self.__window.bind("<F11>", self.__beginFullscreen)


        #set game info as vars
        self.gameSlot = 0
        self.playerNo = 0
        self.playerQueue = []

        #start program
        self.__startScreen()

    def __pause(self):
        pause(self.__window)

    def __endFullscreen(self, event):
        self.__window.attributes("-fullscreen", False)

    def __beginFullscreen(self, event):
        self.__window.attributes("-fullscreen", True)

    def __startScreen(self):
        start(self.__window, self.__bottomFrame, self.__selectGame)

    def __selectGame(self):
        selectGame(self.__bottomFrame, self.__selectPlayers, self.__loadGame)

    def __selectPlayers(self, gameSlot):
        selectPlayers(self.__bottomFrame, gameSlot, self.__loadGame)

    def __loadGame(self, gameFile):
        gameWindow(gameFile)

    def run(self):
        self.__window.mainloop()