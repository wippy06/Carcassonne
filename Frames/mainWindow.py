import tkinter as tk
from frames.startFrame import startFrame
from frames.pauseWindow import pauseWindow
from frames.selectGameFrame import selectGameFrame
from frames.selectPlayersFrame import selectPlayersFrame
from frames.gameFrame import gameFrame
from frames.leaderBoardFrame import leaderBoardFrame
from constants import START_FULLSCREEN,BUTTON_DEFAULT_COLOUR,FRAME_BG_DEFAULT_COLOUR,TEXT_FONT

class mainWindow:
    def __init__(self):
        #set tk window vars
        self.__window = tk.Tk()
        self.__window.attributes("-fullscreen", START_FULLSCREEN)

        self.__window.title("Carcassonne")

        #set tk frames for tk children
        self.__topBarFrame = tk.Frame(self.__window,highlightbackground="black",highlightthickness=1,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__topBarFrame.pack(side="top", fill ="x")

        self.__topBarFrameL = tk.Frame(self.__topBarFrame)
        self.__topBarFrameL.pack(side="left")

        self.__topBarFrameR = tk.Frame(self.__topBarFrame)
        self.__topBarFrameR.pack(side="right")

        self.__bottomFrame = tk.Frame(self.__window,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__bottomFrame.pack(side="top", fill="both",expand=True)

        tk.Label(self.__topBarFrameL,text ="Carcassonne",font=(TEXT_FONT,16)).pack(side="left")
        tk.Button(self.__topBarFrameR, text="Exit",font=(TEXT_FONT,16), command=self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack(side="right")
        tk.Button(self.__topBarFrameR, text = "☰",font=(TEXT_FONT,16), command = self.__displayPauseWindow, bg = BUTTON_DEFAULT_COLOUR).pack(side="right")

        #for full screen mode
        self.__window.bind("<Escape>", self.__endFullscreen)
        self.__window.bind("<F11>", self.__beginFullscreen)

        #playing game attribute to indicate game window, used for showing save button on pause menu
        self.__playingGame = False

        #start program
        self.__displayStartFrame()

    #full screen mode methods
    def __endFullscreen(self, event):
        self.__window.attributes("-fullscreen", False)

    def __beginFullscreen(self, event):
        self.__window.attributes("-fullscreen", True)

    #methods to instantiate window objects
    def __displayPauseWindow(self):
        pauseWindow(self.__window,self.__playingGame, self.__saveGame)

    def __displayStartFrame(self):
        for widget in self.__bottomFrame.winfo_children():
            widget.destroy()
        startFrame(self.__window, self.__bottomFrame, self.__displaySelectGameFrame)

    def __displaySelectGameFrame(self):
        selectGameFrame(self.__bottomFrame, self.__displaySelectPlayersFrame, self.__displayGameFrame)

    def __displaySelectPlayersFrame(self, gameSlot):
        selectPlayersFrame(self.__bottomFrame, gameSlot, self.__displayGameFrame)

    def __displayGameFrame(self, gameFile):
        self.__playingGame = True
        self.__gameWindowObj = gameFrame(self.__bottomFrame, gameFile,self.__displayLeaderBoardFrame)

    def __displayLeaderBoardFrame(self,playerScoreDict):
        self.__playingGame = False
        leaderBoardFrame(self.__window, self.__bottomFrame, playerScoreDict,self.__displayStartFrame)

    def __saveGame(self):
        self.__gameWindowObj.saveGame()

    def run(self):
        self.__window.mainloop()