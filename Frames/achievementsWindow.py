import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, ACHIEVEMENTS_SIZE, TEXT_FONT,FRAME_TOP_BAR_COLOUR,BUTTON_DEFAULT_COLOUR
from .achievementInfoWindow import achievementInfoWindow

class achievementsWindow:
    def __init__(self, window, getLoginFunc, dbHandler, signInOutFunc):
        #new tk window
        self.__achievementWindow = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR,highlightthickness=2)
        self.__achievementWindow.grab_set()
        self.__achievementWindow.focus_force()
        self.__achievementWindow.title("Achievements")
        self.__achievementWindow.geometry(str(ACHIEVEMENTS_SIZE[0])+"x"+str(ACHIEVEMENTS_SIZE[1]))
        self.__achievementWindow.wm_overrideredirect(True)

        self.__achievementWindowTopBar = tk.Frame(self.__achievementWindow,bg=FRAME_TOP_BAR_COLOUR)
        self.__achievementWindowMainFrame = tk.Frame(self.__achievementWindow,bg=FRAME_BG_DEFAULT_COLOUR)

        self.__achievementWindowTopBar.pack(fill="x",anchor="n")
        self.__achievementWindowMainFrame.pack(fill="both",expand=True,anchor="n",side="top")

        tk.Label(self.__achievementWindowTopBar,text ="Achievements",font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(side="left")

        #used to set button size
        pixel = tk.PhotoImage(width=1, height=1)

        closeButton = tk.Button(self.__achievementWindowTopBar, text="❌",font=(TEXT_FONT,16),width=30,height=30,image=pixel, compound='c', command=self.__achievementWindow.destroy, bg = BUTTON_DEFAULT_COLOUR)
        closeButton.image = pixel
        closeButton.pack(side="right")

        helpButton = tk.Button(self.__achievementWindowTopBar, text="?",font=(TEXT_FONT,16),width=30,height=30,image=pixel, compound='c', command=lambda:achievementInfoWindow(self.__achievementWindow), bg = BUTTON_DEFAULT_COLOUR)
        helpButton.image = pixel
        helpButton.pack(side="right")

        self.__center_window(self.__achievementWindow)

        self.__getLogin = getLoginFunc
        self.__dbHandler = dbHandler
        self.__signInOutFunc = signInOutFunc

        self.__initiateDisplayFrame()

    def __initiateDisplayFrame(self):
        #removes tk children
        for widget in self.__achievementWindowMainFrame.winfo_children():
            widget.destroy()

        if self.__getLogin() != "":
            #holds the canvas and the scroll bar
            gameListFrame = tk.Frame(self.__achievementWindowMainFrame)
            gameListFrame.place(relx=0.5,rely=0.5,anchor="center")

            #canvas is used as frame can't be scrolled through
            canvas = tk.Canvas(gameListFrame, height=ACHIEVEMENTS_SIZE[1]-100, width=ACHIEVEMENTS_SIZE[0]-100)
            canvas.pack(side="left")

            scrollBar = tk.Scrollbar(gameListFrame, orient="vertical", command=canvas.yview)
            scrollBar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollBar.set)

            #new frame to hold game frames
            canvasFrame = tk.Frame(canvas, highlightthickness=2)
            canvas.create_window((0, 0), window=canvasFrame, anchor="nw", width=ACHIEVEMENTS_SIZE[0]-100)

            gameDict = self.__dbHandler.getCompletedUsersGamesAndAchievements(self.__getLogin())

            for gameID in gameDict.keys():
                gameFrame = tk.Frame(canvasFrame, highlightthickness=1, highlightbackground="black",pady=5)
                gameFrame.pack(fill="x")

                tk.Label(gameFrame, text="Game " + str(gameID), font=(TEXT_FONT, 13)).pack(side="left")
                
                for symbol in gameDict[gameID]:
                    tk.Label(gameFrame, text=symbol, font=(TEXT_FONT, 13),width=2).pack(side="right")

            # Update scroll region to allow proper scrolling
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

            canvas.bind_all("<MouseWheel>", lambda event:canvas.yview_scroll(-1 if event.delta > 0 else 1, "units"))

        else:
            self.__loginButton = tk.Button(self.__achievementWindowMainFrame,text = "Login", font = (TEXT_FONT,13), bg = BUTTON_DEFAULT_COLOUR, command= self.__openLoginWindow)
            self.__loginButton.place(relx=0.5,rely=0.5,anchor="center")

    def __openLoginWindow(self):
        self.__achievementWindow.winfo_toplevel().wait_window(self.__signInOutFunc().getSignWindow())
        self.__achievementWindow.grab_set()
        self.__initiateDisplayFrame()

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")