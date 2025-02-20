import tkinter as tk
from constants import ACHIEVEMENTS_SIZE, TEXT_FONT, BUTTON_DEFAULT_COLOUR
from .achievementInfoWindow import achievementInfoWindow
from .subwindowBase import subwindowBase

class achievementsWindow(subwindowBase):
    def __init__(self, window, getLoginFunc, dbHandler, signInOutFunc):
        self.__getLogin = getLoginFunc
        self.__dbHandler = dbHandler
        self.__signInOutFunc = signInOutFunc

        super().__init__(window, "Game Achievements")

        helpButton = tk.Button(self._topBar, text="?",font=(TEXT_FONT,16),width=30,height=30,image=self._pixel, compound='c', command=lambda:self.__openAchievementInfoWindow(), bg = BUTTON_DEFAULT_COLOUR)
        helpButton.image = self._pixel
        helpButton.pack(side="right")

    def _displayMainFrame(self):
        self._window.geometry(str(ACHIEVEMENTS_SIZE[0])+"x"+str(ACHIEVEMENTS_SIZE[1]))

        #removes tk children
        for widget in self._mainFrame.winfo_children():
            widget.destroy()

        if self.__getLogin() != "":
            #holds the canvas and the scroll bar
            gameListFrame = tk.Frame(self._mainFrame)
            gameListFrame.place(relx=0.5,rely=0.5,anchor="center")

            #canvas used because frame can't be scrolled through
            canvas = tk.Canvas(gameListFrame, height=ACHIEVEMENTS_SIZE[1]-100, width=ACHIEVEMENTS_SIZE[0]-100)
            canvas.pack(side="left")

            scrollBar = tk.Scrollbar(gameListFrame, orient="vertical", command=canvas.yview)
            scrollBar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollBar.set)

            #new frame to hold game frames
            canvasFrame = tk.Frame(canvas, highlightthickness=2)
            canvas.create_window((0, 0), window=canvasFrame, anchor="nw", width=ACHIEVEMENTS_SIZE[0]-100)

            gameDict = self.__dbHandler.getCompletedUsersGamesAndAchievements(self.__getLogin())

            #cycles through results to display
            for gameID in gameDict.keys():
                gameFrame = tk.Frame(canvasFrame, highlightthickness=1, highlightbackground="black",pady=5)
                gameFrame.pack(fill="x")

                tk.Label(gameFrame, text="Game " + str(gameID), font=(TEXT_FONT, 13)).pack(side="left")
                
                for symbol in gameDict[gameID]:
                    tk.Label(gameFrame, text=symbol, font=(TEXT_FONT, 13),width=2).pack(side="right")

            #update for scrolling and bind mouse wheel
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.bind_all("<MouseWheel>", lambda event:canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        else:
            #get the user to login first
            self.__loginButton = tk.Button(self._mainFrame,text = "Login", font = (TEXT_FONT,13), bg = BUTTON_DEFAULT_COLOUR, command= self.__openLoginWindow)
            self.__loginButton.place(relx=0.5,rely=0.5,anchor="center")

    def __openLoginWindow(self):
        #holds until signed in
        self._window.winfo_toplevel().wait_window(self.__signInOutFunc().getWindow())
        self._window.grab_set()
        self._window.focus_force()
        self._displayMainFrame()

    def __openAchievementInfoWindow(self):
        #holds until achievement into window closed
        self._window.winfo_toplevel().wait_window(achievementInfoWindow(self._window).getWindow())
        self._window.grab_set()
        self._window.focus_force()