import tkinter as tk
from frames.startFrame import startFrame
from frames.pauseWindow import pauseWindow
from frames.selectGameFrame import selectGameFrame
from frames.selectPlayersFrame import selectPlayersFrame
from frames.gameFrame import gameFrame
from frames.leaderBoardFrame import leaderBoardFrame
from frames.signInOutWindow import signInOutWindow
from frames.achievementsWindow import achievementsWindow
from database.dbHandler import dbHandler
from constants import START_FULLSCREEN,BUTTON_DEFAULT_COLOUR,FRAME_BG_DEFAULT_COLOUR,TEXT_FONT,FRAME_TOP_BAR_COLOUR

class mainWindow:
    def __init__(self):
        #set tk window vars
        self.__window = tk.Tk()
        self.__window.attributes("-fullscreen", START_FULLSCREEN)
        self.__window.grab_set()
        self.__window.focus_force()

        self.__window.title("Carcassonne")

        #set tk frames for tk children
        self.__topBarFrame = tk.Frame(self.__window,bg=FRAME_TOP_BAR_COLOUR)
        self.__topBarFrame.pack(side="top", fill ="x")

        self.__topBarFrameL = tk.Frame(self.__topBarFrame)
        self.__topBarFrameL.pack(side="left")

        self.__topBarFrameR = tk.Frame(self.__topBarFrame)
        self.__topBarFrameR.pack(side="right")

        self.__bottomFrame = tk.Frame(self.__window,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__bottomFrame.pack(side="top", fill="both",expand=True)

        #used to get buttons to be square
        self.__pixel = tk.PhotoImage(width=1, height=1)

        tk.Label(self.__topBarFrameL,text ="Carcassonne",font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(side="left")
        tk.Button(self.__topBarFrameR, text="Exit",font=(TEXT_FONT,16), width=32,height=32,image=self.__pixel, compound='c', command=self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack(side="right")
        tk.Button(self.__topBarFrameR, text = "☰",font=(TEXT_FONT,16), width=32,height=32,image=self.__pixel, compound='c', command = self.__displayPauseWindow, bg = BUTTON_DEFAULT_COLOUR).pack(side="right")
        tk.Button(self.__topBarFrameR, text = "🏅", font=(TEXT_FONT,16,"bold"), width=32,height=32,image=self.__pixel, compound='c', command=self.__displayAchievements).pack(side="right")
        self.__signInOutButton = tk.Button(self.__topBarFrameR,text="👤",font=(TEXT_FONT,16), width=32,height=32,image=self.__pixel, compound='c', bg = BUTTON_DEFAULT_COLOUR)

        self.__dbHandler = dbHandler()

        #for full screen mode
        self.__window.bind("<Escape>", self.__endFullscreen)
        self.__window.bind("<F11>", self.__beginFullscreen)

        #playing game attribute to indicate game window, used for showing save button on pause menu
        self.__playingGame = False

        #setting current login to keep track of login
        self.__currentLogin = ""

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
        self.__signInOutButton.pack(side="right")
        self.__signInOutButton.config(command=self.__displaySignInOut)
        startFrame(self.__window, self.__bottomFrame, self.__displaySelectGameFrame)

    def __displaySelectGameFrame(self):
        selectGameFrame(self.__bottomFrame, self.__displaySelectPlayersFrame, self.__displayGameFrame, self.__getLoginID, self.__dbHandler, self.__displaySignInOut, self.__signInOutButton)

    def __displaySelectPlayersFrame(self, gameID):
        self.__signInOutButton.pack_forget()
        selectPlayersFrame(self.__bottomFrame, gameID, self.__displayGameFrame, self.__dbHandler)

    def __displayGameFrame(self, gameID):
        self.__signInOutButton.pack_forget()
        self.__playingGame = True
        self.__gameWindowObj = gameFrame(self.__bottomFrame, gameID, self.__displayLeaderBoardFrame, self.__dbHandler)

    def __displayLeaderBoardFrame(self,playerScoreDict):
        self.__playingGame = False
        leaderBoardFrame(self.__window, self.__bottomFrame, playerScoreDict,self.__displayStartFrame)

    def __displaySignInOut(self):
        return signInOutWindow(self.__window,self.__currentLogin,self.__setLoginID,self.__dbHandler)
    
    def __displayAchievements(self):
        achievementsWindow(self.__window, self.__getLoginID, self.__dbHandler, self.__displaySignInOut)

    def __saveGame(self):
        self.__gameWindowObj.saveGame()

    def __setLoginID(self, user):
        self.__currentLogin = user

    def __getLoginID(self):
        return self.__currentLogin

    def run(self):
        self.__window.mainloop()