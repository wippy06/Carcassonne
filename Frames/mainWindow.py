import tkinter as tk
from frames.start import start
from frames.pause import pause
from frames.selectGame import selectGame
from frames.selectPlayers import selectPlayers
from frames.gameWindow import gameWindow
from constants import START_FULLSCREEN

class mainWindow:
    def __init__(self):
        #set tk window vars
        self.__window = tk.Tk()
        self.__window.attributes("-fullscreen", START_FULLSCREEN)

        self.__window.title("Carcassonne")

        #set tk frames for tk children
        self.__topBarFrame = tk.Frame(self.__window,highlightbackground="black",highlightthickness=1)
        self.__topBarFrame.pack(side="top", fill ="x")

        self.__topBarFrameL = tk.Frame(self.__topBarFrame)
        self.__topBarFrameL.pack(side="left")

        self.__topBarFrameR = tk.Frame(self.__topBarFrame)
        self.__topBarFrameR.pack(side="right")

        self.__bottomFrame = tk.Frame(self.__window)
        self.__bottomFrame.pack(side="top", fill="both")

        tk.Label(self.__topBarFrameL,text ="Carcassonne").pack(side="left")
        tk.Button(self.__topBarFrameR, text="Exit", command=self.__window.destroy).pack(side="right")
        tk.Button(self.__topBarFrameR, text = "Pause", command = self.__pause).pack(side="right")

        #for full screen mode
        self.__window.bind("<Escape>", self.__endFullscreen)
        self.__window.bind("<F11>", self.__beginFullscreen)

        #playing game attribute to indicate game window, used for showing save button on pause menu
        self.__playingGame = False

        #start program
        self.__startScreen()

    #full screen mode methods
    def __endFullscreen(self, event):
        self.__window.attributes("-fullscreen", False)

    def __beginFullscreen(self, event):
        self.__window.attributes("-fullscreen", True)

    #methods to instantiate window objects
    def __pause(self):
        pause(self.__window,self.__playingGame, self.__saveGame)

    def __startScreen(self):
        start(self.__window, self.__bottomFrame, self.__selectGame)

    def __selectGame(self):
        selectGame(self.__bottomFrame, self.__selectPlayers, self.__loadGame)

    def __selectPlayers(self, gameSlot):
        selectPlayers(self.__bottomFrame, gameSlot, self.__loadGame)

    def __loadGame(self, gameFile):
        self.__playingGame = True
        self.__gameWindowObj = gameWindow(self.__bottomFrame, gameFile)

    def __saveGame(self):
        self.__gameWindowObj.saveGame()

    def run(self):
        self.__window.mainloop()