import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, ACHIEVEMENTS_SIZE, TEXT_FONT,FRAME_TOP_BAR_COLOUR,BUTTON_DEFAULT_COLOUR

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

        pixel = tk.PhotoImage(width=1, height=1)
        button = tk.Button(self.__achievementWindowTopBar, text="Close",font=(TEXT_FONT,16), width=50,height=30,image=pixel, compound='c', command=self.__achievementWindow.destroy, bg = BUTTON_DEFAULT_COLOUR)
        button.image = pixel
        button.pack(side="right")

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
            gameListFrame.pack()

            #canvas is used as frame can't be scrolled through
            canvas = tk.Canvas(gameListFrame, height=400, width=400)
            canvas.pack(side="left")

            scrollBar = tk.Scrollbar(gameListFrame, orient="vertical", command=canvas.yview)
            scrollBar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollBar.set)

            #new frame to hold game frames
            canvasFrame = tk.Frame(canvas, highlightthickness=2)
            canvas.create_window((0, 0), window=canvasFrame, anchor="nw", width=400)

            for gameID in self.__dbHandler.getAllCompletedUsersGames(self.__getLogin()):
                frame = tk.Frame(canvasFrame, highlightthickness=1, highlightbackground="black")
                frame.pack(fill="x")
                label = tk.Label(frame, text="Game " + str(gameID[0]), font=(TEXT_FONT, 13))
                label.pack(side="left")

            # Update scroll region to allow proper scrolling
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

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