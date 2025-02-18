import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, ACHIEVEMENTS_SIZE, WINDOW_CENTER_OFFSET

class achievementsWindow:
    def __init__(self, window, getLoginFunc, dbHandler, displaySignInOutFunc):
        #new tk window
        self.__signWindow = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__signWindow.grab_set()
        self.__signWindow.focus_force()
        self.__signWindow.title("Sign In/Out")
        self.__signWindow.geometry(str(ACHIEVEMENTS_SIZE[0])+"x"+str(ACHIEVEMENTS_SIZE[1]))

        self.__center_window(self.__signWindow)

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2-WINDOW_CENTER_OFFSET
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")