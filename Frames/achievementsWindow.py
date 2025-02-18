import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, ACHIEVEMENTS_SIZE, WINDOW_CENTER_OFFSET, TEXT_FONT

class achievementsWindow:
    def __init__(self, window, getLoginFunc, dbHandler, signInOutFunc):
        #new tk window
        self.__achievementWindow = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__achievementWindow.grab_set()
        self.__achievementWindow.focus_force()
        self.__achievementWindow.title("Achievements")
        self.__achievementWindow.geometry(str(ACHIEVEMENTS_SIZE[0])+"x"+str(ACHIEVEMENTS_SIZE[1]))

        self.__center_window(self.__achievementWindow)

        self.__getLogin = getLoginFunc
        self.__dbHandler = dbHandler
        self.__signInOutFunc = signInOutFunc

        self.__initiateDisplayFrame()

    def __initiateDisplayFrame(self):
        #removes tk children
        for widget in self.__achievementWindow.winfo_children():
            widget.destroy()

        if self.__getLogin() != "":
            pass
        else:
            self.__loginButton = tk.Button(self.__achievementWindow,text = "Login", font = (TEXT_FONT,13), command= self.__openLoginWindow)
            self.__loginButton.place(relx=0.5,rely=0.5,anchor="center")

    def __openLoginWindow(self):
        self.__achievementWindow.winfo_toplevel().wait_window(self.__signInOutFunc().getSignWindow())
        self.__initiateDisplayFrame()

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2-WINDOW_CENTER_OFFSET
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")